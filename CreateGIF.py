import json
import requests
import time
import constants
# when this returns create html content and send
import imageio
import os
import urllib.request
import subprocess
from pygifsicle import optimize


from moviepy.editor import *
from moviepy.video.tools.subtitles import SubtitlesClip

class GIF:
	def __init__(self,video_url,text_script):
		self.video_url = video_url
		self.text_script = text_script

	def downloadVideo(self):
		file_name = str(time.time()) + ".mp4"
		urllib.request.urlretrieve(self.video_url, file_name)
		return file_name 

	
	def addSubtitle(self,subtitle_text,inputVideoFile,outputVideoFile):
		generator = lambda txt: TextClip(txt, font='Arial', fontsize=12, color='white')
		subs = [((0, 4.5), str(subtitle_text))]

		subtitles = SubtitlesClip(subs, generator)

		video = VideoFileClip(str(inputVideoFile))
		result = CompositeVideoClip([video, subtitles.set_position((0.15,0.85),relative=True)])

		result.write_videofile(str(outputVideoFile), fps=video.fps, temp_audiofile="temp-audio.m4a", remove_temp=True, codec="libx264", audio_codec="aac")


	def convertVideoToGifFile(self):	
	    
	    inputFile = self.downloadVideo()
	    inputFileOptimised = os.path.splitext(inputFile)[0] + "out.mp4"
	    inputFileResized = os.path.splitext(inputFile)[0] + "resized.mp4"
	    inputFileFrames = os.path.splitext(inputFile)[0] + "frames.mp4"
	    outputFileSub = os.path.splitext(inputFile)[0] + "output.mp4"
	    os.system("ffmpeg -i "+inputFile+" -vcodec libx265 -crf 28 "+inputFileOptimised + " -y")
	    os.system("ffmpeg -i "+inputFileOptimised+" -vf scale=256:-1 "+ inputFileResized + " -y")
	    os.system("ffmpeg -i "+inputFileResized + " -filter:v fps=10 " + inputFileFrames+ " -y")
	    #subprocess.call(['ffmpeg', '-i', inputFile,'-vcodec','libx265','-crf','28',inputFile])
	    outputFile = os.path.splitext(inputFile)[0] + ".gif"
	    self.addSubtitle(self.text_script, inputFileFrames,outputFileSub)
			
	    print("Converting {0} to {1}".format(outputFileSub, outputFile))

	    reader = imageio.get_reader(outputFileSub)
	    fps = reader.get_meta_data()['fps']

	    writer = imageio.get_writer(outputFile, fps=fps)
		
	    for i,im in enumerate(reader):
	        writer.append_data(im)

	    writer.close()
	    optimize(outputFile)
	    outputgif = os.path.splitext(outputFile)[0] + "_out.gif "
	    os.system("rm *.mp4")
	    os.system("gifsicle -O4 "+ outputFile+ " -o " + outputgif + " --colors 128")
	    return outputFile




