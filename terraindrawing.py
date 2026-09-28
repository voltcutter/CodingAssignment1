## This module handles the drawing of terrain.
import math
import random
import time
import gameconstants as GameConstants
terrainSeed = time.time()
randomGenerator = random.Random(terrainSeed)

## Terrain metaball setup

# initialising this array like this to conform to the restraints of the assignment (i.e. appending to arrays is not allowed)
metaballPositions = [
    # (0, 0)
    (
        randomGenerator.randint(int(-GameConstants.TILE_SCREEN_WIDTH / 2), int(GameConstants.TILE_SCREEN_WIDTH / 2) + 1), 
        randomGenerator.randint(int(-GameConstants.TILE_SCREEN_HEIGHT / 2), int(GameConstants.TILE_SCREEN_HEIGHT / 2) + 1)
    ),
    (
        randomGenerator.randint(int(-GameConstants.TILE_SCREEN_WIDTH / 2), int(GameConstants.TILE_SCREEN_WIDTH / 2) + 1), 
        randomGenerator.randint(int(-GameConstants.TILE_SCREEN_HEIGHT / 2), int(GameConstants.TILE_SCREEN_HEIGHT / 2) + 1)
    ),
    (
        randomGenerator.randint(int(-GameConstants.TILE_SCREEN_WIDTH / 2), int(GameConstants.TILE_SCREEN_WIDTH / 2) + 1), 
        randomGenerator.randint(int(-GameConstants.TILE_SCREEN_HEIGHT / 2), int(GameConstants.TILE_SCREEN_HEIGHT / 2) + 1)
    ),
    (
        randomGenerator.randint(int(-GameConstants.TILE_SCREEN_WIDTH / 2), int(GameConstants.TILE_SCREEN_WIDTH / 2) + 1), 
        randomGenerator.randint(int(-GameConstants.TILE_SCREEN_HEIGHT / 2), int(GameConstants.TILE_SCREEN_HEIGHT / 2) + 1)
    ),
    (
        randomGenerator.randint(int(-GameConstants.TILE_SCREEN_WIDTH / 2), int(GameConstants.TILE_SCREEN_WIDTH / 2) + 1), 
        randomGenerator.randint(int(-GameConstants.TILE_SCREEN_HEIGHT / 2), int(GameConstants.TILE_SCREEN_HEIGHT / 2) + 1)
    ),
    (
        randomGenerator.randint(int(-GameConstants.TILE_SCREEN_WIDTH / 2), int(GameConstants.TILE_SCREEN_WIDTH / 2) + 1), 
        randomGenerator.randint(int(-GameConstants.TILE_SCREEN_HEIGHT / 2), int(GameConstants.TILE_SCREEN_HEIGHT / 2) + 1)
    ),
    (
        randomGenerator.randint(int(-GameConstants.TILE_SCREEN_WIDTH / 2), int(GameConstants.TILE_SCREEN_WIDTH / 2) + 1), 
        randomGenerator.randint(int(-GameConstants.TILE_SCREEN_HEIGHT / 2), int(GameConstants.TILE_SCREEN_HEIGHT / 2) + 1)
    ),
]
metaballConstant = 3 # the metaball summing formula (inverse distance) is multiplied by this constant

metaballThreshold = 2 # if the metaball sum is higher than this, then it's land. otherwise, it's water.

## Utility functions

# Draws a square tile, starting from the bottom left corner of the screen position (tileX * GameConstants.TILE_SIZE, tileY * GameConstants.TILE_SIZE)
def DrawTile(screen, turtle, tileX, tileY, color):
    turtle.penup()
    turtle.setheading(0)
    turtle.goto(tileX * GameConstants.TILE_SIZE, tileY * GameConstants.TILE_SIZE)

    turtle.color(color)
    turtle.stamp()

def DetermineColor(tileX, tileY):
    metaballSum = 0

    # iterate through all metaballs to calculate the metaball sum
    for metaballPosition in metaballPositions:
        # calculate the distance using pythagoreon theoreom
        distance = math.sqrt(
            ((metaballPosition[0] - tileX) ** 2) +
            ((metaballPosition[1] - tileY) ** 2)
        )
        # to prevent division by zero errors, set distance to 1 if 0
        if distance == 0:
            distance = 1
        # add inverse distance to total sum
        metaballSum += metaballConstant / distance
    
    # would use ternary operator here, but cannot due to restraints of the assignment.
    if metaballSum > metaballThreshold:
        return "green"
    else:
        return "blue"

def DrawTerrain(screen, turtle):
    # set turtle size so that stamping would cause an appropriately-sized square to appear
    turtle.turtlesize(GameConstants.TILE_SIZE / GameConstants.TURTLE_BASE_SIZE, GameConstants.TILE_SIZE / GameConstants.TURTLE_BASE_SIZE)

    # iterate through all tiles, and draw the tiles.
    for x in range(int(-GameConstants.TILE_SCREEN_WIDTH / 2), int(GameConstants.TILE_SCREEN_WIDTH / 2) + 1):
        for y in range(int(-GameConstants.TILE_SCREEN_HEIGHT / 2), int(GameConstants.TILE_SCREEN_HEIGHT / 2) + 1):
            # draw the tile
            DrawTile(screen, turtle, x, y, DetermineColor(x, y))
            # if ((x + y) % 2 == 0):
            #     DrawTile(screen, turtle, x, y, "black")
            # else:
            #     DrawTile(screen, turtle, x, y, "white")