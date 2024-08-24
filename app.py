from flask import Flask, render_template, request, redirect, session
from flask_socketio import SocketIO
import openai
import pyttsx3
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
import pandas as pd
import requests
from flask import request, redirect

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
openai.api_key = "your-API-key"

messages = []

def clear_chat():
    global messages
    messages = [{"role": "system", "content": "This is a general chatbot. Ask me anything!"}]

def chatbot(input_text):
    try:
        if input_text:
            messages.append({"role": "user", "content": input_text})
            chat = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
            reply = chat.choices[0].message.content
            messages.append({"role": "assistant", "content": reply})
            return reply
    except Exception as e:
        return f"An error occurred: {str(e)}"

def speak_text(command):
    engine = pyttsx3.init()
    engine.say(command)
    engine.runAndWait()

df = pd.read_csv('E:/heart.csv')

# Splitting the data into features (X) and target variable (y)
X = df.drop('target', axis=1)
y = df['target']

# Splitting the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = DecisionTreeClassifier()
model.fit(X_train, y_train)

@app.route('/heart', methods=['POST'])
def predict_heart():
    age = int(request.form['age'])
    sex = int(request.form['sex'])
    cp = int(request.form['cp'])
    trestbps = int(request.form['trestbps'])
    chol = int(request.form['chol'])
    fbs = int(request.form['fbs'])
    restecg = int(request.form['restecg'])
    thalach = int(request.form['thalach'])
    exang = int(request.form['exang'])
    oldpeak = float(request.form['oldpeak'])
    slope = int(request.form['slope'])
    ca = int(request.form['ca'])
    thal = int(request.form['thal'])

    input_data = [[age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]]
    prediction = model.predict(input_data)[0]
    if prediction == 0:
        suggestion = "You are healthy. Here are some regular diet plans:\n"
        suggestion1 = "1. Cut down on saturated fat and sugar\n"
        suggestion2 = "2. Eat lots of fruit and veg\n"
        suggestion3 = "3. Eat less salt: no more than 6g a day for adults\n"
        suggestion4 = "4. Get active and be a healthy weight\n"
        suggestion5 = "5. Do not get thirsty\n"
        suggestion6 = "6. Do not skip breakfast"
    else:
        suggestion = "You are likely to have heart disease. Here are some required health measures:\n"
        suggestion1 = "1. Consult a doctor immediately\n"
        suggestion2 = "2. Follow a heart-healthy diet\n"
        suggestion3 = "3. Exercise regularly\n"
        suggestion4 = "4. Monitor your blood pressure and cholesterol levels\n"
        suggestion5 = "5. Avoid smoking and excessive alcohol consumption\n"
        suggestion6 = "6. Get enough sleep\n"

    return render_template('result.html', prediction=prediction, suggestion=suggestion,suggestion1=suggestion1,suggestion2=suggestion2,suggestion3=suggestion3,suggestion4=suggestion4,suggestion5=suggestion5,suggestion6=suggestion6)
@app.route('/')
def signup_login():
    return render_template('main.html')

@app.route('/main', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_input = request.form.get('user_input', '')
        user_input = user_input.lower()

        bot_reply = chatbot(user_input)
        speak_text(bot_reply)

        # Emit the textual output to the client using Socket.IO
        socketio.emit('text_output', {'content': bot_reply})

    return render_template('index.html')

@app.route('/heart_prediction')
def heart_prediction():
    return render_template('index1.html')

import requests
from flask import request, redirect

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        medicines = request.form['medicines']
        
        # Send form data to signup.php
        response = requests.post('http://localhost/termproject/signup.php', data={'username': username, 'password': password, 'medicines': medicines})
        
        if response.status_code == 200:
            medicines = response.text
            session['medicines'] = medicines 
            return redirect('/main') 
            # Redirect to index.html after successful signup
        else:
            return "Error occurred while signing up"
    return render_template('signup.html')

import time

import requests
from flask import request, redirect, render_template

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Send form data to login.php
        response = requests.post('http://localhost/termproject/login.php', data={'username': username, 'password': password})
        
        if response.status_code == 200:
            # Get medicines from the response text
            medicines = response.text
            session['medicines'] = medicines
            return render_template('index.html')
        else:
            return render_template('login.html', error="Invalid username or password.")
    return render_template('login.html')

@app.route('/medicines')
def display_medicines():
    if 'medicines' in session:
        medicines = session['medicines']
        return render_template('med.html', medicines=medicines)
    else:
        return "Medicines data not found. Please log in first."

@socketio.on('voice_input')
def handle_voice_input(data):
    user_input = data.get('text_input', '')
    user_input = user_input.lower()

    bot_reply = chatbot(user_input)
    speak_text(bot_reply)

    # Emit the textual output to the client using Socket.IO
    socketio.emit('text_output', {'content': bot_reply})

if __name__ == '__main__':
    clear_chat()
    socketio.run(app, debug=True)
