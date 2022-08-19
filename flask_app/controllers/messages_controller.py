from flask import render_template, request, redirect, session, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.message import Message


@app.route('/send_message', methods=['POST'])
def send_message():
    if 'id' not in session:
        return redirect('/')
    
    if not Message.message_valid(request.form):
        return redirect('wall')
    
    Message.send_message(request.form)
    return redirect('/wall')

@app.route('/delete/message/<int:id>')
def delete_message(id):
    data = {
        'id':id
    }
    Message.delete(data)
    return redirect('/wall')