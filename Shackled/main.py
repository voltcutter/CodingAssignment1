# Import the modules
import turtle
import math
import random
import time

# Constants (you can change these)
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 450
WINDOW_TITLE = "Hide & Seek"

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
    t.write("Made with Turtle", align="center", font=("Arial", size, "normal"))

    screen.update()
    time.sleep(1 / 30)

time.sleep(0.5)

t.clear()
t.goto(0, 100)
t.color(1, 1, 1)
t.write("Instructions", align="center", font=("Arial", 50, "normal"))
t.goto(0, 0)
t.write("Player 1 must type their secret location in pixels relative to the origin.", align="center", font=("Arial", 20, "normal"))
t.goto(0, -50)
t.write("Player 2 must make 4 guesses of the location.", align="center", font=("Arial", 20, "normal"))
t.goto(0, -100)
t.write("Good Luck.", align="center", font=("Arial", 20, "normal"))
screen.update()

# time.sleep(5)

t.clear()
screen.update()

SEA_COLOR = "#a4f4fc"
LAND_COLOR = "#329925"
TILE_SIZE = 25

## Generate background
for x in range(int(-SCREEN_WIDTH / 2), int(SCREEN_WIDTH / 2), TILE_SIZE):
    for y in range(int(-SCREEN_HEIGHT / 2), int(SCREEN_HEIGHT / 2), TILE_SIZE):
        tileX = math.floor(x / TILE_SIZE)
        tileY = math.floor(y / TILE_SIZE)

        t.penup()
        t.goto(x, y)

        # if (tileX + tileY) % 2 == 0, set colour to land colour
        t.pencolor(SEA_COLOR)
        t.fillcolor(SEA_COLOR)
        for i in range(1 - (tileX + tileY) % 2):
            t.pencolor(LAND_COLOR)
            t.fillcolor(LAND_COLOR)

        t.begin_fill()
        t.pendown()
        for i in range(4):
            t.forward(TILE_SIZE)
            t.left(90)
        t.end_fill()
        t.penup()

## Generate grid
t.color("#000000")
t.pensize(3)
t.penup()
t.goto(-SCREEN_WIDTH, 0)
t.pendown()
t.goto(SCREEN_WIDTH, 0)

t.penup()
t.goto(0, SCREEN_HEIGHT)
t.pendown()
t.goto(0, -SCREEN_HEIGHT)
t.penup()

for x in range(0, SCREEN_WIDTH, 50):
    t.penup()
    t.goto(x, -5)
    t.pendown()
    t.goto(x, 5)

    t.penup()
    t.goto(x, -30)
    t.write(str(x))

for x in range(0, -SCREEN_WIDTH, -50):
    t.penup()
    t.goto(x, -5)
    t.pendown()
    t.goto(x, 5)

    t.penup()
    t.goto(x, -30)
    t.write(str(x))

for y in range(0, SCREEN_HEIGHT, 50):
    t.penup()
    t.goto(-5, y)
    t.pendown()
    t.goto(5, y)

    t.penup()
    t.goto(-30, y)
    t.write(str(y))

for y in range(0, -SCREEN_HEIGHT, -50):
    t.penup()
    t.goto(-5, y)
    t.pendown()
    t.goto(5, y)

    t.penup()
    t.goto(-30, y)
    t.write(str(y))

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

def drawGuess(guessX, guessY):
    markerTurtle.penup()
    markerTurtle.goto(guessX, guessY)

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

time.sleep(5)

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