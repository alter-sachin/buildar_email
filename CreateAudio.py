import json
import requests

import constants

api_endpoint = constants.API_ENDPOINT

header_data={'Authorization': constants.API_AUTHKEY}

class Audio:
	def __init__(self,speaker_name,text_script,speed):
		self.speaker_name = speaker_name
		self.text_script = text_script
		self.speed = speed


	def create_request_body(self):
		data = {
		  "speakerId": self.speaker_name,
		  "textScript": self.text_script,
		  "speed": self.speed
		}
		return json.dumps(data)


	def get_speaker_details(self):
		print("implement later")


	def create_audio(self):
		response = requests.post(api_endpoint+"audio",
			headers=header_data,
			data = self.create_request_body())
		audioUrl = str(json.loads(response.content.decode('utf-8'))['audioUrl'])
		print(audioUrl)
		return audioUrl



# audioObj = Audio(constants.FEMALE_INDIAN_2,"I am checking with my people",constants.AUDIO_SPEED)
# #get_users()
# audioObj.create_audio()
# # mailObj = Mailer(from_email,list_of_emails)

# # mailObj.send_email()