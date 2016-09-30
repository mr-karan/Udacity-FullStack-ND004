from media import Movie

toy_story = Movie(title = "Toy Story 3", youtube_url ="https://www.youtube.com/watch?v=HpeMXwwoZgc",
				  img_url="http://t3.gstatic.com/images?q=tbn:ANd9GcRUAG6E1nL4GRxsB1G5upnKfQVgm8zeILqd_EbN-2kjMeZZPcah",
				  storyline='''Andy's toys get mistakenly delivered to a day care centre. 
				  			Woody convinces the other toys that they weren't dumped and leads them on an expedition back 
				  			home.''')

print(toy_story.title)
toy_story.show_trailer()