from flask import render_template, request, redirect, url_for, flash
from . import ig
from .forms import PostForm
from ..models import User, Post, db
from flask_login import login_required, current_user



from . import api



@ig.route('/posts/create', methods=['GET', 'POST'])
@login_required
def create_post_page():     
    form = PostForm()
    if request.method == "POST":
        if form.validate():
            title = form.title.data
            caption = form.caption.data
            img_url = form.img_url.data

            my_post = Post(title, caption, img_url, current_user.id)

            db.session.add(my_post)
            db.session.commit()
            flash('Successfully made a post!', 'success')
            return redirect(url_for('ig.home'))

    return render_template('createpost.html', form = form)

def update_post_page(post_id):
    post = Post.query.get(post_id)
    if current_user.id != post.user_id:
        return redirect(url_for('ig.home'))
    form = PostForm()
    if request.method == "POST":
        if form.validate():
            title = form.title.data
            caption = form.caption.data
            img_url = form.img_url.data

            post.title = title
            post.caption = caption
            post.img_url = img_url

            db.session.commit()
            return redirect(url_for('ig.singlepost', post_id = post.id))
        
        return render_template('updatepost.html', post=post, form=form)

  



@ig.route('/post/delete/<post_id>')
@login_required
def delete_post(post_id):
    post = Post.query.get(post_id)
    if current_user.id != post.user_id:
        return redirect(url_for('home'))
    db.session.remove(post)
    db.session.commit()
    return redirect(url_for('ig.home'))

@ig.route('/posts/<post_id>')

def single_post_page(post_id):  
    post = Post.query.get(post_id)
    if post:
        return render_template('singlepost.html', post=post, like_count = len(post.likers2))

  

    return render_template('singlepost.html', post=post)
    

@ig.route('/posts/like/<post_id>')
@login_required
def like_post2(post_id):
    post = Post.query.get(post_id)
    if post:
        current_user.liked_posts2.append(post)    
    db.session.commit()
    return redirect(url_for('ig.home'))

@ig.route('/posts/unlike/<post_id>')
@login_required
def Unlike_post2(post_id):
    post = current_user.liked_posts2.filter_by(post_id=post_id).first()
    if post: 

        current_user.liked_posts2.remove(post)
        db.session.commit()
    return redirect(url_for('ig.home'))

@ig.route('/users')
def users_page():
    users = User.query.all()
    return render_template('users.html', user=users)




@ig.route('/follow/<user_id>')
@login_required
def follow(user_id):
    user = User.query.get(user_id)
    current_user.followed.append(user)
    db.session.commit()

    return redirect(url_for('ig.users'))


@ig.route('/unfollow/<user_id>')
@login_required
def unfollow(user_id):
    user = current_user.followed.filter_by(id=user_id).first()
    if user: 

        current_user.followed.remove(user)
        db.session.commit()
    return redirect(url_for('ig.users'))