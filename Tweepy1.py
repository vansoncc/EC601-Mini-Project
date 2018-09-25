# Import part
import json
import tweepy
import os
import wget 
import subprocess
import ffmpeg
import io
import PIL
from os import listdir
from google.cloud import vision
from google.cloud.vision import types
from  PIL import ImageDraw, Image, ImageFont

#Provide the Twitter key and token
consumer_key = ''
consumer_secret = ''
access_token = ''
access_token_secret = ''

#The Image save path
image_path=os.chdir('/Users/vanson/downloads/boston university/EC601/API')

#Set the Json File
os.environ['GOOGLE_APPLICATION_CREDENTIALS']= "My_First.json"

#Set the label text size and font
FONT_PATH = os.environ.get("FONT_PATH", "/Library/Fonts/Times New Roman.ttf")

#Tweepy Authority process
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)
# for tweet in public_tweets:
#     print(tweet.text)



#Using the Tweepy to download image
def download_tweets(source):
    Twitter_Page = api.user_timeline(screen_name =source, count=200)
    Twitter_with_image=set()
    print('Downloading the Image from '+ source)
    print('Processing.....')
    for status in Twitter_Page:
        media = status.entities.get('media', [])
        if (len(media) > 0):
            Twitter_with_image.add(media[0]['media_url'])
    i=0
    for url in Twitter_with_image:
        image=wget.download(url)
        os.rename(image, 'image'+str(i) + '.jpg')
        i += 1
    return Twitter_with_image

#Use ffmpeg to convert the images to video
def conv_image():
     print('Converting the images to video....Processing')
     subprocess.call(['ffmpeg', '-framerate', '1', '-i', 'image%d.jpg', '-vcodec', 'mpeg4','Tweets.mp4'])


client = vision.ImageAnnotatorClient()

#Use the google vision to label to images and then add the label text to the images
def get_describe(h):
    print('Label the Images...Processing')
    for i in range(h):
        file_name = os.path.join(os.path.dirname(__file__), 'image%s.jpg'%(i))

        with io.open(file_name, 'rb') as image_file:
            content = image_file.read()

            image = vision.types.Image(content=content)


# Performs label detection on the image file
            response = client.label_detection(image=image)
            labels = response.label_annotations
        j = 0
        for label in labels:
            # print(label.description)
            raw_image = Image.open(file_name)
            draw = ImageDraw.Draw(raw_image)  # 修改图片
            font = ImageFont.truetype('/Library/Fonts/Times New Roman.ttf', 36)
            draw.text((50, 40 + j), label.description, fill=(0,0,0), font=font)
            j += 30
            raw_image.save(file_name)


def count_file_number():
    filename_list = listdir(image_path)
    h = 0
    for filename in filename_list:
        if filename.endswith('jpg'):
            h += 1
    print('Total image file :', + h-2)
    return h-2

if __name__ == '__main__':


    #Step1. Download the images from twitter
    #Step2. Label the images
    #Step3. Add the text to the images
    #steo4. Convert the image to video


    str1 = input("Request Download Image from Twitter Acount:")
    download_tweets(str1)
    h=count_file_number()
    get_describe(h)
    conv_image()