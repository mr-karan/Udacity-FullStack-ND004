import webbrowser
class Movie:
	def __init__(self,title,trailer_youtube_url,poster_image_url,storyline):
		self.title = title
		self.trailer_youtube_url= trailer_youtube_url
		self.poster_image_url = poster_image_url
		self.storyline = storyline

	def show_trailer(self):
		webbrowser.open(self.trailer_youtube_url)