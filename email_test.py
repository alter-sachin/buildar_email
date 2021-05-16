# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import pandas as pd
import requests
import json
# send build email to many email addrsesses together
import constants


from CreateAudio import Audio
from CreateVideo import Video
from jinja2 import Template
from CreateGIF import GIF

from_email = constants.FROM_EMAIL

list_of_email_and_names = []

class Mailer:

	def __init__(self, from_email, to_email, subject, html_content):
		self.message = Mail(from_email=from_email, to_emails=to_email,
	    subject=subject,
	    html_content=html_content)

	def send_email(self):
		try:
		    sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
		    response = sg.send(self.message)
		    print(response.status_code)
		    print(response.body)
		    print(response.headers)

		except Exception as e:
		    # pylint: disable=no-member
		    print(e.message)


def read_email_list(source_csv):
	df = pd.read_csv(source_csv)

	for index, row in df.iterrows():
		firstname = row['Firstname']
		email = (row['Email'])
		pair = [email,firstname]

		list_of_email_and_names.append(pair)

	return list_of_email_and_names


def read_html(source_html):
	with open(source_html, 'r') as f:
		html_string = f.read()
	return html_string


# emailName = "sachin"

t = Template(read_html("firstmail.html"))


list_of_email_and_names = read_email_list("email_test1.csv")
# take a user from the list
for userMail,userFirstName in list_of_email_and_names: 
	subject = "We Made A Video Message For You"
	text_script = "Hello "+ userFirstName +", You will love making videos with me as an actor in them. ~"
	audio_url = Audio(speaker_name="Indian English Male Voice 1",text_script=text_script,speed=0.8).create_audio()
	video_url = Video(1,audio_url).create_video()
	print(video_url)
	gif_output = GIF(video_url,text_script).convertVideoToGifFile()
	gif_url = "https://buildar.live/images/" + gif_output
	html_content = t.render(name=userFirstName,
		gifurl=gif_url,
		videoLink=video_url)
	mailObj = Mailer(constants.FROM_EMAIL,str(userMail),subject,html_content)
	mailObj.send_email()
	


### we need to dymacillay upload the gif to a url on our buildar.live server
### and then give this url to the template

# async call to audio
# from audio create corresponding video
