import requests

def check(word):
	r= requests.get("http://www.wdylike.appspot.com/?q="+word).json()
	print(r)

check("this is a mother fucking piece of fucking shit")