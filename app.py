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
    # topics = []
    # depth = 1
    # user_topic = input("Please enter a topic that you want to know about: ")
    # topics.append(
    #     {"role": "user", 
    #      "content": 'Topic: ' + user_topic + '. Can you show what knowledge I can acquire about the above mentioned topic in a list format? show me only the name of the points and description in python key value pair'
    #     }
    # )
    # chat_completio_response = client.chat.completions.create(
    #     messages=topics,
    #     model="gpt-3.5-turbo",
    # )
    # response_data = chat_completio_response.choices[0].message.content
    # response_dict = json.loads(response_data)
    # key_topis = list(response_dict.keys())
    # print(key_topis)
    # print(response_data)

    user_entered_topic = input("Please enter a topic that you want to know about: ")
    init_topic = user_entered_topic
    data = []
    topics = []
    topics.append(user_entered_topic)
    count = 0
    while count < 3:
        current_iteration_topics = list(topics)
        for item in current_iteration_topics:
            print(item)
            if count == 3:
                break
            else:
                query = [{
                    "role": "user",
                    "content" : 'Parent-topic: ' + init_topic + ' Topic: ' + item + '. Can you show what knowledge I can acquire about the above mentioned topic in a list format? show me only the name of the points and description in python dictionary format. Keep the dictionary limited to 3 items'
                }]
                chat_completion_response = client.chat.completions.create(
                    messages=query,
                    model="gpt-3.5-turbo",
                )
                response_data = chat_completion_response.choices[0].message.content.strip('\n').strip()
                response_dict = json.loads(response_data)
                key_topis = list(response_dict.keys())
                value_topics = list(response_dict.values())
                print(key_topis)
                # data.append(response_data)
                query.append({
                    "role": "user",
                    "content": response_data
                })

                # print(key_topis)
                # clear the topics list
                topics.clear()

                # add new topics in topic list
                for itm in key_topis:
                    topics.append(itm)
                
                count += 1
    print(data)
            
            









    return render_template('index.html', data = "Hello")

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8080)