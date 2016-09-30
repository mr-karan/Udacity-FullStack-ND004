import turtle

def draw_rectangle():
	window = turtle.Screen()
	window.bgcolor("blue")

	jeff = turtle.Turtle()
	jeff.color("brown")
	jeff.shape("classic")
	jeff.speed(1)
	jeff.fd(100)
	jeff.rt(90)
	jeff.fd(50)
	jeff.rt(90)
	jeff.fd(100)
	jeff.rt(90)
	jeff.fd(50)
	jeff.rt(90)

draw_rectangle()
