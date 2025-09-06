from flask import Flask, render_template, request
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

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
