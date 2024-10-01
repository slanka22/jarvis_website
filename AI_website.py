from openai import OpenAI 
import webview 
import threading 
from flask import Flask, render_template, request 
from bs4 import BeautifulSoup


app = Flask(__name__)
api_key = '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'
client = OpenAI(api_key=api_key, base_url="https://api.perplexity.ai")
default_ai_content = 'Whatever the user requests to change the website, provide only the raw HTML code without any formatting markers or code block syntax. The HTML should be ready for direct injection into the HTML file. Do not interact with the user, just provide the HTML code. Also dont change whats already in it and set it as it is. Assume that you are adding code into the <body>. The lang has already been created for you along witht he heading and the title and <!DocType>. Also dont delete the last prompt unless the user tells you to clear it out.'
user_content = ''

messages = [
    {'role': 'system', 'content': default_ai_content},
    {'role': 'user', 'content': 'user_content'},
]

def web_start(): 
    app.run(debug=True, use_reloader=False) 


def create_webview():
    webview.create_window("Home", "http://127.0.0.1:5000/", maximized=True)
    webview.start()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/user_input', methods=['POST'])
def user_input():
    user_content = request.form.get('user_input')
    if user_content: 
        message = [
        {'role': 'system', 'content': default_ai_content},
        {'role': 'user', 'content': user_content}
        ]
        data = client.chat.completions.create(model = 'llama-3.1-sonar-large-128k-chat', messages=message)
        response = data.choices[0].message.content
        response = BeautifulSoup(response, 'html.parser')
        response = response.prettify() 
        response = response.replace('```', '')
        response = response.replace('html', '')
        print(response)
        return render_template('home.html', ai_response = response)
    return render_template('home.html') 



if __name__ == '__main__':
    app_thread = threading.Thread(target=web_start)
    app_thread.start()
    create_webview() 
    

