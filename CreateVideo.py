import json
import requests
import constants

api_endpoint = constants.API_ENDPOINT
header_data={'Authorization': constants.API_AUTHKEY}

class Video:
	def __init__(self,actorId,audioUrl):
		self.actorId = actorId
		self.audioUrl = audioUrl
		

	def create_request_body(self):
		data = {
		  "actorId": self.actorId,
		  "audioUrl": self.audioUrl,
		}
		return json.dumps(data)


	def get_speaker_details(self):
		print("implement later")


	def create_video(self):
		response = requests.post(api_endpoint+"video",
			headers=header_data,
			data = self.create_request_body())
		videoUrl = str(json.loads(response.content.decode('utf-8'))['videoUrl'])
		return videoUrl


# videoObj = Video(constants.ACTOR1,"https://dreal.in/aud/1621100562.873771.wav")
# #get_users()
# videoObj.create_video()
# # mailObj = Mailer(from_email,list_of_emails)

# # mailObj.send_email()