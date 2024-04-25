from flask import Flask, render_template, url_for
import requests
from openai import OpenAI
import json

app = Flask(__name__)
API_KEY = open("API_KEY", 'r').read()

client = OpenAI(
    # This is the default and can be omitted
    api_key=API_KEY,
)

@app.route('/')
def index():
    
    user_entered_topic = input("Please enter a topic that you want to know about: ")
    init_topic = user_entered_topic
    data = []

    topics_to_process = [(init_topic, 0)]  # Initialize with the user-entered topic at level 0
    visited_topics = set()  # Keep track of visited topics to avoid duplicates

    while topics_to_process:
        
        topic, level = topics_to_process.pop(0)  # Pop the topic from the beginning of the list (BFS)
        print(topic)
        if level >= 2:
            break

        if topic not in visited_topics:
            visited_topics.add(topic)

            query = [{
                "role": "user",
                "content": 'Parent-topic: ' + init_topic + ' Topic: ' + topic + '. Can you show what knowledge I can acquire about the above mentioned topic in a list format? show me only the name of the points and description in python dictionary format. Keep the dictionary limited to 3 items. Keys must contain only string, no numerics.'
            }]
            chat_completion_response = client.chat.completions.create(
                messages=query,
                model="gpt-3.5-turbo",
            )
            response_data = chat_completion_response.choices[0].message.content.strip('\n').strip()
            print(response_data)
            response_dict = json.loads(response_data)

            key_topics = list(response_dict.keys())

            query.append({
                    "role": "user",
                    "content": response_data
                })
            print(key_topics)

            # Append response to data
            # data.append(response_data)

            # Add new topics to the topics_to_process list
            for new_topic in key_topics:
                topics_to_process.append((new_topic, level + 1))

    # print(data)

    return render_template('index.html', data=data)
    print(data)
            
            









    return render_template('index.html', data = "Hello")

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8080)