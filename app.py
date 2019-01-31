import numpy as np
import pandas as pd
import requests
import urllib
import json
import os
import random
import csv
import psycopg2
from bs4 import BeautifulSoup
from urllib.parse import urlparse

from flask import Flask
from flask import request
from flask import make_response

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))


    res = processRequest(req)

    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r




def processRequest(req):
    url = urlparse(os.environ["DATABASE_URL"])

    conn = psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
    )
    cur = conn.cursor()
    result = req.get("result")
    meta = result.get("metadata")
    intent = meta.get("intentName")
    request = req.get("originalRequest")
    first_data = request.get("data")
    sender = first_data.get("sender")
    user_id = sender.get("id")
    token = "EAAOADUqeP70BAJCjjmZBd7zz4kRXT5Ywz0j1VUnDZAXTU74Gi3Uro5pNe5r5Q5sVaYC5sDQuFdVaybLR47NCgecWsANXhnA8dVqddnf3hdGg8HEJZCbgU4sixStPvqlZCWyQZCgpDD3U3S7YJg7cHZBEBvcePopwdUNBeQx5JaZBgZDZD"
    url = "https://graph.facebook.com/v2.6/me/messages?access_token=" + token

    if intent == "start":
        url2 = "https://graph.facebook.com/v2.6/" + user_id + "?fields=first_name,last_name,locale,timezone,gender&access_token=" + token
        r4 = requests.get(url2)
        s = r4.json()
        first_name = s.get("first_name")
        joy= u'\U0001F602'
        like='(y)'
        url3="https://graph.facebook.com/v2.6/me/messenger_profile?access_token="+token

        payload= {

                  "text": "Hey " + first_name + "! I am Retina and I would love to be the personal home to all your Movies and Tv series"
                }

        payload2 = {

                  "text":"I would really appreciate it if you signed up for excellent services which will enable you to know stuff like"
            }

        payload3 = {

                  "text":"When Superman finally stops wearing his underwear outside his clothes "+joy+joy+joy
            }

        payload4 = {

                    "text": "Just Kidding"
                }



        fb = {

                    "attachment": {
                        "type": "template",
                        "payload": {
                            "template_type": "generic",
                            "elements": [
                                {
                                    "title": "Sign Up for Retina",
                                    "subtitle": "To get all your Movies and Tv series at your Fingertips",
                                    "buttons": [
                                        {
                                            "type": "postback",
                                            "title": "Sign Up",
                                            "payload": "Signed"
                                        }
                                    ]
                                }

                            ]
                        }
                    }


        }
        post_request(url, payload, user_id)
        post_request(url, payload2, user_id)
        post_request(url, payload3, user_id)
        post_request(url, payload4, user_id)
        post_request(url, fb, user_id)

        return {
             "speech": "",
             "data": {
             },

             "source": "moviebot"

        }
    elif intent == "Signed":
        user_id=str(user_id)
        cur.execute('INSERT INTO user_data (user_id) VALUES('+user_id+')')
        conn.commit()
        conn.close()
        payload_sign = {

            "text": "Thank You for Signing up and I am Super excited to get to know you"
        }

        ques = ['What Would you love to entertain yourself with today? Movies or Tv Series', 'What can I get for you today boss Movies or Tv series', 'Should we dive into some Movies or Tv Series']
        ques = random.choice(ques)
        payload =  {
            "text": ques,
            "quick_replies": [
                {
                    "content_type": "text",
                    "title": "Movies",
                    "payload": "movies"
                },
                {
                    "content_type": "text",
                    "title": "Tv Series",
                    "payload": "tv series"
                }
            ]
        }
        post_request(url, payload_sign, user_id)
        post_request(url, payload, user_id)
        return {
            "speech": "",
            "data": {
            },

            "source": "moviebot"

        }

    elif intent == "task":
        payload_sign = {
            "text": "Hey am Retina your personal home to all your Movies and Tv series"
        }
        payload_sign2 = {
            "text": "And am making a bet that I can get you all those your favourite Tv series and Movies"
        }

        ques = ['So What will it be Tv series or Movies', 'What type of film would you like to start with Tv series or Movies', 'So Should we dive into some Movies or Tv Series']
        ques = random.choice(ques)
        payload =  {
            "text": ques,
            "quick_replies": [
                {
                    "content_type": "text",
                    "title": "Movies",
                    "payload": "movies"
                },
                {
                    "content_type": "text",
                    "title": "Tv Series",
                    "payload": "tv series"
                }
            ]
        }
        post_request(url, payload_sign, user_id)
        post_request(url, payload_sign2, user_id)
        post_request(url, payload, user_id)
        return {
            "speech": "",
            "data": {
            },

            "source": "moviebot"

        }


    elif intent == "tv":
        like = '(y)'
        file = pd.read_csv('top_rated.csv')
        df = pd.DataFrame(file)
        df = df.ix[np.random.choice(df.index, 10, replace=False)]
        user_id = str(user_id)
        cur.execute(
            'SELECT user_id FROM user_data WHERE user_id =' + user_id )
        rows = cur.fetchall()
        count = 0
        for rw in rows:
            count = count + 1
        if count == 0:
            cur.execute('INSERT INTO user_data (user_id) VALUES(' + user_id + ')')
            conn.commit()
            conn.close()
        all_element = []
        for index, row in df.iterrows():
            element = {
                "title": "" + row['movie'],
                "image_url": "" + row['movie_image-src'],
                "subtitle": "" + row['desc'],
                "buttons": [
                    {
                        "type": "postback",
                        "title": "View",
                        "payload": "" + row['movie']+" f*123 x#123 v$456"
                    }
                ]

            }

            all_element.append(element)
        data= json.dumps(all_element, indent=4)

        series= ['Check out this top Tv series But don\'t hesitate to ask for more','You would certainly love to try this out','Here is a few Tv series that are currently Trending \nBut feel free to ask for others \n I have you covered ']
        series= random.choice(series)
        payload_sign = {
            "text": ""+series+" "+like
        }

        payload = {

            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "generic",
                    "elements": data


                }
            }

        }

        post_request(url, payload_sign, user_id)
        post_request(url, payload, user_id)
        return {
            "speech": "",
            "data": {
            },

            "source": "moviebot"

        }

    elif intent == "movies":
        like = '(y)'
        file = pd.read_csv('top_ratedm.csv', encoding="ISO-8859-1")
        df = pd.DataFrame(file)
        df = df.ix[np.random.choice(df.index, 10, replace=False)]
        user_id = str(user_id)
        cur.execute(
            'SELECT user_id FROM user_data WHERE user_id =' + user_id)
        rows = cur.fetchall()
        count = 0
        for rw in rows:
            count = count + 1
        if count == 0:
            cur.execute('INSERT INTO user_data (user_id) VALUES(' + user_id + ')')
            conn.commit()
            conn.close()
        all_element = []
        for index, row in df.iterrows():
            desc = str(row['desc'])
            element = {
                "title": "" + row['name'],
                "image_url": "" + row['image'],
                "subtitle": "" + desc,
                "buttons": [
                    {
                        "type": "postback",
                        "title": "View",
                        "payload": "" + row['name']+" ##**##asdfghjkli"
                    }
                ]

            }

            all_element.append(element)
        data = json.dumps(all_element, indent=4)

        series = ['Check out this top Movies But don\'t hesitate to ask for more',
                  'You would certainly love to try this out',
                  'Here is a few that are currently Trending \nBut feel free to ask for others \n I have you covered ']
        series = random.choice(series)
        payload_sign = {
            "text": "" + series + " " + like
        }

        payload = {

            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "generic",
                    "elements": data

                }
            }

        }

        post_request(url, payload_sign, user_id)
        post_request(url, payload, user_id)
        return {
            "speech": "",
            "data": {
            },

            "source": "moviebot"

        }



    elif intent == "movies download":
        payload = {
            "text": "For the Best experience on an Android device I would suggest follow this steps"
        }
        payload11 = {
            "text": "From the latest version of messenger \n Tap the avatar icon in the top right corner of your messenger home page"
        }

        payload12 = {
            "attachment": {
                "type": "image",
                "payload": {
                    "url": "https://lit-anchorage-95694.herokuapp.com/static/firstpart.png"
                }

            }
        }
        payload13 = {
            "text": "Then turn on Link open externally and you can now download from your favorite browser"
        }
        payload14 = {
            "attachment": {
                "type": "image",
                "payload": {
                    "url": "https://lit-anchorage-95694.herokuapp.com/static/secondpart.png"
                }

            }
        }


        payload2 = {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "generic",
                    "elements": [
                        {
                            "title": "If you have download Issues Please click this Button",
                            "buttons": [
                                {
                                    "type": "postback",
                                    "title": "Download Issues",
                                    "payload": "Issues"
                                }
                            ]
                        }

                    ]
                }
            }
        }
        file = pd.read_csv('movies_data.csv', encoding="ISO-8859-1")
        df = pd.DataFrame(file)
        parameters = result.get("parameters")
        download = parameters.get("movie")
        rating = "5"
        user_id4 = str(user_id)
        strdownload = str(download)
        sq="'"
        cur.execute('INSERT INTO user_movies_rating (user_id,rating,movies) VALUES('+user_id4+','+rating+','+sq+strdownload+sq+')')
        conn.commit()
        conn.close()
        new_df = df[df["name"].str.contains(download, na=False, case=False)]
        all_element = []
        series = ['Here is your request boss',
                  'I have your order coming up',
                  'Nice pick, your download should be ready in a sec']
        series = random.choice(series)
        payload_sign = {
            "text": "" + series
        }

        post_request(url, payload, user_id)
        post_request(url, payload11, user_id)
        post_request(url, payload12, user_id)
        post_request(url, payload13, user_id)
        post_request(url, payload14, user_id)

        post_request(url, payload_sign, user_id)
        for index, row in new_df.iterrows():
            namemov= row['name']
            nametrail= namemov+ " official trailer"
            soup = BeautifulSoup(requests.get( "https://www.youtube.com/results?search_query=" + nametrail).content, "html.parser")
            times = ['1']
            stuff=[]
            for vid in soup.findAll( attrs={'class':'yt-uix-tile-link'} ):
                link_trail= 'https://www.youtube.com' + vid['href']
                stuff.append(link_trail)
            print(stuff)
            element2 = {
                "title": "" + namemov,
                "image_url": "" + str(row['image']),
                "subtitle": "" + str(row['desc']),
                "buttons": [
                    {
                        "type": "web_url",
                        "title": "Download",
                        "url": "" + str(row['first_link'])
                    }
                ]

            }
            elementtrail={
                "title": "" + namemov,
                "image_url": "" + str(row['image']),
                "subtitle": "" + str(row['desc']),
                "buttons": [
                    {
                        "type": "web_url",
                        "title": "Watch trailer",
                        "url": "" + str(stuff[0])
                    }
                ]

            }

            all_element.append(element2)
            all_element.append(elementtrail)
        data2 = all_element
        payload7 = {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "generic",
                    "elements": data2

                }
            }

        }
        post_request(url, payload7, user_id)

        post_request(url, payload2, user_id)
        return {
            "speech": "",
            "data": {
            },

            "source": "moviebot"

        }


    elif intent == "film request":
        parameters = result.get("parameters")
        download = parameters.get("Tv_show")
        movie = parameters.get("movie")
        if movie:
            file = pd.read_csv('movies_data.csv', encoding="ISO-8859-1")
            df = pd.DataFrame(file)
            new_df = df[df["name"] == movie]
            all_element = []
            rating = "5"
            user_id4 = str(user_id)
            strdownload = str(movie)
            sq="'"
            cur.execute(
                'INSERT INTO user_movies_rating (user_id,rating,movies) VALUES(' + user_id4 + ',' + rating + ',' +sq+ strdownload +sq+ ')')
            conn.commit()
            conn.close()
            series = ['Here is your request boss',
                      'I have your order coming up',
                      'I got it']
            series = random.choice(series)
            payload_sign = {
                "text": "" + series
            }

            post_request(url, payload_sign, user_id)
            for index, row in new_df.iterrows():
                element2 = {
                    "title": "" + row['name'],
                    "image_url": "" + str(row['image']),
                    "subtitle": "" + str(row['desc']),
                    "buttons": [
                        {
                            "type": "postback",
                            "title": "View",
                            "payload": "" + row['name']+" ##**##asdfghjkli"
                        }
                    ]

                }

                all_element.append(element2)
            data2 = all_element
            payload7 = {
                "attachment": {
                    "type": "template",
                    "payload": {
                        "template_type": "generic",
                        "elements": data2

                    }
                }

            }
            post_request(url, payload7, user_id)

        elif download:
            print('man')
            file = pd.read_csv('movie_data2.csv', encoding="ISO-8859-1")
            df = pd.DataFrame(file)
            new = df[df["name"] == download]
            edata = new.loc[~new['name'].duplicated()]
            t_data = edata.copy()
            all_element = []
            rating = "5"
            user_id4 = str(user_id)
            strdownload = str(download)
            sq="'"
            cur.execute(
                'INSERT INTO user_series_rating (user_id,rating,tv_series) VALUES(' + user_id4 + ',' + rating + ','+ sq+strdownload +sq+')')
            conn.commit()
            conn.close()
            series = ['Here is your request boss',
                      'I have your order coming up',
                      'I got it']
            series = random.choice(series)
            payload_sign = {
                "text": "" + series
            }

            post_request(url, payload_sign, user_id)
            for index, row in t_data.iterrows():

                element2 =  {
                                    "title": "" + row['name'],
                                    "image_url": "" + str(row['movie_image-src']),
                                    "subtitle": "" + str(row['desc']),
                                    "buttons": [
                                        {
                                            "type": "postback",
                                            "title": "View",
                                            "payload": "" + row['name'] + " f*123 x#123 v$456"
                                        }
                                    ]

                                }
                all_element.append(element2)
            data2 = all_element
            payload7 = {
                "attachment": {
                    "type": "template",
                    "payload": {
                        "template_type": "generic",
                        "elements": data2

                    }
                }

            }
            post_request(url, payload7, user_id)
            return {
                "speech": "",
                "data": {
                },

                "source": "moviebot"

            }




    elif intent == "Get Season":
        parameters = result.get("parameters")
        download = parameters.get("Tv_show")
        file = pd.read_csv('movie_data2.csv', encoding="ISO-8859-1")
        df = pd.DataFrame(file)
        new = df[df["name"].str.contains(download, na=False, case=False)]
        new_dt= new.loc[~new['season'].duplicated()]
        new_dt = new_dt.copy()
        season_data = new_dt.sort_values(['season'], ascending=[True])
        quick_data= []
        for index, row in season_data.iterrows():
            quick =  {
                    "content_type": "text",
                    "title": ""+row['season'],
                    "payload": ""+download+" "+row['season']
                }
            quick_data.append(quick)
        data = json.dumps(quick_data, indent=4)
        right= ['just feels right. Which season should I deliver to you', 'is a very interesting Tv Series \n What season should I get for you','is a nice pick. What season would you prefer right now']
        right= random.choice(right)
        payload = {
            "text": ""+download+" "+right,
            "quick_replies": data

        }
        post_request(url, payload, user_id)

    elif intent == "episodes":
        parameters = result.get("parameters")
        download = parameters.get("Tv_show")
        season = parameters.get("season")
        file = pd.read_csv('movie_data2.csv', encoding="ISO-8859-1")
        df = pd.DataFrame(file)
        rating = "5"
        user_id4 = str(user_id)
        strdownload = str(download)
        sq="'"
        cur.execute('INSERT INTO user_series_rating (user_id,rating,tv_series) VALUES(' + user_id4 + ',' + rating + ','+sq+ strdownload +sq+')')
        conn.commit()
        new = df[df["name"].str.contains(download, na=False, case=False)& df["season"].str.contains(season, na=False, case=False)]
        new_dt = new.loc[~new['episode_link'].duplicated()]
        new_dt = new_dt.copy()
        episode_data= new_dt.sort_values(['episode_link'], ascending=[True])
        payload = {
            "text": "For the Best experience on an Android device I would suggest follow this steps"
        }
        payload11 = {
            "text": "From the latest version of messenger \n Tap the avatar icon in the top right corner of your messenger home page"
        }

        payload12 = {
            "attachment": {
                "type": "image",
                "payload": {
                    "url": "https://lit-anchorage-95694.herokuapp.com/static/firstpart.png"
                }

            }
        }
        payload13 = {
            "text": "Then turn on Link open externally and you can now download from your favorite browser"
        }
        payload14 = {
            "attachment": {
                "type": "image",
                "payload": {
                    "url": "https://lit-anchorage-95694.herokuapp.com/static/secondpart.png"
                }

            }
        }


        payload2={
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "generic",
                    "elements": [
                        {
                            "title": "If you have download Issues Please click this Button",
                            "buttons": [
                                {
                                    "type": "postback",
                                    "title": "Download Issues",
                                    "payload": "Issues"
                                }
                            ]
                        }

                    ]
                }
            }
        }

        payload_sign = {
            "text": "Here are the episodes available right now \n I hope you find the one you are looking for"
        }
        post_request(url, payload, user_id)
        post_request(url, payload11, user_id)
        post_request(url, payload12, user_id)
        post_request(url, payload13, user_id)
        post_request(url, payload14, user_id)

        post_request(url, payload_sign, user_id)
        av_episode=[]
        times= ['1','2','3']
        for i in times:
            if episode_data.shape[0] > 10:
                first_ten= episode_data[: 10]
                episode_data= episode_data[ 10:]
                for index, row in first_ten.iterrows():
                    element = {
                        "title": "" + row['name'],
                        "image_url": "" + str(row['movie_image-src']),
                        "subtitle": "" + str(row['episode_link']),
                        "buttons": [
                            {
                                "type": "web_url",
                                "title": "Download",
                                "url": "" + str(row['first_Link-href'])
                            }
                        ]

                    }

                    av_episode.append(element)
                data = json.dumps(av_episode, indent=4)

                payload = {
                    "attachment": {
                        "type": "template",
                        "payload": {
                            "template_type": "generic",
                            "elements": data

                        }
                    }

                }


                post_request(url, payload, user_id)
                av_episode= []
            elif episode_data.shape[0] > 0 & episode_data.shape[0] < 10:
                first_ten = episode_data[: 10]
                episode_data = episode_data[10:]
                for index, row in first_ten.iterrows():
                    element = {
                        "title": "" + row['name'],
                        "image_url": "" + str(row['movie_image-src']),
                        "subtitle": "" + str(row['episode_link']),
                        "buttons": [
                            {
                                "type": "web_url",
                                "title": "Download",
                                "url": "" + str(row['first_Link-href'])
                            }
                        ]

                    }

                    av_episode.append(element)
                data = json.dumps(av_episode, indent=4)

                payload = {
                    "attachment": {
                        "type": "template",
                        "payload": {
                            "template_type": "generic",
                            "elements": data

                        }
                    }

                }

                post_request(url, payload, user_id)
                av_episode = []
        post_request(url, payload2, user_id)
        user_id4=str(user_id)
        strdownload=str(download)
        sq ="'"
        cur.execute('SELECT user_id,tv_series FROM series_sub WHERE user_id =' + user_id4 + ' AND tv_series =' +sq+ strdownload+sq)
        rows = cur.fetchall()
        count=0
        for rw in rows:
            count=count+1
        if count == 0:
            payload = {
                "text": "Would you like Updates on "+download+" I promise you won\'t be disappointed",
                "quick_replies": [
                    {
                        "content_type": "text",
                        "title": "Yes",
                        "payload": "subscribe "+download
                    },
                    {
                        "content_type": "text",
                        "title": "No",
                        "payload": "Dont send "+download
                    }
                ]
            }
            post_request(url, payload, user_id)
        return {
            "speech": "",
            "data": {
            },

            "source": "moviebot"

        }

    elif intent == "Issues":
        payload11 = {
            "text": "From the latest version of messenger \n Tap the avatar icon in the top right corner of your messenger home page"
        }

        payload12 = {
            "attachment": {
                "type": "image",
                "payload": {
                    "url": "https://lit-anchorage-95694.herokuapp.com/static/firstpart.png"
                }

            }
        }
        payload13 = {
            "text": "Then turn on Link open externally and you can now download from your favorite browser"
        }
        payload14 = {
            "attachment": {
                "type": "image",
                "payload": {
                    "url": "https://lit-anchorage-95694.herokuapp.com/static/secondpart.png"
                }

            }
        }

        payload = {
            "text": "If on a mobile device and you get a black screen instead of a prompt to open in your browser \nTap the play button to stream online or tap the top right button and select \"Open with Default Browser\" to start downloading in your default browser"
        }
        payload3 = {
            "text": "If you still get a black screen on your mobile device press and hold the play button or on the screen and you will get an option to save video. Select that option"
        }
        payload4= {
            "text": "If you get a black screen on a pc simply right click on play button and select Save as and your download will start"
        }
        post_request(url, payload11, user_id)
        post_request(url, payload12, user_id)
        post_request(url, payload13, user_id)
        post_request(url, payload14, user_id)
        post_request(url, payload, user_id)
        post_request(url, payload3, user_id)
        post_request(url, payload4, user_id)
        conn.close()

        return {
            "speech": "",
            "data": {
            },

            "source": "moviebot"

        }


    elif intent == "get genre":
        context= result.get("contexts")
        if context:
            print("shit")
            name=context[0].get("name")
            para = context[0].get("parameters")
            genre= para.get("genre")
            if name =="get_genre_dialog_params_film":
                payload = {
                    "text": "Should I get you "+genre+" Movies or "+genre+" Tv series?",
                    "quick_replies": [
                        {
                            "content_type": "text",
                            "title": "Movies",
                            "payload": ""+genre+" movies"
                        },
                        {
                            "content_type": "text",
                            "title": "Tv Series",
                            "payload": ""+genre+" tv series"
                        }
                    ]
                }
                return {
                    "speech": "",
                    "data": {
                        "facebook":payload
                    },

                    "source": "moviebot"

                }

        else:
            print("gosh")
            parameters = result.get("parameters")
            genre = parameters.get("genre")
            film = parameters.get("film")
            if film == "Tv Shows":
                file = pd.read_csv('movie_data2.csv', encoding="ISO-8859-1")
                df = pd.DataFrame(file)
                new = df[df["genres"].str.contains(genre, na=False, case=False)]
                episode_data = new.loc[~new['name'].duplicated()]
                episode_data = episode_data.copy()
                size = episode_data.shape[0]
                salute = u'\U0001F646'
                face = u'\U0001F62F'
                if size == 0:

                    payload_sign = {
                        "text": "" + face + " I am really sorry. I couldn\'t find those " + genre + " " + film + " " + "you wanted" + salute
                    }
                    payload = {
                        "text": "I have got a better idea why not request for another genre. \nI bet I would be able to get it for you " + salute
                    }
                    post_request(url, payload_sign, user_id)
                    post_request(url, payload, user_id)
                else:
                    if size > 30:
                        size = size - 5
                    episode_data = episode_data.ix[np.random.choice(episode_data.index, size, replace=False)]

                    payload_sign = {
                        "text": "Here are the " + genre + " " + film + " you requested for boss " + salute
                    }
                    post_request(url, payload_sign, user_id)
                    available = []
                    times = ['1', '2', '3']
                    for i in times:
                        if episode_data.shape[0] > 10:
                            first_ten = episode_data[: 10]
                            episode_data = episode_data[10:]
                            for index, row in first_ten.iterrows():
                                element = {
                                    "title": "" + row['name'],
                                    "image_url": "" + str(row['movie_image-src']),
                                    "subtitle": "" + str(row['desc']),
                                    "buttons": [
                                        {
                                            "type": "postback",
                                            "title": "View",
                                            "payload": "" + row['name'] + " f*123 x#123 v$456"
                                        }
                                    ]

                                }

                                available.append(element)
                            data = json.dumps(available, indent=4)

                            payload = {
                                "attachment": {
                                    "type": "template",
                                    "payload": {
                                        "template_type": "generic",
                                        "elements": data

                                    }
                                }

                            }

                            post_request(url, payload, user_id)
                            available = []
                        elif episode_data.shape[0] > 0 & episode_data.shape[0] < 10:
                            first_ten = episode_data[: 10]
                            episode_data = episode_data[10:]
                            for index, row in first_ten.iterrows():
                                element = {
                                    "title": "" + row['name'],
                                    "image_url": "" + str(row['movie_image-src']),
                                    "subtitle": "" + str(row['desc']),
                                    "buttons": [
                                        {
                                            "type": "postback",
                                            "title": "View",
                                            "payload": "" + row['name'] + " f*123 x#123 v$456"
                                        }
                                    ]

                                }

                                available.append(element)
                            data = json.dumps(available, indent=4)

                            payload = {
                                "attachment": {
                                    "type": "template",
                                    "payload": {
                                        "template_type": "generic",
                                        "elements": data

                                    }
                                }

                            }

                            post_request(url, payload, user_id)
                            available = []
            elif film == "Movies":
                file = pd.read_csv('movies_data.csv', encoding="ISO-8859-1")
                df = pd.DataFrame(file)
                new = df[df["genre1"].str.contains(genre, na=False, case=False) | df["genre2"].str.contains(genre, na=False, case=False) | df["genre3"].str.contains(genre, na=False, case=False) | df["genre4"].str.contains(genre, na=False, case=False)]
                episode_data = new.loc[~new['name'].duplicated()]
                episode_data = episode_data.copy()
                size = episode_data.shape[0]
                salute = u'\U0001F646'
                face = u'\U0001F62F'
                if size == 0:

                    payload_sign = {
                        "text": ""+face+" I am really sorry. I couldn\'t find those "+genre+" "+film+" "+"you wanted"+ salute
                    }
                    payload = {
                        "text": "I have got a better idea why not request for another genre. \nI bet I would be able to get it for you "+ salute
                    }
                    post_request(url, payload_sign, user_id)
                    post_request(url, payload, user_id)
                else:
                    if size > 30:
                        size= size - 5
                    episode_data = episode_data.ix[np.random.choice(episode_data.index, size, replace=False)]


                    payload_sign = {
                        "text": "Here are the "+genre+" "+film+" you requested for boss "+salute
                    }
                    post_request(url, payload_sign, user_id)
                    available=[]
                    times= ['1','2','3']
                    for i in times:
                        if episode_data.shape[0] > 10:
                            first_ten= episode_data[: 10]
                            episode_data= episode_data[ 10:]
                            for index, row in first_ten.iterrows():
                                element = {
                                    "title": "" + row['name'],
                                    "image_url": "" + str(row['image']),
                                    "subtitle": "" + str(row['desc']),
                                    "buttons": [
                                        {
                                            "type": "postback",
                                            "title": "View",
                                            "payload": "" + row['name']+" ##**##asdfghjkli"
                                        }
                                    ]

                                }

                                available.append(element)
                            data = json.dumps(available, indent=4)

                            payload = {
                                "attachment": {
                                    "type": "template",
                                    "payload": {
                                        "template_type": "generic",
                                        "elements": data

                                    }
                                }

                            }

                            post_request(url, payload, user_id)
                            available= []
                        elif episode_data.shape[0] > 0 & episode_data.shape[0] < 10:
                            first_ten = episode_data[: 10]
                            episode_data = episode_data[10:]
                            for index, row in first_ten.iterrows():
                                element = {
                                    "title": "" + row['name'],
                                    "image_url": "" + str(row['image']),
                                    "subtitle": "" + str(row['desc']),
                                    "buttons": [
                                        {
                                            "type": "postback",
                                            "title": "View",
                                            "payload": "" + row['name']+" ##**##asdfghjkli"
                                        }
                                    ]

                                }

                                available.append(element)
                            data = json.dumps(available, indent=4)

                            payload = {
                                "attachment": {
                                    "type": "template",
                                    "payload": {
                                        "template_type": "generic",
                                        "elements": data

                                    }
                                }

                            }

                            post_request(url, payload, user_id)
                            available = []
            return {
                "speech": "",
                "data": {
                },

                "source": "moviebot"

            }

    elif intent == "subscribe to updates":
        parameters = result.get("parameters")
        download = parameters.get("Tv_show")
        user_id4 = str(user_id)
        strdownload = str(download)
        sq="'"
        cur.execute('INSERT INTO series_sub (user_id,tv_series) VALUES(' + user_id4 + ',' +sq+ strdownload +sq+ ')')
        conn.commit()
        conn.close()
    elif intent == "stop updates":
        parameters = result.get("parameters")
        download = parameters.get("Tv_show")
        user_id4 = str(user_id)
        strdownload = str(download)
        sq="'"
        cur.execute('DELETE from series_sub WHERE user_id =' + user_id4 + ' AND tv_series =' + sq+strdownload+sq )
        conn.commit()
        conn.close()
        element = {
            "text": "No problem. You won\'t receive " + download +" updates anymore",
        }
        post_request(url, element, user_id)



    elif intent == "latest":
        parameters = result.get("parameters")
        download = parameters.get("Tv_show")
        file = pd.read_csv('movie_data2.csv', encoding="ISO-8859-1")
        file = pd.DataFrame(file)
        new = file[file.name == download]
        season_data = new.sort_values(['season', 'episode_link'], ascending=[True, True])
        data = season_data.tail(1)
        all_element=[]
        for index, row in data.iterrows():
            element = {
                "title": "" + row['name'],
                "image_url": "" + row['movie_image-src'],
                "subtitle": ""+row['season']+"  " + row['episode_link'],
                "buttons": [
                    {
                        "type": "postback",
                        "title": "Download",
                        "payload": "" + row['name']
                    }
                ]

            }

            all_element.append(element)
        data= json.dumps(all_element, indent=4)
        payload = {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "generic",
                    "elements": data

                }
            }

        }

        post_request(url, payload, user_id)


    elif intent == "info":
        parameters = result.get("parameters")
        download = parameters.get("Tv_show")
        download_mov = parameters.get("movie")
        if not download_mov:
            file = pd.read_csv('movie_data2.csv', encoding="ISO-8859-1")
            file = pd.DataFrame(file)
            new = file[file.name == download]
            new = new.head(1)
            for index, row in new.iterrows():
                desc = row['desc']
            element = {
                "text": "" + desc,
            }

            post_request(url, element, user_id)
        else:
            file = pd.read_csv('movies_data.csv', encoding="ISO-8859-1")
            file = pd.DataFrame(file)
            new = file[file.name == download_mov]
            new = new.head(1)
            for index, row in new.iterrows():
                desc = row['desc']
            element = {
                "text": "" + desc,
            }

            post_request(url, element, user_id)
    elif intent == "cast movie":
        parameters = result.get("parameters")
        movie = parameters.get("movie")
        file = pd.read_csv('movies_data.csv', encoding="ISO-8859-1")
        file = pd.DataFrame(file)
        new = file[file.name == movie]
        new = new.head(1)
        for index, row in new.iterrows():
            cast = row['casts']
        element = {
                "text": "" + cast,
        }

        post_request(url, element, user_id)
    elif intent == "cast":
        parameters = result.get("parameters")
        download = parameters.get("Tv_show")
        file = pd.read_csv('movie_data2.csv', encoding="ISO-8859-1")
        file = pd.DataFrame(file)
        new = file[file.name == download]
        new = new.head(1)
        for index, row in new.iterrows():
            cast = row['casts']
        element = {
                "text": "" + cast,
        }
        post_request(url, element, user_id)

    elif intent == "movie year":
        parameters = result.get("parameters")
        year = parameters.get("year")
        file = pd.read_csv('movies_data.csv', encoding="ISO-8859-1")
        df = pd.DataFrame(file)
        new = df[df["year"] == year]
        size = new.shape[0]
        salute = u'\U0001F646'
        face = u'\U0001F62F'
        if size == 0:
            payload_sign = {
                "text": "" + face + " I am really sorry. I couldn\'t find those " + year + " movies you wanted" + salute
            }
            payload = {
                "text": "I have got a better idea why not request for another year. \nI bet I would be able to get it for you " + salute
            }
            post_request(url, payload_sign, user_id)
            post_request(url, payload, user_id)
        else:
            if size > 30:
                new= new.iloc[:30,:]
                size = 30
            new = new.ix[np.random.choice(new.index, size, replace=False)]

            payload_sign = {
                "text": "Here are the " + year + " movies you requested for boss " + salute
            }
            post_request(url, payload_sign, user_id)
            available = []
            times = ['1', '2', '3']
            for i in times:
                if new.shape[0] > 10:
                    first_ten = new[: 10]
                    new = new[10:]
                    for index, row in first_ten.iterrows():
                        element = {
                            "title": "" + row['name'],
                            "image_url": "" + str(row['image']),
                            "subtitle": "" + str(row['desc']),
                            "buttons": [
                                {
                                    "type": "postback",
                                    "title": "View",
                                    "payload": "" + row['name']+" ##**##asdfghjkli"
                                }
                            ]

                        }

                        available.append(element)
                    data = json.dumps(available, indent=4)

                    payload = {
                        "attachment": {
                            "type": "template",
                            "payload": {
                                "template_type": "generic",
                                "elements": data

                            }
                        }

                    }

                    post_request(url, payload, user_id)
                    available = []
                elif new.shape[0] > 0 & new.shape[0] <= 10:
                    first_ten = new[: 10]
                    new = new[10:]
                    for index, row in first_ten.iterrows():
                        element = {
                            "title": "" + row['name'],
                            "image_url": "" + str(row['image']),
                            "subtitle": "" + str(row['desc']),
                            "buttons": [
                                {
                                    "type": "postback",
                                    "title": "View",
                                    "payload": "" + row['name']+" ##**##asdfghjkli"
                                }
                            ]

                        }

                        available.append(element)
                    data = json.dumps(available, indent=4)

                    payload = {
                        "attachment": {
                            "type": "template",
                            "payload": {
                                "template_type": "generic",
                                "elements": data

                            }
                        }

                    }

                    post_request(url, payload, user_id)
        return {
            "speech": "",
            "data": {
            },

            "source": "moviebot"

        }
    elif intent == "actors movie":
        parameters = result.get("parameters")
        actor = parameters.get("actor")
        file = pd.read_csv('movie_data2.csv', encoding="ISO-8859-1")
        file = pd.DataFrame(file)
        new = file[file["casts"].str.contains(actor, na=False, case=False)]
        data = new.loc[~new['name'].duplicated()]
        data = data.copy()
        size = data.shape[0]
        if size > 10:
            df = data.ix[np.random.choice(data.index, 10, replace=False)]
            all_element = []
            for index, row in df.iterrows():
                element = {
                    "title": "" + row['movie'],
                    "image_url": "" + row['movie_image-src'],
                    "subtitle": "" + row['desc'],
                    "buttons": [
                        {
                            "type": "postback",
                            "title": "View",
                            "payload": "" + row['movie'] + " f*123 x#123 v$456"
                        }
                    ]

                }

                all_element.append(element)
            data = json.dumps(all_element, indent=4)
        else:
            df = data.ix[np.random.choice(data.index, size, replace=False)]
            all_element = []
            for index, row in df.iterrows():
                element = {
                    "title": "" + row['movie'],
                    "image_url": "" + row['movie_image-src'],
                    "subtitle": "" + row['desc'],
                    "buttons": [
                        {
                            "type": "postback",
                            "title": "View",
                            "payload": "" + row['movie'] + " f*123 x#123 v$456"
                        }
                    ]

                }

                all_element.append(element)
            data = json.dumps(all_element, indent=4)
        payload = {

            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "generic",
                    "elements": data

                }
            }

        }
        post_request(url, payload, user_id)

    elif intent == "latest movies":
        file = pd.read_csv('movies_data.csv', encoding="ISO-8859-1")
        df = pd.DataFrame(file)
        new = df.sort_values(['year'], ascending= False)
        new = new.iloc[:30, :]
        size = new.shape[0]
        salute = u'\U0001F646'
        face = u'\U0001F62F'
        if size == 0:
            payload_sign = {
                "text": "" + face + " I am really sorry. I couldn\'t find those latest movies you wanted" + salute
            }
            payload = {
                "text": "I have got a better idea why not request for another year. \nI bet I would be able to get it for you " + salute
            }
            post_request(url, payload_sign, user_id)
            post_request(url, payload, user_id)
        else:
            if size > 30:
                new= new.iloc[:30,:]

            payload_sign = {
                "text": "Here are the latest movies you requested for"
            }
            post_request(url, payload_sign, user_id)
            available = []
            times = ['1', '2', '3']
            for i in times:
                if new.shape[0] > 10:
                    first_ten = new[: 10]
                    new = new[10:]
                    for index, row in first_ten.iterrows():
                        element = {
                            "title": "" + row['name'],
                            "image_url": "" + str(row['image']),
                            "subtitle": "" + str(row['desc']),
                            "buttons": [
                                {
                                    "type": "postback",
                                    "title": "View",
                                    "payload": "" + row['name']+" ##**##asdfghjkli"
                                }
                            ]

                        }

                        available.append(element)
                    data = json.dumps(available, indent=4)

                    payload = {
                        "attachment": {
                            "type": "template",
                            "payload": {
                                "template_type": "generic",
                                "elements": data

                            }
                        }

                    }

                    post_request(url, payload, user_id)
                    available = []
                elif new.shape[0] > 0 & new.shape[0] <= 10:
                    first_ten = new[: 10]
                    new = new[10:]
                    for index, row in first_ten.iterrows():
                        element = {
                            "title": "" + row['name'],
                            "image_url": "" + str(row['image']),
                            "subtitle": "" + str(row['desc']),
                            "buttons": [
                                {
                                    "type": "postback",
                                    "title": "View",
                                    "payload": "" + row['name']+" ##**##asdfghjkli"
                                }
                            ]

                        }

                        available.append(element)
                    data = json.dumps(available, indent=4)

                    payload = {
                        "attachment": {
                            "type": "template",
                            "payload": {
                                "template_type": "generic",
                                "elements": data

                            }
                        }

                    }

                    post_request(url, payload, user_id)
        return {
            "speech": "",
            "data": {
            },

            "source": "moviebot"

        }


    elif intent == "good ms":
        parameters = result.get("parameters")
        download = parameters.get("Tv_show")
        season = parameters.get("season")
        episode = parameters.get("episode")
        file = pd.read_csv('movie_data2.csv', encoding="ISO-8859-1")
        file = pd.DataFrame(file)
        new = file[file["name"].str.contains(download, na=False, case=False) & file["season"].str.contains(season, na=False,
                                                                                                           case=False) & file["episode_link"].str.contains(episode, na=False,case=False) ]
        sgt = list(new.index.values)
        str1 = sgt[0]
        desc = new.loc[str1, 'desc']
        season = new.loc[str1, 'season']
        name = new.loc[str1, 'name']
        episode = new.loc[str1, 'episode_link']
        mp4 = new.loc[str1, 'mp4_link-href']
        threegp = new.loc[str1, '3gp_link-href']
        img = new.loc[str1, 'movie_image-src']
        speech = "hmmm"

        print("Response:")
        print(speech)

        facebook_message = {
        "attachment":{
          "type":"template",
          "payload":{
            "template_type":"button",
            "text":"What do you want to do next?",
            "buttons":[
              {
                "type":"web_url",
                "url":"https://petersapparel.parseapp.com",
                "title":"Show Website"
              },
              {
                  "type": "web_url",
                  "url": "https://petersapparel.parseapp.com",
                  "title": "ok"
              }
            ]
          }
        }
      }


        return {
            "speech": speech,
            "displayText": speech,
            "data": {"facebook": facebook_message},
            "contextOut": [],
            "source": "moviebot"
         }


def post_request(url, payload, user_id):
    data_payload = {
            "recipient": {
                "id": user_id
            },
            "message": payload

    }

    headers = {'Content-type': 'application/json'}
    requests.post(url, data=json.dumps(data_payload), headers=headers)

@app.route('/greeting/')
def greeting():
    like = '(y)'
    token = "EAAOADUqeP70BAJCjjmZBd7zz4kRXT5Ywz0j1VUnDZAXTU74Gi3Uro5pNe5r5Q5sVaYC5sDQuFdVaybLR47NCgecWsANXhnA8dVqddnf3hdGg8HEJZCbgU4sixStPvqlZCWyQZCgpDD3U3S7YJg7cHZBEBvcePopwdUNBeQx5JaZBgZDZD"
    once = {
        "setting_type": "greeting",
        "greeting": [
            {
                "locale": "default",
                "text": "Hello!"
            }, {
                "locale": "en_US",
                "text": "Hello {{user_first_name}}! tap the button to enter the world of amazing entertainment.\nSee you there"
            }
        ]
    }
    del_msg = {
        "setting_type": "greeting"
    }

    url8 = "https://graph.facebook.com/v2.6/me/messenger_profile?access_token=" + token
    headers = {'Content-type': 'application/json'}
    requests.post(url8, data=json.dumps(once), headers=headers)
    return "it rocks"


@app.route('/sunday/')
def sundaynot():
    token = "EAAOADUqeP70BAJCjjmZBd7zz4kRXT5Ywz0j1VUnDZAXTU74Gi3Uro5pNe5r5Q5sVaYC5sDQuFdVaybLR47NCgecWsANXhnA8dVqddnf3hdGg8HEJZCbgU4sixStPvqlZCWyQZCgpDD3U3S7YJg7cHZBEBvcePopwdUNBeQx5JaZBgZDZD"
    url2 = "https://graph.facebook.com/v2.6/me/messages?access_token=" + token
    url = urlparse(os.environ["DATABASE_URL"])

    conn = psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
    )

    cur = conn.cursor()

    like = '(y)'
    file = pd.read_csv('sunday.csv', encoding="ISO-8859-1")
    df = pd.DataFrame(file)
    df = df.ix[np.random.choice(df.index, 10, replace=False)]
    cur.execute('SELECT DISTINCT ON (user_id) user_id FROM user_data')
    rows = cur.fetchall()
    for rw in rows:
        user_id= rw[0]
        all_element = []
        for index, row in df.iterrows():
            element = {
                "title": "" + row['name'],
                "image_url": "" + row['image'],
                "subtitle": "" + row['desc'],
                "buttons": [
                    {
                        "type": "postback",
                        "title": "View",
                        "payload": "" + row['name']+" ##**##asdfghjkli"
                    }
                ]

            }

            all_element.append(element)
        data = json.dumps(all_element, indent=4)

        payload_sign = {
            "text": "Get together with the family today and enjoy some family drama. I have some movies for you " +like
        }

        payload = {

            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "generic",
                    "elements": data

                }
            }

        }

        post_request4(url2, payload_sign, user_id)
        post_request4(url2, payload, user_id)

        return "bro thats it"

def post_request4(url2, payload, user_id):

    data_payload = {
         "recipient": {
              "id": user_id
                },
            "message": payload

         }

    headers = {'Content-type': 'application/json'}
    requests.post(url2, data=json.dumps(data_payload), headers=headers)




@app.route('/user')
def notification():
    url = urlparse(os.environ["DATABASE_URL"])

    conn = psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
    )
    cur = conn.cursor()
    token = "EAAOADUqeP70BAJCjjmZBd7zz4kRXT5Ywz0j1VUnDZAXTU74Gi3Uro5pNe5r5Q5sVaYC5sDQuFdVaybLR47NCgecWsANXhnA8dVqddnf3hdGg8HEJZCbgU4sixStPvqlZCWyQZCgpDD3U3S7YJg7cHZBEBvcePopwdUNBeQx5JaZBgZDZD"
    url = "https://graph.facebook.com/v2.6/me/messages?access_token=" + token
    file = pd.read_csv('series_update.csv')
    df = pd.DataFrame(file)
    for index, row in df.iterrows():
        movie= row["name"]
        print(movie)
        image = row['movie_image-src']
        episode= row['episode_link']
        season = row['season']
        link = row['first_Link-href']
        strdownload = str(movie)
        sq="'"
        cur.execute('SELECT user_id,tv_series FROM series_sub WHERE tv_series =' + sq+strdownload+sq)
        new = cur.fetchall()
        for row in new:
            user_id = row[0]
            print(user_id)
            print(movie)
            payload2 = {
                "text": "Hey I have some "+movie+" update for you "
            }

            payload = {
                "attachment": {
                  "type": "template",
                  "payload": {
                  "template_type": "generic",
                "elements":[ {
                "title": "" + movie,
                "image_url": "" + image,
                "subtitle": ""+season+"  " + episode,
                "buttons": [
                    {
                        "type": "web_url",
                        "title": "Download",
                        "url": "" + link
                    },
                    {
                        "type": "postback",
                        "title": "Stop Updates",
                        "payload": "Unsuscribe to " + movie
                    }
                ]
                }
                      ]
                }
                }
            }

            print(payload)
            post_request2(url, payload2, user_id)
            post_request2(url, payload, user_id)
    return "Notifications sent"


def post_request2(url, payload, user_id):
    data_payload = {
            "recipient": {
                "id": user_id
            },
            "message": payload

    }

    headers = {'Content-type': 'application/json'}
    requests.post(url, data=json.dumps(data_payload), headers=headers)
    print("bro")
@app.route('/datashow/')
def datashow():
    url = urlparse(os.environ["DATABASE_URL"])

    conn = psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
    )

    cur = conn.cursor()
    cur.execute('SELECT user_id,tv_series FROM series_sub ')
    rows = cur.fetchall()
    for rt in rows:
        print("user_sub_data")
        print(rt[0])
        print(rt[1])
    cur.execute('SELECT user_id,rating,tv_series FROM user_series_rating')
    rows = cur.fetchall()
    for rt in rows:
        print("user_series_data")
        print(rt[0])
        print(rt[1])
        print(rt[2])
    cur.execute('SELECT user_id,rating,movies FROM user_movies_rating')
    rows = cur.fetchall()
    for rt in rows:
        print("user_movies_data")
        print(rt[0])
        print(rt[1])
        print(rt[2])
    cur.execute('SELECT user_id FROM user_data')
    rows = cur.fetchall()
    for rt in rows:
        print("user_data")
        print(rt[0])

    return "it rocks"
@app.route('/createtable/')
def dbcreate():

    url = urlparse(os.environ["DATABASE_URL"])

    conn = psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
    )

    cur = conn.cursor()
    cur.execute('''CREATE TABLE user_data ( id SERIAL PRIMARY KEY NOT NULL, user_id BIGINT NOT NULL);''')
    cur.execute(
        '''CREATE TABLE series_sub ( id SERIAL PRIMARY KEY NOT NULL, user_id BIGINT NOT NULL, tv_series VARCHAR(1000) NOT NULL);''')
    cur.execute(
        '''CREATE TABLE user_movies_rating ( id SERIAL PRIMARY KEY NOT NULL, user_id BIGINT NOT NULL, rating INT NOT NULL, movies VARCHAR(1000) NOT NULL);''')
    cur.execute(
        '''CREATE TABLE user_series_rating ( id SERIAL PRIMARY KEY NOT NULL, user_id BIGINT NOT NULL, rating INT NOT NULL, tv_series VARCHAR(1000) NOT NULL);''')

    conn.commit()
    conn.close()
    return  "bro i got it"

@app.route('/gentvupdate/')
def gen_tv_update():
    token = "EAAOADUqeP70BAJCjjmZBd7zz4kRXT5Ywz0j1VUnDZAXTU74Gi3Uro5pNe5r5Q5sVaYC5sDQuFdVaybLR47NCgecWsANXhnA8dVqddnf3hdGg8HEJZCbgU4sixStPvqlZCWyQZCgpDD3U3S7YJg7cHZBEBvcePopwdUNBeQx5JaZBgZDZD"
    url3 = "https://graph.facebook.com/v2.6/me/messages?access_token=" + token
    url = urlparse(os.environ["DATABASE_URL"])

    conn = psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
    )

    cur = conn.cursor()

    like = '(y)'
    file = pd.read_csv('gen_tv_update.csv', encoding="ISO-8859-1")
    df = pd.DataFrame(file)
    df = df.ix[np.random.choice(df.index, 1, replace=False)]
    cur.execute('SELECT user_id FROM user_data')
    rows = cur.fetchall()
    rows = pd.DataFrame(rows)
    print("start")
    all_element = []
    for index, row in df.iterrows():
        print("df1")
        element = {
            "title": "" + row['name'],
            "image_url": "" + row['movie_image-src'],
            "subtitle": "" + row['season']+" "+row['episode_link'],
            "buttons": [
                {
                    "type": "web_url",
                    "url": "" + row['first_Link-href'],
                    "title": "Download"
                }
            ]

        }

        all_element.append(element)
    data = json.dumps(all_element, indent=4)
    payload_sign = {
        "text": "Just thought you might care. A new Episode of Originals is out and I got it for you " + like
    }

    payload10 = {
        "text": "For the Best experience on an Android device I would suggest follow this steps"
    }
    payload11 = {
        "text": "From the latest version of messenger \n Tap the avatar icon in the top right corner of your messenger home page"
    }

    payload12 = {
        "attachment": {
            "type": "image",
            "payload": {
                "url": "https://lit-anchorage-95694.herokuapp.com/static/firstpart.png"
            }

        }
    }
    payload13 = {
        "text": "Then turn on Link open externally and you can now download from your favorite browser"
    }
    payload14 = {
        "attachment": {
            "type": "image",
            "payload": {
                "url": "https://lit-anchorage-95694.herokuapp.com/static/secondpart.png"
            }

        }
    }

    payload = {

        "attachment": {
            "type": "template",
            "payload": {
                "template_type": "generic",
                "elements": data

            }
        }

    }
    print("bro")
    data4 = rows.loc[~rows[0].duplicated()]
    data4 = data4.copy()
    for index, rw in data4.iterrows():
        user_id= rw[0]
        user_id=str(user_id)
        print(user_id)
        post_request10(url3, payload_sign, user_id)
        post_request10(url3, payload, user_id)
        post_request10(url3, payload10, user_id)
        post_request10(url3, payload11, user_id)
        post_request10(url3, payload12, user_id)
        post_request10(url3, payload13, user_id)
        post_request10(url3, payload14, user_id)

        print("bro")

    return "bro thats it"


def post_request10(url3, payload, user_id):
    data_payload = {
    "recipient": {
             "id": user_id
        },
     "message": payload

    }

    headers = {'Content-type': 'application/json'}
    requests.post(url3, data=json.dumps(data_payload), headers=headers)

@app.route('/persmenu/')
def menu():
    url9="https://graph.facebook.com/v2.6/me/messenger_profile?access_token=EAAOADUqeP70BAJCjjmZBd7zz4kRXT5Ywz0j1VUnDZAXTU74Gi3Uro5pNe5r5Q5sVaYC5sDQuFdVaybLR47NCgecWsANXhnA8dVqddnf3hdGg8HEJZCbgU4sixStPvqlZCWyQZCgpDD3U3S7YJg7cHZBEBvcePopwdUNBeQx5JaZBgZDZD"
    payload={
  "persistent_menu":[
    {
      "locale":"default",
      "composer_input_disabled":True,
      "call_to_actions":[
          {
              "type": "postback",
              "title": "Request a movie",
              "payload": "Request a movie",

          },
          {
              "type": "postback",
              "title": "Request a Tv series",
              "payload": "Request a Tv series",

          },
        {
          "title":"More",
          "type":"nested",
          "call_to_actions":[
            {
              "title":"Request movie genre",
              "type":"postback",
              "payload":"Request movie genre"
            },
            {
                "title": "Request tv series genre",
                "type": "postback",
                "payload": "Request tv series genre"
            },
            {
                  "title": "Movie of a certain year",
                  "type": "postback",
                  "payload": "Movie of a certain year"
            },
              {
                  "type": "web_url",
                  "title": "Get Help",
                  "url": "https://murmuring-mountain-66302.herokuapp.com/help/index.html",
                  "webview_height_ratio": "full"
              }
          ]
        }
      ]
    },
    {
      "locale":"zh_CN",
      "composer_input_disabled":False
    }
  ]
}
    headers = {'Content-type': 'application/json'}
    requests.post(url9, data=json.dumps(payload), headers=headers)
    return "The boss"

@app.route('/started/')
def started():
    url4 = "https://graph.facebook.com/v2.6/me/messenger_profile?access_token=EAAOADUqeP70BAJCjjmZBd7zz4kRXT5Ywz0j1VUnDZAXTU74Gi3Uro5pNe5r5Q5sVaYC5sDQuFdVaybLR47NCgecWsANXhnA8dVqddnf3hdGg8HEJZCbgU4sixStPvqlZCWyQZCgpDD3U3S7YJg7cHZBEBvcePopwdUNBeQx5JaZBgZDZD"

    payload={
  "get_started":{
    "payload":"GET_STARTED_PAYLOAD"
  }
}

if __name__ == "__main__":
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')

