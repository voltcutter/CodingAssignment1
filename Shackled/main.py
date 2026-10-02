# Import the modules
import turtle
import math
import random
import time

# Constants (you can change these)
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 450
WINDOW_TITLE = "Shackled"

# Set up the screen object
turtle.setup(SCREEN_WIDTH, SCREEN_HEIGHT)
screen = turtle.Screen()
screen.title(WINDOW_TITLE)
screen.tracer(0)

## Splash screen
t = turtle.Turtle()
t.hideturtle()

screen.bgcolor("#000000")

for i in range(30):
    progress = i / 30
    brightness = 1 - progress
    size = int(60 + i * 0.25)

    t.clear()
    t.color(brightness, brightness, brightness)
    t.penup()
    t.goto(0, -size / 2)
    t.write("Hide & Seek", align="center", font=("Arial", size, "normal"))

    screen.update()
    time.sleep(1 / 30)

t.clear()
t.goto(0, 0)
t.color(1, 1, 1)
t.write("Instructions")
screen.update()

time.sleep(5)

t.clear()
screen.update()

## Generate background
screen.bgcolor("#a4f4fc")
t.color("#888888")
t.penup()
t.goto(-10, 0)
t.pendown()
t.goto(10, 0)

t.penup()
t.goto(0, 10)
t.pendown()
t.goto(0, -10)
t.penup()

screen.update()

## Receive secret location from player 1
secretX = screen.numinput("Secret Location", "Please put the x coordinate of your secret location.")
secretY = screen.numinput("Secret Location", "Please put the y coordinate of your secret location.")

## Guess loop
totalScore = 0
totalDistance = 0
closestDistance = math.inf

def getDistance(guessX, guessY):
    distance = math.sqrt((secretX - guessX) ** 2 + (secretY - guessY) ** 2)
    return distance

def getScore(guessX, guessY):
    distance = getDistance(guessX, guessY)
    score = (max(0, 200 - distance) ** 2) / 4000
    return score

markerTurtle = turtle.Turtle()
markerTurtle.hideturtle()
markerTurtle.penup()
markerTurtle.shape("circle")

for i in range(1):
    guessX = screen.numinput("Guess", "Please put the x coordinate of your guess.")
    guessY = screen.numinput("Guess", "Please put the y coordinate of your guess.")
    markerTurtle.goto(guessX, guessY)
    markerTurtle.stamp()

    markerTurtle.goto(guessX + 50, guessY)
    score = getScore(guessX, guessY)
    distance = getDistance(guessX, guessY)
    markerTurtle.write(f"Score: {score:.2f}, Distance: {distance:.2f}")

    totalScore += score
    totalDistance += distance

    closestDistance = min(closestDistance, distance)

    screen.update()
    time.sleep(2)

## Reveal secret
markerTurtle.goto(0, 0)
markerTurtle.shape("turtle")
markerTurtle.color("#FFFF00")
markerTurtle.stamp()

screen.update()

time.sleep(1)

## Game results
t.clearstamps()

screen.bgcolor("#000000")
t.color("#ffffff")
t.goto(0, 100)
t.write("Result", align="center", font=("Arial", 30, "normal"))

t.goto(0, 0)
t.write(f"Total Score: {totalScore}", align="center", font=("Arial", 15, "normal"))
t.goto(0, -50)
t.write(f"Total Distance: {totalDistance}", align="center", font=("Arial", 15, "normal"))
t.goto(0, -100)
t.write(f"Best Distance: {closestDistance}", align="center", font=("Arial", 15, "normal"))

screen.update()

## End of your code

# Make a clean exit
screen.exitonclick()