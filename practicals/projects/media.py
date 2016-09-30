import webbrowser
class Movie:
	def __init__(self,title,youtube_url,img_url,storyline):
		self.title = title
		self.youtube_url = youtube_url
		self.img_url = img_url
		self.storyline = storyline

	def show_trailer(self):
		webbrowser.open(self.youtube_url)