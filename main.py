## Import modules
import turtle
import time
import random

import gameconstants as GameConstants
import terraindrawing as TerrainDrawing

## Setup screen
screen = turtle.Screen()
screen.setup(GameConstants.SCREEN_WIDTH, GameConstants.SCREEN_HEIGHT)
screen.title("Hide and Eel")
screen.bgcolor("white")
screen.tracer(0, 0)

## Setup several types of turtles
terrainTurtle = turtle.Turtle()
terrainTurtle.shape("square")

fpsTurtle = turtle.Turtle()

## Draw terrain
TerrainDrawing.DrawTerrain(screen, terrainTurtle)

## Game Loop
accumulatedFixedDeltaTime = 0
pastFrameTime = time.time()
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
    time.sleep(GameConstants.FIXED_DELTA_TIME)