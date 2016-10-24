import webbrowser


class Movie:
	'''
	A class to represent Movie object.
	'''	

	def __init__(self,title,trailer_youtube_url,poster_image_url,storyline):
		'''
		Initializes `Movie` object with the supplied arguments.
		'''
		
		self.title = title
		self.trailer_youtube_url= trailer_youtube_url
		self.poster_image_url = poster_image_url
		self.storyline = storyline

	def show_trailer(self):
		'''
		Method to open a new web browswer session with the link to movie trailer. 
		'''
		link = 'https://www.youtube.com/watch?v='+self.trailer_youtube_url
		webbrowser.open(link)
