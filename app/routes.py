from flask import render_template, request, redirect, url_for, flash
from app import app
from .forms import LoginForm, SignUpForm, PostForm
from .models import Liked_Pokemon, User, Post, db
import requests as r
from .forms import SearchForm
from flask_login import login_user, logout_user, current_user
import random

@app.route('/users')
def users():
    other_users = User.query.filter(User.id != current_user.id).all()
    return render_template('users.html', other_users=other_users)



@app.route('/battle/<int:opponent_id>')
def battle(opponent_id):
    opponent = User.query.get(opponent_id)
    return render_template('battle.html', opponent=opponent, user=current_user)

@app.route('/battlepage/<int:opponent_id>', methods=['GET', 'POST'])
def battlepage(opponent_id):
    opponent = User.query.get(opponent_id)
    user_pokemon = None  
    other_users = User.query.filter(User.id != current_user.id).all()  # Get a list of other users

    if request.method == 'POST':
        user_pokemon_id = int(request.form.get('user_pokemon_id'))
        user_pokemon = Liked_Pokemon.query.get(user_pokemon_id)

        opponent_pokemon = get_opponent_pokemon()
        winner = determine_winner(user_pokemon, opponent_pokemon)

        return render_template('battlepage.html', opponent=opponent, user=current_user, winner=winner, user_pokemon=user_pokemon, opponent_pokemon=opponent_pokemon, other_users=other_users)

    opponent_pokemon_ids = [1, 2, 3, 4, 5]  
    opponent_pokemon_id = random.choice(opponent_pokemon_ids)
    opponent_pokemon = Liked_Pokemon.query.get(opponent_pokemon_id)

    return render_template('battlepage.html', opponent=opponent, user=current_user, user_pokemon=user_pokemon, opponent_pokemon=opponent_pokemon, other_users=other_users)




# @app.route('/battlepage/<int:opponent_id>', methods=['GET', 'POST'])
# def battlepage(opponent_id):
#     opponent = User.query.get(opponent_id)
#     user_pokemon = None  

#     if request.method == 'POST':
#         user_pokemon_id = int(request.form.get('user_pokemon_id'))
#         user_pokemon = Liked_Pokemon.query.get(user_pokemon_id)

#         opponent_pokemon = get_opponent_pokemon()  
#         winner = determine_winner(user_pokemon, opponent_pokemon)

#         return render_template('battlepage.html', opponent=opponent, user=current_user, winner=winner, user_pokemon=user_pokemon, opponent_pokemon=opponent_pokemon)

#     return render_template('battlepage.html', opponent=opponent, user=current_user, user_pokemon=user_pokemon)

# def get_opponent_pokemon():
    
#     opponent_pokemon_ids = [1, 2, 3, 4, 5]
#     opponent_pokemon_id = random.choice(opponent_pokemon_ids)
    
#     return Liked_Pokemon.query.get(opponent_pokemon_id)

def determine_winner(user_pokemon, opponent_pokemon):
    
    if user_pokemon.attack > opponent_pokemon.defense:
        return 'user'
    elif user_pokemon.attack < opponent_pokemon.defense:
        return 'opponent'
    else:
        return 'tie'




@app.route('/attack/<int:opponent_id>/<int:user_pokemon_id>')
def attack(opponent_id, user_pokemon_id):
    opponent = User.query.get(opponent_id)
    user_pokemon = Liked_Pokemon.query.get(user_pokemon_id)

    current_user.wins += 1
    opponent.losses += 1
    db.session.commit()

    return render_template('battle_result.html', opponent=opponent, user=current_user, user_pokemon=user_pokemon)



@app.route('/add_pokemon/<int:pokemon_id>', methods=['POST'])
def add_pokemon(pokemon_id):
    if current_user.is_authenticated:
        if len(current_user.pokemon_team) >= 5:
            flash('You already have the maximum number of Pokemon in your team.', 'warning')
        else:
            pokemon = Liked_Pokemon.query.get(pokemon_id)
            if pokemon and pokemon not in current_user.pokemon_team:
                current_user.pokemon_team.append(pokemon)
                db.session.commit()
                flash(f'{pokemon.name} has been added to your team.', 'success')
    
    return redirect(url_for('home'))

@app.route('/remove_pokemon/<int:pokemon_id>', methods=['POST'])
def remove_pokemon(pokemon_id):
    if current_user.is_authenticated:
        pokemon = Liked_Pokemon.query.get(pokemon_id)
        if pokemon and pokemon in current_user.pokemon_team:
            current_user.pokemon_team.remove(pokemon)
            db.session.commit()
            flash(f'{pokemon.name} has been removed from your team.', 'success')
    
    return redirect(url_for('home'))


@app.route('/save_pokemon', methods=['POST'])
def save_pokemon():
     pokemon_action = request.form.get('pokemon_action')
     pokemon_name = request.form.get('liked_pokemon')
     liked_pokemon_list = current_user.get_liked_pokemon()
     print(pokemon_action, pokemon_name)
     if pokemon_action == 'like':
        if pokemon_name not in [pokemon.name for pokemon in liked_pokemon_list]:
    
             pokemon = get_pokemon(pokemon_name)
             if pokemon:
                 x = Liked_Pokemon(current_user.id, pokemon['name'])
                 db.session.add(x)
                 db.session.commit()
                 flash(f'{pokemon_name} is now liked!', 'success')
             else:
                 flash('Failed to like the Pokémon!', 'danger')
     elif pokemon_action == 'save':
 
         flash(f'{pokemon_name} is saved!', 'success')

     return redirect(url_for('search'))





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
                flash('Successfully logged in.', 'wuccess')
                return redirect(url_for('home'))
            else:
                flash('Incorrect username/password.', 'danger')
        else:
            flash('Incorrect username.', 'danger')
    else:
        flash('An error has occurred. Please try again later', 'success')


    return render_template('login.html', form=form)




@app.route('/signup', methods=["GET", "POST"])
def signup_page():
    form = SignUpForm()
    print(request)    
    if request.method =="POST":  
        if form.validate():
            username = form.username.data
            email = form.email.data
            password = form.password.data
            first_name = form.first_name.data
            last_name = form.last_name.data
            user = User(username, email, password, first_name, last_name)
            

            db.session.add(user)
            db.session.commit()
            flash('Successfully created user.', 'success')
            return redirect(url_for('login_page'))
        flash('An error has occurred. Please try again later', 'success')
       
    

    return render_template('signup.html', form = form)

# @app.route('/page1')
# def page1():
#     return render_template('page1.html')

# @app.route('/page2')
# def page2():
#     return render_template('page2.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login_page'))




@app.route('/')
@app.route('/posts')
def home( ):
    posts = Post.query.all()
    liked_pokemon_list = []
    if current_user.is_authenticated:
        
        liked_pokemon_list = Liked_Pokemon.query.filter_by(user_id=current_user.id).all()
        liked_pokemon_list = [get_pokemon(lp.name) for lp in liked_pokemon_list]
        
    return render_template('home.html', posts=posts, liked_pokemon_list=liked_pokemon_list)



def update_post_page(post_id):
    post = Post.query.get(post_id)
    if current_user.id != post.user_id:
        return redirect(url_for('ig.home'))
    form = PostForm()
    if request.method == "POST":
        if form.validate():
            title = form.title.data
            caption = form.caption.data
            img_url = form.img_url
            
        db.session.commit()
        return redirect(url_for('ig.singlepost', post_id = post.id))
    return render_template('updatepost.html', post=post, form=form)




