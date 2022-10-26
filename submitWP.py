import json
import base64
import requests
import random


def authenticate():
    user = "Rahi"
    password = "t5nC 34nz obVc BUzM c1Nt KQnK"
    creds = user + ':' + password
    cred_token = base64.b64encode(creds.encode())
    header = {'Authorization': 'Basic ' + cred_token.decode('utf-8')}
    return header


def featured_image_upload(image_list):
    url = 'https://calculator4engineers.com/wp-json/wp/v2'
    header = authenticate()
    path = random.choice(image_list)
    media = {'file': open(path, 'rb')}
    image = requests.post(url+'/media', headers=header, files=media)
    post_id = json.loads(image.content.decode('utf-8'))['id']
    return str(post_id)


def submit(posttitle, n, content, time, bannerImages):
    header = authenticate()
    url = 'https://calculator4engineers.com/wp-json/wp/v2'

    post = {
        'title': posttitle,
        'slug': f"{n}",
        'author': random.choice(['1', '2', '4', '5', '6']),
        'content': content,
        'status': 'publish',
        'date': time,
        'publish': 'standard',
        'categories': '4',
        'featured_media': featured_image_upload(bannerImages)
    }
    wprequest = requests.post(url + '/posts', headers=header, json=post)
    return wprequest
