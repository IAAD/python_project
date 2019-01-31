import numpy as np
import pandas as pd
import requests
import json
import os

from flask import Flask


app = Flask(__name__)


@app.route('/user')
def notification():
    token = "EAAP2twGHVKwBANXZAufWYyZCTORUzuZBWaQReXkaklqx2M3VQnYJpLSZB8PvBsqc1jxR9U8CZA8FbK1H7ZAqc9st4c8a9ZBAAvuZCAlBrdNZBUC9t60gE9IrWR5JhCVTa4gKZAKiZCnwas6xpi3Y0NRkf0ZBKGY36O9ZAbJ3Vk3vWP4ZBhpgZDZD"
    url = "https://graph.facebook.com/v2.6/me/messages?access_token=" + token
    user_data= pd.read_csv('series_sub.csv')
    file = pd.read_csv('series_update.csv')
    df = pd.DataFrame(file)
    for index, row in df.iterrows():
        movie= row["movie"]
        image = row['movie_image-src']
        episode= row['episode_link']
        link = row['mp4_link-href']
        new = user_data[user_data.movie == movie]
        for index, row in new.iterrows():
            user_id = row["user_id"]
            payload = {
                "attachment": {
                "type": "template",
                "payload": {
                "template_type": "generic",
                "elements": {
                "title": "" + movie,
                "image_url": "" + image,
                "subtitle": "" + episode,
                "buttons": [
                    {
                        "type": "web_url",
                        "title": "Download",
                        "url": "" + link
                    },
                    {
                        "type": "postback",
                        "title": "Stop Updates",
                        "postback": "Unsuscribe to" + movie
                    }
                ]
                }
                }
                }
            }


            post_request(url, payload, user_id)
    return "Notifications sent"


def post_request(url, payload, user_id):
    data_payload = {
            "recipient": {
                "id": user_id
            },
            "message": payload

    }

    headers = {'Content-type': 'application/json'}
    requests.post(url, data=json.dumps(data_payload), headers=headers)
if __name__ == "__main__":
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')