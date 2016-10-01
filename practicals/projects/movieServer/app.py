
from flask import Flask
app = Flask(__name__)
from media import Movie
from flask import render_template
import re

@app.route('/')
def hello():
	toy_story = Movie(title = "Toy Story 3", trailer_youtube_url ="https://www.youtube.com/watch?v=QW0sjQFpXTU",
				  poster_image_url="https://images-na.ssl-images-amazon.com/images/M/MV5BMTgxOTY4Mjc0MF5BMl5BanBnXkFtZTcwNTA4MDQyMw@@._V1_UY268_CR3,0,182,268_AL_.jpg",
				  storyline='''Andy's toys get mistakenly delivered to a day care centre. 
				  			Woody convinces the other toys that they weren't dumped and leads them on an expedition back 
				  			home.''')
	pulp_fiction = Movie(title = "Pulp Fiction ", trailer_youtube_url ="https://www.youtube.com/watch?v=s7EdQ4FqbhY",
					  poster_image_url="https://images-na.ssl-images-amazon.com/images/M/MV5BMTkxMTA5OTAzMl5BMl5BanBnXkFtZTgwNjA5MDc3NjE@._V1_UX182_CR0,0,182,268_AL_.jpg",
					  storyline='''The lives of two mob hit men, a boxer, a gangster's wife, and a pair of diner bandits 
					  			   intertwine in four tales of violence and redemption''')
	shawshank = Movie(title = "The Shawshank Redemption", trailer_youtube_url ="https://www.youtube.com/watch?v=KtwXlIwozog",
					  poster_image_url="https://images-na.ssl-images-amazon.com/images/M/MV5BODU4MjU4NjIwNl5BMl5BanBnXkFtZTgwMDU2MjEyMDE@._V1_UX182_CR0,0,182,268_AL_.jpg",
					  storyline='''Two imprisoned men bond over a number of years, finding solace
					  			and eventual redemption through acts of common decency.''')
	godfather = Movie(title = "The Godfather ", trailer_youtube_url ="https://www.youtube.com/watch?v=sY1S34973zA",
					  poster_image_url="https://images-na.ssl-images-amazon.com/images/M/MV5BMjEyMjcyNDI4MF5BMl5BanBnXkFtZTcwMDA5Mzg3OA@@._V1_UX182_CR0,0,182,268_AL_.jpg",
					  storyline='''The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son.''')
	dark_knight = Movie(title = "The Dark Knight ", trailer_youtube_url ="https://www.youtube.com/watch?v=EXeTwQWrcwY",
					  poster_image_url="https://images-na.ssl-images-amazon.com/images/M/MV5BMTMxNTMwODM0NF5BMl5BanBnXkFtZTcwODAyMTk2Mw@@._V1_UX182_CR0,0,182,268_AL_.jpg",
					  storyline='''Set within a year after the events of Batman Begins, Batman, Lieutenant James Gordon, and new district attorney Harvey Dent successfully begin to round up the criminals''')
	movies=[toy_story,pulp_fiction,dark_knight,godfather,shawshank]
	youtube_urls=[]
	for movie in movies:
		youtube_id_match = re.search(r'(?<=v=)[^&#]+', movie.trailer_youtube_url)
		youtube_id_match = youtube_id_match or re.search(r'(?<=be/)[^&#]+', movie.trailer_youtube_url)
		trailer_youtube_id = (youtube_id_match.group(0) if youtube_id_match else None)
		movie.trailer_youtube_url = trailer_youtube_id
	return render_template('index.html',
                           data=movies)

if __name__ == '__main__':
	app.run(debug=True)


