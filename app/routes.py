from flask import render_template, request, redirect, url_for
from app import app
from .forms import SignUpForm
from .models import User, db
import requests as r
from .forms import SearchForm
from flask import Flask





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
    if request.method == 'POST':
       
        username = request.form.get('username')
        password = request.form.get('password')
        
 
        if username == 'admin' and password == 'password':
           
            return 'Login successful!'
        else:
            
            return 'Invalid username or password!'
    
    
    return render_template('login.html')


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
   

    
    return render_template('index.html')

if __name__ == '__main__':
    app.run()

@app.route('/page1')
def page1():
    return render_template('page1.html')

@app.route('/page2')
def page2():
    return render_template('page2.html')
