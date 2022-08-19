from unittest import result
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from datetime import datetime, timedelta

class Message:
    
    def __init__(self, data):
        self.id = data['id']
        self.content = data['content']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.sender_id = data['sender_id']
        self.receiver_id = data['receiver_id']
        
        self.sender_name = data['sender_name']
        self.receiver_name = data['receiver_name']
        
    @classmethod
    def send_message(cls, form):
        query = 'INSERT INTO messages (content, sender_id, receiver_id) VALUES (%(content)s, %(sender_id)s, %(receiver_id)s)'
        result = connectToMySQL('muro_privado').query_db(query, form)
        return result
    
    @classmethod
    def count_messages_received(cls, data):
        query = 'SELECT count(receiver_id) FROM messages WHERE receiver_id=%(id)s'
        result = connectToMySQL('muro_privado').query_db(query, data)
        count = result[0]['count(receiver_id)']
        return count
    
    @classmethod
    def count_messages_sent(cls, data):
        query = 'SELECT count(receiver_id) FROM messages WHERE sender_id=%(id)s'
        result = connectToMySQL('muro_privado').query_db(query, data)
        count = result[0]['count(receiver_id)']
        return count
    
    @classmethod
    def get_user_messages(cls, data):
        query = 'SELECT messages.*, receivers.first_name as receiver_name, senders.first_name as sender_name FROM messages LEFT JOIN users as receivers ON receivers.id = receiver_id LEFT JOIN users as senders ON senders.id = sender_id WHERE receiver_id = %(id)s;'
        results = connectToMySQL('muro_privado').query_db(query, data)
        messages = []
        for message in results:     
            inst_message = cls(message)
            messages.append(inst_message)
        return messages
    
    @staticmethod
    def rest_times(time):
        now = datetime.now()
        rest = now - time
        return rest
    
    @classmethod
    def delete(cls, data):
        query = 'DELETE FROM messages WHERE id = %(id)s'
        result = connectToMySQL('muro_privado').query_db(query, data)
        return result

    @staticmethod
    def message_valid(form):
        message_valid = True
        if len(form['content']) < 5:
            flash('Your message should have at least 5 charaters', 'send_message')
            message_valid = False
        return message_valid