from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from functools import wraps
from datetime import datetime
import database_manager as dbHandler
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'userID' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/', methods=['GET', 'POST'])
@login_required
def home():
    data = dbHandler.listExtension()
    user_id = session.get('userID')
    now = datetime.now()
    current_day = now.strftime('%A')
    current_time = now.strftime('%H:%M')

    if current_day in ['Saturday', 'Sunday']:
        current_day = 'Monday'

    user = dbHandler.get_user_by_id(user_id)
    role = user['role']
    group_id = user['groupID']

    if request.method == 'POST' and role == 'teacher':
        text = request.form['message']
        target_group = int(request.form['target_group'])
        dbHandler.save_public_message(user_id, target_group, text, now)

    if role == 'student':
        public_messages = dbHandler.get_public_messages_for_group(group_id)[:4]
        private_messages = dbHandler.get_recent_received_messages(user_id, limit=3)
    elif role == 'teacher':
        public_messages = []
        private_messages = dbHandler.get_recent_received_messages(user_id, limit=3)
    else:
        public_messages = []
        private_messages = []

    full_schedule = dbHandler.get_group_timetable(group_id)
    today_schedule = [entry for entry in full_schedule if entry[0] == current_day]

    subject_colors = {
        'Maths': '#f28b82',
        'English': '#fdd663',
        'Science': '#a7ffeb',
        'PDHPE': '#ccff90',
        'CPT': '#d3d3d3',
        'French': '#ffd6a5',
        'Food Technology': '#999999',
        'Drama': '#d7aefb',
        'Art': '#ffb5e8',
        'Engineering': '#e6ccb2',
        'German': '#a5d6a7',
        'Chinese': '#ffcc80',
        'Japanese': '#e1bee7',
        'Break': '#f0f0f0'
    }

    current_or_next = None
    for entry in today_schedule:
        _, period, subject, location, start, end = entry
        if start <= current_time <= end:
            current_or_next = {
                'subject': subject,
                'location': location,
                'time': start,
                'status': 'Now',
                'color': subject_colors.get(subject, '#f0f0f0')
            }
            break
        elif current_time < start:
            current_or_next = {
                'subject': subject,
                'location': location,
                'time': start,
                'status': 'Next',
                'color': subject_colors.get(subject, '#f0f0f0')
            }
            break

    return render_template('index.html',
                           content=data,
                           current_class=current_or_next,
                           public_messages=public_messages,
                           private_messages=private_messages,
                           role=role,
                           show_sidebar=True)

def get_current_or_next_class(today_schedule):
    now = datetime.now().strftime('%H:%M')

    for entry in today_schedule:
        _, period, subject, location, start, end = entry
        if start <= now <= end:
            return {
                'subject': subject,
                'location': location,
                'time': start,
                'status': 'Now'
            }
        elif now < start:
            return {
                'subject': subject,
                'location': location,
                'time': start,
                'status': 'Next'
            }

    return None

@app.route('/classes')
@login_required
def classes():
    user_id = session['userID']
    user = dbHandler.get_user_by_id(user_id)

    now = datetime.now()
    current_day = now.strftime('%A')
    current_time = now.strftime('%H:%M')

    if current_day in ['Saturday', 'Sunday']:
        current_day = 'Monday'

    if user['role'] == 'student':
        group_id = user['groupID']
        full_schedule = dbHandler.get_group_timetable(group_id)
    elif user['role'] == 'teacher':
        subject = user['subject']
        full_schedule = dbHandler.get_teacher_timetable(subject)
    else:
        full_schedule = []

    today_schedule = [entry for entry in full_schedule if entry[0] == current_day]

    subject_colors = {
        'Maths': '#f28b82',
        'English': '#fdd663',
        'Science': '#a7ffeb',
        'PDHPE': '#ccff90',
        'CPT': '#d3d3d3',
        'French': '#ffd6a5',
        'Food Technology': '#999999',
        'Drama': '#d7aefb',
        'Art': '#ffb5e8',
        'Engineering': '#e6ccb2',
        'German': '#a5d6a7',
        'Chinese': '#ffcc80',
        'Japanese': '#e1bee7',
        'Break': '#f0f0f0'
    }

    current_or_next = get_current_or_next_class(today_schedule)
    if current_or_next:
        current_or_next['color'] = subject_colors.get(current_or_next['subject'], '#f0f0f0')

    recess = {
        'label': 'Recess',
        'subject': 'Break',
        'location': 'Outside',
        'start': '10:35',
        'end': '10:55',
        'color': subject_colors['Break']
    }
    lunch = {
        'label': 'Lunch',
        'subject': 'Break',
        'location': 'Outside',
        'start': '12:45',
        'end': '13:25',
        'color': subject_colors['Break']
    }

    slots = {
        period: {
            'label': f'Period {period}',
            'subject': subject,
            'location': location,
            'start': start,
            'end': end,
            'color': subject_colors.get(subject, '#ddd')
        }
        for (_, period, subject, location, start, end) in today_schedule
    }

    schedule_left = [slots.get(1), slots.get(2), recess, slots.get(3)]
    schedule_right = [slots.get(4), lunch, slots.get(5), slots.get(6)]

    return render_template('classes.html',
                           current_class=current_or_next,
                           schedule_left=schedule_left,
                           schedule_right=schedule_right)

@app.route('/chat')
@login_required
def chat():
    contacts = dbHandler.get_user_contacts_with_preview(session['userID'])
    return render_template('chat.html', contacts=contacts)

@app.route('/messages/<int:contact_id>')
@login_required
def get_messages(contact_id):
    try:
        user_id = session['userID']
        messages = dbHandler.get_message_history(user_id, contact_id)
        print(f"Messages for user {user_id} with contact {contact_id}: {messages}")
        if not messages:
            messages = [("No messages yet", contact_id)]
        return jsonify(messages)
    except Exception as e:
        print("Error in get_messages:", e)
        return jsonify({"error": str(e)}), 500

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = dbHandler.validate_user(email, password)
        if user:
            session['userID'] = user[0]
            session['name'] = user[1]
            return redirect(url_for('home'))
        else:
            error = 'Invalid email or password.'
    return render_template('login.html', error=error)

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=session['name'])

@app.route('/add_contact_by_email', methods=['POST'])
@login_required
def add_contact_by_email():
    email = request.form['contact_email'].strip().lower()
    contact = dbHandler.find_user_by_email(email)
    if contact:
        dbHandler.add_contact(session['userID'], contact[0])
    return redirect(url_for('chat'))

@app.route('/messages/<contact_id>', methods=['POST'])
def send_message(contact_id):
    data = request.get_json()
    text = data.get('text')
    sender_id = data.get('senderId')
    timestamp = datetime.now()

    dbHandler.save_message(sender_id, contact_id, text, timestamp)

    return jsonify({'status': 'success'})

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = None
    if request.method == 'POST':
        email = request.form['email']
        name = request.form['name']
        password = request.form['password']
        role = request.form['role']
        group_id = request.form.get('groupID') if role == 'student' else None
        subject = request.form.get('subject') if role == 'teacher' else None

        if role == 'student' and not group_id:
            error = 'Please select a class level.'
        elif role == 'teacher' and not subject:
            error = 'Please enter the subject you teach.'
        else:
            success = dbHandler.create_user(email, password, name, role, group_id, subject)
            if success:
                return redirect(url_for('login'))
            else:
                error = 'Email already exists or invalid input.'

    return render_template('signup.html', error=error)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)