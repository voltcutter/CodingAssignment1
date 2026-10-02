## Import modules
import turtle
import time
import random
import math

import gameconstants as GameConstants
import terraindrawing as TerrainDrawing

## Setup screen
screen = turtle.Screen()
screen.setup(GameConstants.SCREEN_WIDTH, GameConstants.SCREEN_HEIGHT)
screen.title("Hide and Seek")
screen.bgcolor("white")
screen.tracer(0, 0)

## Setup several types of turtles
terrainTurtle = turtle.Turtle()
terrainTurtle.shape("square")

fpsTurtle = turtle.Turtle()
fpsTurtle.hideturtle()

splashScreenTitleTurtle = turtle.Turtle()
splashScreenTitleTurtle.hideturtle()

## Draw terrain
TerrainDrawing.DrawTerrain(screen, terrainTurtle)

## Game Loop
accumulatedFixedDeltaTime = 0
accumulatedDeltaTime = 0
pastFrameTime = time.time()

splashScreen = False
splashScreenDuration = 1.5
splashScreenProgress = 0 # moves from 0 to 1

## Splash screen
while True:
    deltaTime = time.time() - pastFrameTime
    pastFrameTime = time.time()

    splashScreenTitleTurtle.clear()
    splashScreenTitleTurtle.penup()

    # Draw black rectangle
    splashScreenTitleTurtle.goto(-GameConstants.SCREEN_WIDTH, -GameConstants.SCREEN_HEIGHT)
    splashScreenTitleTurtle.pendown()
    splashScreenTitleTurtle.fillcolor("#000000")
    splashScreenTitleTurtle.begin_fill()
    splashScreenTitleTurtle.goto(-GameConstants.SCREEN_WIDTH, GameConstants.SCREEN_HEIGHT)
    splashScreenTitleTurtle.goto(GameConstants.SCREEN_WIDTH, GameConstants.SCREEN_HEIGHT)
    splashScreenTitleTurtle.goto(GameConstants.SCREEN_WIDTH, -GameConstants.SCREEN_HEIGHT)
    splashScreenTitleTurtle.end_fill()
    splashScreenTitleTurtle.penup()

    # Calculate text brightness and size
    progress = accumulatedDeltaTime / splashScreenDuration
    brightness = 1 - progress
    size = int(60 + progress * 15)
    splashScreenTitleTurtle.color(
        brightness,
        brightness,
        brightness
    )
    splashScreenTitleTurtle.goto(0, -size / 2)
    splashScreenTitleTurtle.write("Title", align="center", font=("Arial", size, "normal"))

    accumulatedFixedDeltaTime += GameConstants.FIXED_DELTA_TIME
    accumulatedDeltaTime += deltaTime

    screen.update()

    time.sleep(GameConstants.FIXED_DELTA_TIME)

    if (accumulatedDeltaTime > splashScreenDuration):
        break

splashScreenTitleTurtle.clear()

## Game loop
while True:
    # fps calculations
    deltaTime = time.time() - pastFrameTime
    pastFrameTime = time.time()

    # show fps
    fpsTurtle.clear()
    fpsTurtle.pencolor("orange")
    # would use ternary operator here, but cannot due to restraints of the assignment.
    if deltaTime != 0:
        fpsTurtle.write("FPS: " + str(1/deltaTime), font=("Arial", 16, "normal"))
    else:
        fpsTurtle.write("FPS: -", font=("Arial", 16, "normal"))

    # end of frame
    screen.update()
    accumulatedFixedDeltaTime += GameConstants.FIXED_DELTA_TIME
    accumulatedDeltaTime += deltaTime
    time.sleep(GameConstants.FIXED_DELTA_TIME)