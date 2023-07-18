from flask import render_template, request, redirect, url_for
from app import app
from .forms import LoginForm, SignUpForm, PostForm
from .models import User, Post, db
import requests as r
from .forms import SearchForm
from flask import Flask
from flask_login import login_user, logout_user, login_required, current_user




def get_pokemon(name):
    url = f'https://pokeapi.co/api/v2/pokemon/{name}'
    response = r.get(url)
    smaller_data = {}
    if response.ok:
        data = response.json()

        smaller_data = {
            "name": data['name'],
            "id": data['id'],
            "img_url": data['sprites']['front_shiny'],
            "hp": data['stats'][0]['base_stat'],
            "attack": data['stats'][1]['base_stat'],
            "defense": data['stats'][2]['base_stat']
        }

    return smaller_data
   
 #print(search{name})


@app.route('/search', methods=['GET', 'POST'])
def search():
    form = SearchForm()

    if request.method == 'POST' and form.validate_on_submit():
        
        search_query = form.search_term.data
        pokemon= get_pokemon(search_query)
        
        return render_template('search.html', pokemon=pokemon, form=form)

    return render_template('search.html', form=form)



            

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()  
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()

        if user:
            if password == user.password:
                login_user(user)
                return redirect(url_for('index'))
            else:
                return 'Invalid username or password!'

    return render_template('login.html', form=form)


if __name__ == '__main__':
    app.run()

@app.route('/signup', methods=["GET", "POST"])
def signup_page():
    form = SignUpForm()
    print(request)    
    if request.method =="POST":  
        if form.validate():
            username = form.username.data
            email = form.email.data
            password = form.password.data

            user = User(username, email, password)
            

            db.session.add(user)
            db.session.commit()
            return redirect(url_for('login_page'))
       
    

    return render_template('signup.html', form = form)



@app.route('/Home', methods=['GET', 'POST'])
def index():
    posts = Post.query.all()
       
    return render_template('index.html', posts=posts)

if __name__ == '__main__':
    app.run()


@app.route('/page1')
def page1():
    return render_template('page1.html')

@app.route('/page2')
def page2():
    return render_template('page2.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login_page'))

@app.route('/posts/create', methods=['GET', 'POST'])
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
            
            return redirect(url_for('home'))

    return render_template('createpost.html', form = form)

@app.route('/')
@app.route('/posts')
def home( ):
    posts = Post.query.all()
    return render_template('index.html', posts=posts)

@app.route('/posts/update/<post_id>', methods=['GET', 'POST'])
@login_required
def update_post_page(post_id):

  
    post = Post.query.get(post_id)
    if current_user.id != post.user_id:
        return redirect(url_for('home'))
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
            return redirect(url_for('single_post_page', post_id = post.id))
    return render_template('updatepost.html', post=post, form=form)


@app.route('/post/delete/<post_id>')
@login_required
def delete_post(post_id):
    post = Post.query.get(post_id)
    if current_user.id != post.user_id:
        return redirect(url_for('home'))
    db.session.remove(post)
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/posts/<post_id>')

def single_post_page(post_id):

  
    post = Post.query.get(post_id)

  

    return render_template('singlepost.html', post=post)
    

  