from media import Movie

toy_story = Movie(title = "Toy Story 3", youtube_url ="https://www.youtube.com/watch?v=HpeMXwwoZgc",
				  img_url="http://t3.gstatic.com/images?q=tbn:ANd9GcRUAG6E1nL4GRxsB1G5upnKfQVgm8zeILqd_EbN-2kjMeZZPcah",
				  storyline='''Andy's toys get mistakenly delivered to a day care centre. 
				  			Woody convinces the other toys that they weren't dumped and leads them on an expedition back 
				  			home.''')


pulp_fiction = Movie(title = "Pulp Fiction ", youtube_url ="https://www.youtube.com/watch?v=s7EdQ4FqbhY",
				  img_url="https://encrypted-tbn3.gstatic.com/images?q=tbn:ANd9GcTZuBLJPU2hkleQzm2iYFQIuVhn_O7gflYziq--y59ov5OAH_SJ4wTr5A",
				  storyline='''The lives of two mob hit men, a boxer, a gangster's wife, and a pair of diner bandits 
				  			   intertwine in four tales of violence and redemption''')

print("Fav movie is"+pulp_fiction.title)
pulp_fiction.show_trailer()
