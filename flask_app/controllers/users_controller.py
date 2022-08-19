from flask import render_template, request, redirect, session, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.message import Message
from flask_bcrypt import Bcrypt   
from datetime import datetime, timedelta

bcrypt = Bcrypt(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    if not User.validation(request.form):
        return redirect('/')
    
    pwd = bcrypt.generate_password_hash(request.form['password'])
    
    form = {
        'first_name':request.form['first_name'],
        'last_name':request.form['last_name'],
        'email':request.form['email'],
        'password':pwd,
    }
    
    id=User.create_user(form)
    session['id']=id
    
    return redirect('/wall')

@app.route('/login', methods=['POST'])
def login():
    user = User.user_by_email(request.form)
    if not user: 
        flash('Wrong email', 'login')
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash('Wrong password', 'login')
        return redirect('/')
    session['id']=user.id
    return redirect('/wall')

@app.route('/wall')
def wall():
    if not 'id' in session:
        return redirect('/')
    data = {
        'id': session['id']
    }
    user = User.user_by_id(data)
    users = User.get_all()
    number_received = Message.count_messages_received(data)
    number_sent = Message.count_messages_sent(data)
    messages = Message.get_user_messages(data)
    time = datetime.now()
    print(time)
    return render_template('wall.html', user=user, users=users, number_received=number_received, number_sent=number_sent, messages=messages, time=time)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
