import turtle

def draw_shape():
	window = turtle.Screen()
	window.bgcolor("blue")

	jeff = turtle.Turtle()
	jeff.color("brown")
	jeff.shape("classic")
	jeff.speed(1)
	for i in range(4):
		jeff.fd(100)
		jeff.rt(90)
	angie = turtle.Turtle()
	angie.circle(50)
	ron = turtle.Turtle()
	for i in range(3):
		ron.rt(120)
		ron.fd(60)
	window.exitonclick()
draw_shape()
