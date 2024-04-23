from flask import Flask, render_template, url_for
import requests
from openai import OpenAI

app = Flask(__name__)
API_KEY = open("API_KEY", 'r').read()

client = OpenAI(
    # This is the default and can be omitted
    api_key=API_KEY,
)

@app.route('/')
def index():
    chat_completio_response = client.chat.completions.create(
    messages=[
            {
                "role": "user",
                "content": "Who is Steve Jobs?",
            }
        ],
        model="gpt-3.5-turbo",
    )
    response_data = chat_completio_response.choices[0].message.content
    print()
    return render_template('index.html', data = response_data)

if __name__ == "__main__":
    app.run(debug=True)