import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.video import Video
from kivy.lang import Builder
from kivy.uix.videoplayer import VideoPlayer
kivy.require("1.11.1")

# class EpicApp(App):
#     def build(self):
#         return Label(text = "hey there!")
    
# if __name__ == "__main__":
#     EpicApp().run() 

# root = Builder.load_string('''
# VideoPlayer:
#     source: 'http://10.21.143.20:8081/stream.mjpg'
# ''')

# class TestApp(App):
# 	def build(self):
# 		return root

class TestApp(App):
	def build(self):
		video = Video(source='http://10.21.143.20:8081/stream.mjpg')
		video.state= 'play'
		video.options = {'eos': 'loop'}
		video.allow_stretch=False
		return video

if __name__ == '__main__':
    TestApp().run()
