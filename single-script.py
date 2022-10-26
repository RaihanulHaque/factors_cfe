import json
import base64
import requests
from datetime import datetime, timedelta
import random


def authenticate():
    user = "Rahi"
    password = "t5nC 34nz obVc BUzM c1Nt KQnK"
    creds = user + ':' + password
    cred_token = base64.b64encode(creds.encode())
    header = {'Authorization': 'Basic ' + cred_token.decode('utf-8')}
    return header

def image_upload(path):
    header = authenticate()
    url = 'https://calculator4engineers.com/wp-json/wp/v2'
    media = {'file': open(path, 'rb')}
    image = requests.post(url+'/media', headers=header, files=media)
    post_id = json.loads(image.content.decode('utf-8'))['id']
    image_link = image.json()['guid']['rendered']
    locString = f"<!-- wp:image {{\"id\":{str(post_id)},\"sizeSlug\":\"full\",\"linkDestination\":\"none\" }} -->"
    locString += f"<figure class=\"wp-block-image size-full\"><img src=\"{image_link}\" alt=\"\" class=\"wp-image-{str(post_id)}\"/></figure>"
    locString += "<!-- /wp:image -->"
    code = locString
    print(image_link)
    return code


def wp_paragraph(text):
    return f"<!-- wp:paragraph -->{text}<!-- /wp:paragraph -->"


def wp_heading(text):
    return f"<!-- wp:heading -->{text}<!-- /wp:heading -->"


def schedule(current_time):
    # tdelta = timedelta(minutes=random.randrange(3, 9))
    # current_time = current_time + tdelta
    hour = str(current_time.hour)
    minute = str(current_time.minute)
    second = str(current_time.second)
    if len(hour) == 1:
        hour = f"0{hour}"
    if len(minute) == 1:
        minute = f"0{minute}"
    if len(second) == 1:
        second = f"0{second}"
    return f"{current_time.date()}T{hour}:{minute}:{second}"


# Math
# user = "WP SEO Geeks"
# password = "e4gB PSHR pLnB qLFL SFDz ITmO"
# Physicsmaniac
# user = "Rahi_"
# password = "rbId ChMZ bHPk 1aFL ibOX 1mwc"

header = authenticate()
url = 'https://calculator4engineers.com/wp-json/wp/v2'
# current_time = datetime.now()
posttitle = "Automation test 101"
# postslug = "automation_test_101"
postcontent = "This post is created by python script for testing purpose"
content = "Baka<h2>Rahi</h2><a href="'#'">Baka</a>"
content += image_upload("images/anime.jpg")
# for i in range(0, 5):
# tdelta = timedelta(minutes=random.randrange(2, 6))
# current_time = current_time + tdelta
# time = schedule(current_time)
# print(time)
post = {
    'title': posttitle,
    # 'slug': postslug,
    'content': content,
    'status': 'publish',
    # 'author':'235',
    'publish': 'standard',
    # 'date': "2022-10-04T09:59:00",
    # 'date': time,
    # 'date': f"{current_time.date()}T{current_time.hour}:{current_time.minute}:{current_time.second}",
    'categories': '3'
    # 'featured_media': '542'
}
# media = {
#  "file": open(f"images/100_banner_simple.jpg", "rb"),
#  "caption": "caption",
#  "description": "description",
#  "alt_text": "Custom Alt Text",
#  }
# upload_image = requests.post(url + "/media", headers=header, files=media)

wprequest = requests.post(url + '/posts', headers=header, json=post)
print(wprequest)
