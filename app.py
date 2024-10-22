# app.py
from flask import Flask, render_template, request, redirect, url_for, jsonify
from crypt_utils import encrypt_message, decrypt_message
import sqlite3

app = Flask(__name__)

# SQLite database setup
def init_db():
    """Initialize the database and create the necessary table."""
    conn = sqlite3.connect('secure_it.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            original_message TEXT NOT NULL,
            encrypted_message TEXT NOT NULL,
            decrypted_message TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Encrypt and store message in the database
@app.route('/encrypt', methods=['POST'])
def encrypt():
    message = request.form['message']
    encrypted_msg = encrypt_message(message)
    
    # Store the encrypted message in the database
    conn = sqlite3.connect('secure_it.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO messages (original_message, encrypted_message)
        VALUES (?, ?)
    ''', (message, encrypted_msg))
    conn.commit()
    conn.close()
    
    return redirect(url_for('index'))

# Decrypt a specific message by ID
@app.route('/decrypt/<int:message_id>', methods=['GET'])
def decrypt(message_id):
    conn = sqlite3.connect('secure_it.db')
    cursor = conn.cursor()
    cursor.execute('SELECT encrypted_message FROM messages WHERE id=?', (message_id,))
    encrypted_msg = cursor.fetchone()
    
    if encrypted_msg:
        decrypted_msg = decrypt_message(encrypted_msg[0])
        return redirect(url_for('index', manual_decrypted_message=decrypted_msg))
    else:
        return jsonify({"error": "Message not found"}), 404

# Manual decryption route for user input
@app.route('/manual_decrypt', methods=['POST'])
def manual_decrypt():
    encrypted_message = request.form['manual_encrypted_message']
    
    try:
        decrypted_msg = decrypt_message(encrypted_message.encode())
        return render_template('index.html', manual_decrypted_message=decrypted_msg, messages=get_messages())
    except Exception as e:
        return render_template('index.html', manual_decrypted_message=f"Decryption failed: {str(e)}", messages=get_messages())

# Route for submitting manually entered decrypted message
@app.route('/manual_decrypt_message', methods=['POST'])
def manual_decrypt_message():
    user_decrypted_message = request.form['user_decrypted_message']
    
    # You can save or process the manually entered decrypted message as needed
    print(f"User submitted decrypted message: {user_decrypted_message}")
    
    return redirect(url_for('index'))

# Helper function to retrieve all messages from the database
def get_messages():
    conn = sqlite3.connect('secure_it.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, original_message, encrypted_message FROM messages')
    messages = cursor.fetchall()
    conn.close()
    return messages

# Homepage route
@app.route('/')
def index():
    messages = get_messages()
    return render_template('index.html', messages=messages)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)

