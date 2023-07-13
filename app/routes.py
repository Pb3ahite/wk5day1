from flask import render_template, request, redirect, url_for
from app import app
from .forms import SignUpForm
from .models import User, db
import requests as r
from .forms import SearchForm




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


    



            

@app.route('/login')
def login_page():

    return render_template('login.html')


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

@app.route('/home_page', methods=["GET", "POST"])
def home_page():

    
    return render_template('home.html')