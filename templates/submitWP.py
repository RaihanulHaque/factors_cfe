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


def submit(posttitle, content):
    header = authenticate()
    url = 'https://calculator4engineers.com/wp-json/wp/v2'

    post = {
        'title': posttitle,
        # 'slug': f"prime-factorization-of-{n}",
        # 'author': random.choice(['1', '2', '4', '5', '6']),
        'content': content,
        'status': 'publish',
        # 'date': time,
        'publish': 'standard',
        'categories': '4'
    }
    wprequest = requests.post(url + '/posts', headers=header, json=post)
    return wprequest
