import turtle

def draw_shape():
	window = turtle.Screen()
	window.bgcolor("blue")

	jeff = turtle.Turtle()
	jeff.color("brown")
	jeff.shape("classic")
	jeff.speed(1)
	for i in range(36):
		jeff.rt(3)
		jeff.rt(120)
		jeff.fd(120)
	window.exitonclick()
draw_shape()
