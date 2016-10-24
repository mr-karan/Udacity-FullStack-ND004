import requests

def check(word):
	r= requests.get("http://www.wdylike.appspot.com/?q="+word).json()
	print(r)

def extract():
	with open("movie_quotes.txt") as the_file:
		content = the_file.read()

	check(content)

extract()