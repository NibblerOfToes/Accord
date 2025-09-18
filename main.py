from flask import Flask, render_template, request, redirect, url_for, session
import database_manager as dbHandler

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    data = dbHandler.listExtension()
    return render_template('index.html', content=data)

@app.route('/classes', methods=['GET'])
def classes():
    return render_template('classes.html')

@app.route('/chat', methods=['GET'])
def chat():
    return render_template('chat.html')

import os
app.secret_key = os.urandom(24)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        email = request.form['username']  # assuming you're using email as login
        password = request.form['password']
        user = dbHandler.validate_user(email, password)
        if user:
            session['userID'] = user[0]  # userID is at index 0
            session['name'] = user[1]    # name is at index 1
            return redirect(url_for('home'))
        else:
            error = 'Invalid email or password.'
    return render_template('login.html', error=error)

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/profile')
def profile():
    if 'name' not in session:
        return redirect(url_for('login'))
    return render_template('profile.html', name=session['name'])

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)  