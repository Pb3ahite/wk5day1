from flask import render_template
from app import app




   



@app.route('/')
def home_page():
    
    people = ['Ray Charles', 'Aretha Franklin', 'Amy Winehouse', 'Pink Floyd', 'Led Zeppelin']

  
        

    return render_template('index.html', people = people)



@app.route('/contact')
def contact_page():
    
    Paul = 'Pb3'
    
    return {
        'name': 'Paul',
        'audio_url': 'https://en.wikipedia.org/wiki/What%27d_I_Say'}





