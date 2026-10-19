# Import the modules
import turtle
import math
import random
import time

## Game Constants
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 600
WINDOW_TITLE = "Code & Seek"

## Terrain Constants
SEED = time.time()
TILE_SIZE = 5 # size of each tile, in pixels
NUM_METABALLS = 20 # number of metaballs to use in terrain generation
METABALL_MULTIPLIER = 7 # the inverse distance is multiplied by this number and added to the total metaball value when determining colour

DEEP_SEA_THRESHOLD = 2.1
# shallow sea colour
SEA_COLOUR_SHALLOW_R = 247 / 255
SEA_COLOUR_SHALLOW_G = 234 / 255
SEA_COLOUR_SHALLOW_B = 186 / 255
# deep sea colour
SEA_COLOUR_DEEP_R = 66 / 255
SEA_COLOUR_DEEP_G = 159 / 255
SEA_COLOUR_DEEP_B = 156 / 255

BEACH_THRESHOLD = 2.75 # metaball values above this threshold will be considered beach
BEACH_COLOUR = "#faefc6"
BEACH_COLOUR_ALT = "#f7eaba"

LAND_THRESHOLD = 3 # metaball values above this threshold will be considered land
LAND_COLOUR = "#329925"
LAND_COLOUR_ALT = "#2F7918"

## Vegetation Constants
PALM_TREE_CHANCE = 1 # chance to generate a palm tree per valid tile from 0-100
PALM_TRUNK_MAX_LEANING_ANGLE = 7 # the maximum change in angle of each palm trunk segment in degrees
PALM_TRUNK_THICKNESS = 3 # the width of the pen when drawing the palm trunk
PALM_TRUNK_COLOUR = "#421C0A"
PALM_TRUNK_COLOUR_ALT = "#6C3615"
PALM_TRUNK_SEGMENTS = 5 # the amount of segments for the palm trees
PALM_TRUNK_SEGMENT_LENGTH = 4 # the length of each segment in pixels
PALM_LEAVES_THICKNESS = 2 # the width of the pen when drawing palm leaves
PALM_LEAVES_COLOUR = "#5FC039"
PALM_LEAVES_SEGMENTS = 3 # the amount of palm leaves segments
PALM_LEAVES_SEGMENT_LENGTH = 6 # the length of each palm leaf segment in pixels
PALM_LEAVES_DROOP = 2 # the amount that each palm leaf segment droops down
PALM_LEAVES_DROOP_INDEX_OFFSET = -1 # the lower this value, the higher up the palm leaves will start at before drooping down.
PALM_LEAVES_TILT = 0.4 # the amount of horizontal tilt of the palm leaves. a smaller value will give more of a 3d isometric effect.
PALM_LEAVES_COUNT_MIN = 3
PALM_LEAVES_COUNT_MAX = 5

FLOWER_CHANCE = 1 # chance to generate a flower per valid tile from 0-100
FLOWER_BUD_COLOUR = "#fff200"
FLOWER_BUD_RADIUS = 5 # radius of the flower bud in pixels
FLOWER_PETAL_RADIUS = 5 # radius of the petals in pixels
FLOWER_PETAL_OFFSET = 2 # the offset distance between the flower bud and the flower petals
FLOWER_PETAL_COUNT = 5 # the amount of flower petals

# Set up the screen object
turtle.setup(SCREEN_WIDTH, SCREEN_HEIGHT)
screen = turtle.Screen()
screen.title(WINDOW_TITLE)
screen.tracer(0)

## Splash screen

# intro
# draws white text on a black screen
# the white text enlarges and fades out over 30 framess
main_turtle = turtle.Turtle()
main_turtle.hideturtle()

screen.bgcolor("#000000")

for i in range(30):
    progress = i / 30
    brightness = 1 - progress
    size = int(60 + i * 0.25)

    main_turtle.clear()
    main_turtle.color(brightness, brightness, brightness)
    main_turtle.penup()
    main_turtle.goto(0, -size / 2)
    main_turtle.write("Made with Turtle", align="center", font=("Arial", size, "normal"))

    screen.update()
    time.sleep(1 / 30)

time.sleep(0.5)

# instructions
main_turtle.clear()
main_turtle.goto(0, 100)
main_turtle.color(1, 1, 1)
main_turtle.write("Code & Seek", align="center", font=("Arial", 50, "normal"))
main_turtle.goto(0, 0)
main_turtle.write("Player 1 must type their secret location in pixels relative to the origin.", align="center", font=("Arial", 20, "normal"))
main_turtle.goto(0, -50)
main_turtle.write("Player 2 must make 4 guesses of the location.", align="center", font=("Arial", 20, "normal"))
main_turtle.goto(0, -100)
main_turtle.write("Good Luck.", align="center", font=("Arial", 20, "normal"))

screen.update()

time.sleep(5)

main_turtle.clear()
screen.update()

## Generate background
"""
EXPLANATION OF TERRAIN GENERATION:

To generate terrain, I will use a concept called 'metaballs'.
Metaballs are commonly used to create organic looking shapes from just a few points.
It's common in 2d particle simulations to smooth out the shape of the particles, which is where I learned this concept!

A 'metaball' is a point in space that has a value that decreases as the distance to a sample point 'P' increases.
In other words, the metaball value is inversely proportional to the distance.
In this specific game, the metaball function is as follows:

f(x) = k/x

where 'f' represents the metaball function,
      'x' represents the distance between the metaball and 'P',
      'k' represents the metaball multiplier. (defined in the terrain constants)

To determine the 'total metaball value' at P, the program will find f(x) for all metaballs and get the sum.
In other words, the sum of all metaball functions at P is defined as the 'total metaball value'.
This value is then used to determine the colour of the tile at P.

If the total metaball value is greater than the beach threshold, the colour is the beach colour.
If the total metaball value is greater than the land threshold, the colour is the land colour.
Otherwise, it's water colour.

------

DETAILED EXPLANATION OF IMPLEMENTATION:
In this specific game, I chose to use a tile-based approach.
Since turtle is a vector based drawing program, I decided the simplest way to represent terrain is using square tiles.
Each square tile can have a certain colour, and when these tiles are placed together, it will look like terrain.

To generate the whole map, the colour of each square tile is calculated one at a time through the usage of a for loop, and the colour is then drawn as a tile.
The for loop iterates through all possible tile positions, and the colour of each tile is determined by calling the determine_colour_of_tile() method.

In this method, the colour of the tile is determined using the following steps:
1. Get the total metaball value at the tile's position
2. Use the total metaball value to determine the colour of the tile

In step one, the total metaball value is calculated.
Firstly, the seed must be set to a constant value (SEED constant determined at the start of the code) at the beginning of this method.
The reason is because since the program is iterating through all the tiles, the random metaball positions
must be the same for all the tiles, or else the map would just look like random noise.
Setting the seed does two things: it ensures that the random numbers being generated will be consistent, and also resets the state of the random generator. These two things combined makes the random numbers generated become consistent for all tiles.
After this, the program repeats these steps for the amount of metaballs that there are. (NUM_METABALLS)
1a. generate a random metaball position
1b. calculate the distance and inverse distance
1c. multiply the inverse distance by the metaball multiplier and add it to the total metaball value
Once the loop is done, the total metaball value is returned.

In step two, the colour of the tile is determined.
This is done by using the total metaball value and comparing it to the thresholds.
First, the sea colour is calculated and set as the colour.
The sea colour is a colour interpolated between the deep and shallow sea colours, depending on its deepness.
The deepness is calculated using inverse linear interpolation between the deep sea threshold and beach threshold.
A t value is then created using the deepness value, which is within the range [0.5, 1]. This is because the shallow sea colour is actually very close to the beach colour, and a tile just below the water would appear almost the same as the beach, which is unwanted.
Then, the t value is increased if the sum of the x and y tile coordinates, integer divided by two, is even. This produces a checkerboard pattern which looks aesthetically pleasing. There is integer division by two because this operation would make each checker two tiles large.
Then, the sea colour is interpolated between the shallow and deep sea colours, using the deepness as the t value.
The resulting colour is then set as the tile's colour.

Now, it is time to determine if the tile is actually above the water.
If the total metaball value is above BEACH_THRESHOLD, the tile is considered beach.
    - For this assignment, an if statement is disallowed.
    - Instead, a for loop could be used in its place to achieve an equivilant effect.
    - As I learned in class, the inner block of a for loop runs for the numbers contained within the builtin 'range' method.
    - However, what if the range contains 0 numbers? This is possible if range(x) is used where x < 1. This will cause the inner block to not run.
    - Therefore, by using range(clamp(math.ceil(total_metaball_value - BEACH_THRESHOLD), 0, 1)), the inner block will run if and only if the total metaball value is above the BEACH_THRESHOLD.
    - This can be applied to any other condition, as long as the value is < 1 if it is false and >= 1 if it is true.
The colour, by default is BEACH_COLOUR. However, the same checkerboard condition from above is applied here too. In that case, it is BEACH_COLOUR_ALT.
This overrides the water colour from before.

If the total metaball value is above LAND_THRESHOLD, the tile is considered land. (The same for loop logic is applied here as well)
Just like the beach, the colour is either LAND_COLOUR or LAND_COLOUR_ALT.
This overrides the beach colour.

Then, draw_tile is used which simply draws a tile of the colour that was determined in these past steps.

For vegetation, the draw_palm_tree and draw_flower methods are used.
Palm trees can only be drawn on beach, since palm trees only grow on sand.
Flowers can only be drawn on land, since flowers only grow on grass.
To determine if the tile is sand/grass, the same method from above is used.
If the condition is met, there is a chance (defined in the constants) that the respective vegetation is drawn.

After this, the map is fully drawn!

------

Decision making:

I decided to make some sort of tile-based terrain for this assignment, as it would be interesting.
From this, I knew that some sort of noise algorithm would need to be used. It would be some algorithm that could return a random value given a point.
The first thing I thought of was "Perlin Noise", which is a form of smooth noise that I have used in the past. This is commonly used in games to generate terrain, and game engines often have built-in implementations for perlin noise, such as Mathf.PerlinNoise method from unity.
However, I then found out that the python 'random' module does not have a built-in implementation of perlin noise. I also do not know how to implement perlin noise, so I decided to not use perlin noise.
Then, I thought about generating pure random values and interpolating between them to create smooth noise. However, that may look too uninteresting/patternless.
Then I remembered about the existence of metaballs. I had used them in the past and I remember how they were really good for blending together particles.
They are also really simple to implement and understand.
So, I decided to use metaballs for this assignment.
"""
# math utility methods
def clamp(x, a, b):
    """
    Clamps x between a and b
    """
    return max(a, min(x, b))
def lerp(a, b, t):
    """
    Linearly interpolates between two numbers, a and b, by t
    """
    return a + (b - a) * t
def inverse_lerp(a, b, n):
    """
    Returns the value of t such that a + (b - a) * t = n within [0, 1]
    """
    return clamp((n - a) / (b - a), 0, 1)
def blend_colour(r1, g1, b1, r2, g2, b2, t):
    """
    Linearly interpolates between two colours by t
    """
    return (lerp(r1, r2, t), lerp(g1, g2, t), lerp(b1, b2, t))

# terrain generation methods
def get_total_metaball_value(tileX, tileY):
    """
    Gets the total metaball value at a tile's position
    """
    random.seed(SEED)
    total_metaball_value = 0
    for i in range(NUM_METABALLS):
        # generate a random metaball position
        metaball_x = random.randint(-SCREEN_WIDTH // TILE_SIZE // 2, SCREEN_WIDTH // TILE_SIZE // 2)
        metaball_y = random.randint(-SCREEN_HEIGHT // TILE_SIZE // 2, SCREEN_HEIGHT // TILE_SIZE // 2)
        # calculate its inverse distance
        distance = max(math.sqrt((tileX - metaball_x) ** 2 + (tileY - metaball_y) ** 2), 1) # clamped in the range [1, math.inf) to prevent divisoin-by-zero error if the distance is zero
        inverse_distance = 1 / distance
        metaball_value = inverse_distance * METABALL_MULTIPLIER

        total_metaball_value = total_metaball_value + metaball_value # use accumulator pattern to accumulate the total metaball value
    return total_metaball_value

def determine_colour_of_tile(tileX, tileY):
    """
    Determines the colour of a tile given its coordinates.
    """
    total_metaball_value = get_total_metaball_value(tileX, tileY)

    deepness = 1 - inverse_lerp(DEEP_SEA_THRESHOLD, BEACH_THRESHOLD, total_metaball_value) # calculate deepness of water
    t_value = deepness * 0.5 + 0.5 # adjusts the t value to be within the range [0.5, 1], making it appear more visually appealing
    for i in range(1 - ((tileX // 2 + tileY // 2) % 2)): # if the sum of the tileX // 2 and tileY // 2 coordinates is even, choose the colour of a slightly deeper depth (this creates a checkboard pattern where each checker is 2 tiles large)
        t_value = clamp(t_value + 0.1, 0, 1)
    colour = blend_colour(SEA_COLOUR_SHALLOW_R, SEA_COLOUR_SHALLOW_G, SEA_COLOUR_SHALLOW_B, SEA_COLOUR_DEEP_R, SEA_COLOUR_DEEP_G, SEA_COLOUR_DEEP_B, t_value)

    # set colour to beach, if the metaball value is above BEACH_THRESHOLD.
    # if total_metaball_value > BEACH_THRESHOLD, the expression will evaluate to a value that is at least 1, which runs the for loop and overwrites the colour to beach colour.
    # otherwise, it will evaluate to a value below 1, which does not run the for loop, and keeps it as sea colour.
    # an if statement is much more optimal here, however, if statements are disallowed.
    for i in range(clamp(math.ceil(total_metaball_value - BEACH_THRESHOLD), 0, 1)):
        colour = BEACH_COLOUR
        # same checkboard condition from above
        for j in range(1 - ((tileX // 2 + tileY // 2) % 2)):
            colour = BEACH_COLOUR_ALT

    # same condition from above, adjusted for land threshold and land colour
    for i in range(clamp(math.ceil(total_metaball_value - LAND_THRESHOLD), 0, 1)):
        colour = LAND_COLOUR
        # same checkboard condition from above
        for j in range(1 - ((tileX // 2 + tileY // 2) % 2)):
            colour = LAND_COLOUR_ALT

    return colour

def draw_rectangle(turtle, min_x, min_y, max_x, max_y):
    """
    Draws the outline of a rectangle with the bottom-left corner at screen position (min_x, min_y),
    and the top-right corner at screen position (max_x, max_y).
    """
    turtle.penup()
    turtle.goto(min_x, min_y)
    turtle.pendown()
    turtle.goto(max_x, min_y)
    turtle.goto(max_x, max_y)
    turtle.goto(min_x, max_y)
    turtle.penup()

def draw_rectangle_fill(turtle, min_x, min_y, max_x, max_y, fill_colour):
    """
    Draws a filled rectangle with the bottom-left corner at screen position (min_x, min_y),
    and the top-right corner at screen position (max_x, max_y).
    """
    turtle.penup()
    turtle.goto(min_x, min_y)
    turtle.fillcolor(fill_colour)
    turtle.begin_fill()
    turtle.pendown()
    turtle.goto(max_x, min_y)
    turtle.goto(max_x, max_y)
    turtle.goto(min_x, max_y)
    turtle.penup()
    turtle.end_fill()

def draw_tile(tileX, tileY):
    """
    Draws a filled square with the bottom-left corner at screen position (tileX * TILE_SIZE, tileY * TILE_SIZE),
    and the top-right corner at screen position ((tileX + 1) * TILE_SIZE, (tileY + 1) * TILE_SIZE).

    Its colour is determined by the return value of determine_colour_of_tile(tileX, tileY)
    """

    # move the turtle to the tile's position
    main_turtle.penup()
    main_turtle.goto(tileX * TILE_SIZE, tileY * TILE_SIZE)

    # determine and set the colour
    colour = determine_colour_of_tile(tileX, tileY)
    main_turtle.fillcolor(colour)
    main_turtle.pencolor(colour)
    main_turtle.pensize(1)

    # draw and fill a square
    main_turtle.begin_fill()
    main_turtle.pendown()
    for i in range(4):
        main_turtle.forward(TILE_SIZE)
        main_turtle.left(90)
    main_turtle.end_fill()
    main_turtle.penup()

def draw_palm_tree(tileX, tileY):
    """
    Draws a palm tree where its stump is at screen position (tileX * TILE_SIZE + TILE_SIZE // 2, tileY * TILE_SIZE + TILE_SIZE // 2)
    """
    stump_x = tileX * TILE_SIZE + TILE_SIZE // 2
    stump_y = tileY * TILE_SIZE + TILE_SIZE // 2
    trunk_leaning = random.randint(-PALM_TRUNK_MAX_LEANING_ANGLE, PALM_TRUNK_MAX_LEANING_ANGLE) # the angle at which the trunk will lean

    main_turtle.penup()
    main_turtle.goto(stump_x, stump_y)
    main_turtle.setheading(90)

    # Draw a trunk
    trunk_tip_x = 0
    trunk_tip_y = 0
    main_turtle.pensize(PALM_TRUNK_THICKNESS)
    main_turtle.pendown()
    for i in range(PALM_TRUNK_SEGMENTS):
        main_turtle.pencolor(PALM_TRUNK_COLOUR)
        for j in range(i % 2): # alternate colours every other segment
            main_turtle.pencolor(PALM_TRUNK_COLOUR_ALT)
        main_turtle.right(trunk_leaning)
        main_turtle.forward(PALM_TRUNK_SEGMENT_LENGTH)
        trunk_tip_x = main_turtle.xcor()
        trunk_tip_y = main_turtle.ycor()

    # Draw leaves
    initial_angle = random.random()
    angle = initial_angle
    main_turtle.pencolor(PALM_LEAVES_COLOUR)
    main_turtle.pensize(PALM_LEAVES_THICKNESS)
    palm_leaves_count = random.randint(PALM_LEAVES_COUNT_MIN, PALM_LEAVES_COUNT_MAX)
    for i in range(palm_leaves_count):
        # represents the current displacement from the trunk tip
        current_displacement_x = 0
        current_displacement_y = 0
        # represents the direction in which the palm leaves should move
        base_displacement_x = PALM_LEAVES_SEGMENT_LENGTH * math.cos(angle)
        base_displacement_y = PALM_LEAVES_SEGMENT_LENGTH * math.sin(angle)

        main_turtle.penup()
        main_turtle.goto(trunk_tip_x, trunk_tip_y)
        main_turtle.pendown()
        for j in range(PALM_LEAVES_SEGMENTS):
            # the y displacement is multiplied by a tilt value to make it appear more 3d and subtracted by the droop amount, which increases every segment to represent a drooping leaf
            tilted_displacement_y = base_displacement_y * PALM_LEAVES_TILT - PALM_LEAVES_DROOP * (j + PALM_LEAVES_DROOP_INDEX_OFFSET)
            main_turtle.goto(
                trunk_tip_x + current_displacement_x + base_displacement_x,
                trunk_tip_y + current_displacement_y + tilted_displacement_y
            )
            # use the accumulator pattern and add the displacement that it just drew
            current_displacement_x = current_displacement_x + base_displacement_x
            current_displacement_y = current_displacement_y + tilted_displacement_y
        angle = angle + (math.pi * 2) / palm_leaves_count

    main_turtle.penup()

def draw_flower(tileX, tileY):
    """
    Draws a round flower where its centre is at screen position (tileX * TILE_SIZE + TILE_SIZE // 2, tileY * TILE_SIZE + TILE_SIZE // 2)
    """
    x = tileX * TILE_SIZE + TILE_SIZE // 2
    y = tileY * TILE_SIZE + TILE_SIZE // 2

    # draw all the petals first, with a random RGB colour.
    angle = random.random()
    main_turtle.pensize(1)
    petalR = random.random()
    petalG = random.random()
    petalB = random.random()
    for i in range(FLOWER_PETAL_COUNT):
        petalX = x + (FLOWER_PETAL_RADIUS + FLOWER_PETAL_OFFSET) * math.cos(angle)
        petalY = y + (FLOWER_PETAL_RADIUS + FLOWER_PETAL_OFFSET) * math.sin(angle)
        main_turtle.penup()
        main_turtle.goto(petalX, petalY - FLOWER_PETAL_RADIUS)
        main_turtle.setheading(0)
        main_turtle.pendown()
        main_turtle.fillcolor(petalR, petalG, petalB)
        main_turtle.pencolor(petalR, petalG, petalB)
        main_turtle.begin_fill()
        main_turtle.circle(FLOWER_BUD_RADIUS)
        main_turtle.end_fill()
        main_turtle.penup()

        angle = angle + math.pi * 2 / FLOWER_PETAL_COUNT

    # draw the bud last so that it goes over the petals
    main_turtle.penup()
    main_turtle.goto(x, y - FLOWER_BUD_RADIUS)
    main_turtle.setheading(0)
    main_turtle.pendown()
    main_turtle.fillcolor(FLOWER_BUD_COLOUR)
    main_turtle.pencolor(FLOWER_BUD_COLOUR)
    main_turtle.begin_fill()
    main_turtle.circle(FLOWER_BUD_RADIUS)
    main_turtle.end_fill()
    main_turtle.penup()

main_turtle.clear()
main_turtle.penup()

loading_turtle = turtle.Turtle()
loading_turtle.hideturtle()

def draw_loading_screen(is_generating_vegetation, progress):
    """
    Draws the loading screen.
    If is_generating_vegetation is 1, the text will switch to 'Generating vegetation...' instead.
    """
    # draw the black background
    draw_rectangle_fill(loading_turtle, -SCREEN_WIDTH // 2, -SCREEN_HEIGHT // 2, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, "#000000")

    # draw big generating text
    loading_turtle.color("#ffffff")
    loading_turtle.penup()
    loading_turtle.goto(0, -25)
    for i in range(1 - is_generating_vegetation):
        loading_turtle.write("Generating terrain...", align="center", font=("Arial", 50, "normal"))
    for i in range(is_generating_vegetation):
        loading_turtle.write("Generating vegetation...", align="center", font=("Arial", 50, "normal"))

    # draw "this may take a few seconds"
    loading_turtle.goto(0, -50)
    loading_turtle.write("(This may take a few seconds)", align="center", font=("Arial", 14, "normal"))

    # draw progress bar
    loading_turtle.pencolor("#ffffff")
    draw_rectangle(loading_turtle, -100, -90, 100, -70) # outline of the progress bar
    draw_rectangle_fill(loading_turtle, -100, -90, -100 + lerp(0, 200, progress), -70, "#ffffff") # filling bar of the progress bar

# Draw the loading screen with zero progress at the start
draw_loading_screen(0, 0)
screen.update()

# Start generating terrain
progress = 0
for x in range(int(-SCREEN_WIDTH / 2), int(SCREEN_WIDTH / 2), TILE_SIZE):
    for y in range(int(-SCREEN_HEIGHT / 2), int(SCREEN_HEIGHT / 2), TILE_SIZE):
        # Draw the terrain tile
        tileX = math.floor(x / TILE_SIZE)
        tileY = math.floor(y / TILE_SIZE)
        draw_tile(tileX, tileY)

        # Use accumulator pattern on the progress
        progress = progress + 1
        # Normalised progress is the progress of the generation from 0-1, used for draw_loading_screen
        normalised_progress = progress / ((SCREEN_WIDTH / TILE_SIZE) * (SCREEN_HEIGHT / TILE_SIZE))
        for i in range(1 - clamp(progress % 2048, 0, 1)): # only draw every 2048 iterations to save performance
            loading_turtle.clear()
            draw_loading_screen(0, normalised_progress)
            screen.update()

# Start generating vegetation
progress = 0
for x in range(int(-SCREEN_WIDTH / 2), int(SCREEN_WIDTH / 2), TILE_SIZE):
    for y in range(int(-SCREEN_HEIGHT / 2), int(SCREEN_HEIGHT / 2), TILE_SIZE):
        tileX = math.floor(x / TILE_SIZE)
        tileY = math.floor(y / TILE_SIZE)
        total_metaball_value = get_total_metaball_value(tileX, tileY)
        random.seed(SEED + progress)

        # determine if a palm tree could be drawn
        can_draw_palm_tree = 0
        for i in range(clamp(math.ceil(total_metaball_value - BEACH_THRESHOLD), 0, 1)): # if the total metaball value is above the beach threshold, there's a chance to draw a palm tree.
            can_draw_palm_tree = 1
        for i in range(clamp(math.ceil(total_metaball_value - LAND_THRESHOLD), 0, 1)): # if the total metaball value is above the land threshold, there's no longer a chance to draw a palm tree, because palm trees don't grow on grass
            can_draw_palm_tree = 0

        # draw the palm tree with a chance, if it could be drawn.
        for i in range(can_draw_palm_tree):
            random_number = random.randint(1, 100)
            for j in range(clamp(random_number - (100 - PALM_TREE_CHANCE), 0, 1)):
                draw_palm_tree(tileX, tileY)

        # determine if a flower could be drawn
        can_draw_flower = 0
        for i in range(clamp(math.ceil(total_metaball_value - LAND_THRESHOLD), 0, 1)): # flowers can be drawn on land/grass.
            can_draw_flower = 1

        # draw the flower with a chance, if it could be drawn
        for i in range(can_draw_flower):
            random_number = random.randint(1, 100)
            for j in range(clamp(random_number - (100 - FLOWER_CHANCE), 0, 1)):
                draw_flower(tileX, tileY)

        # use accumulator pattern on the progress
        progress = progress + 1
        # Normalised progress is the progress of the generation from 0-1, used for draw_loading_screen
        normalised_progress = progress / ((SCREEN_WIDTH / TILE_SIZE) * (SCREEN_HEIGHT / TILE_SIZE))
        for i in range(1 - clamp(progress % 2048, 0, 1)): # only draw every 2048 iterations to save performance
            loading_turtle.clear()
            draw_loading_screen(1, normalised_progress)
            screen.update()

loading_turtle.clear()

## Generate grid
# generate x and y axes
main_turtle.color("#000000")
main_turtle.pensize(1)
main_turtle.penup()
main_turtle.goto(-SCREEN_WIDTH, 0)
main_turtle.pendown()
main_turtle.goto(SCREEN_WIDTH, 0)

main_turtle.penup()
main_turtle.goto(0, SCREEN_HEIGHT)
main_turtle.pendown()
main_turtle.goto(0, -SCREEN_HEIGHT)
main_turtle.penup()

# generate tick marks every 50 pixels
for x in range(0, SCREEN_WIDTH, 50):
    main_turtle.penup()
    main_turtle.goto(x, -5)
    main_turtle.pendown()
    main_turtle.goto(x, 5)

    main_turtle.penup()
    main_turtle.goto(x, -30)
    main_turtle.write(str(x))

for x in range(0, -SCREEN_WIDTH, -50):
    main_turtle.penup()
    main_turtle.goto(x, -5)
    main_turtle.pendown()
    main_turtle.goto(x, 5)

    main_turtle.penup()
    main_turtle.goto(x, -30)
    main_turtle.write(str(x))

for y in range(0, SCREEN_HEIGHT, 50):
    main_turtle.penup()
    main_turtle.goto(-5, y)
    main_turtle.pendown()
    main_turtle.goto(5, y)

    main_turtle.penup()
    main_turtle.goto(-15, y)
    main_turtle.write(str(y), align="right")

for y in range(0, -SCREEN_HEIGHT, -50):
    main_turtle.penup()
    main_turtle.goto(-5, y)
    main_turtle.pendown()
    main_turtle.goto(5, y)

    main_turtle.penup()
    main_turtle.goto(-15, y)
    main_turtle.write(str(y), align="right")

screen.update()

## Receive secret location from player 1
secretX = screen.numinput("Secret Location", "Please put the x coordinate of your secret location.")
secretY = screen.numinput("Secret Location", "Please put the y coordinate of your secret location.")

## Guess loop
total_score = 0
total_distance = 0
closest_distance = math.inf

def get_distance(guessX, guessY):
    """
    Returns the euclidian distance between the secret and the guess.
    """
    distance = math.sqrt((secretX - guessX) ** 2 + (secretY - guessY) ** 2)
    return distance

def get_score(guessX, guessY):
    """
    Returns the score of the guess.
    """
    distance = get_distance(guessX, guessY)
    score = (max(0, 200 - distance) ** 2) / 4000
    return score

def draw_guess(guessX, guessY):
    """
    Draws a strange shape at screen position (guessX, guessY)
    """
    marker_turtle.penup()
    marker_turtle.goto(guessX, guessY)

    marker_turtle.setheading(90)
    for i in range(6):
        marker_turtle.goto(guessX, guessY)
        marker_turtle.pendown()
        for j in range(3):
            marker_turtle.pensize(j + 1)
            marker_turtle.forward(5)
        marker_turtle.right(360 / 6)
        marker_turtle.penup()

marker_turtle = turtle.Turtle()
marker_turtle.hideturtle()
marker_turtle.penup()

for i in range(4):
    guessX = screen.numinput("Guess", "Please put the x coordinate of your guess.")
    guessY = screen.numinput("Guess", "Please put the y coordinate of your guess.")

    # draw guess
    draw_guess(guessX, guessY)

    # draw score and distance of that guess
    marker_turtle.goto(guessX + 25, guessY)
    score = get_score(guessX, guessY)
    distance = get_distance(guessX, guessY)
    marker_turtle.write(f"Guess #{i + 1}: Score: {score:.2f}, Distance: {round(distance)}px")

    # use accumulator pattern to track total score and distance
    total_score = total_score + score
    total_distance = total_distance + distance

    # use min to find the closest distance
    closest_distance = min(closest_distance, distance)

    screen.update()
    time.sleep(2)

## Reveal secret
def draw_smiley(x, y):
    """
    Draws a yellow smiley face at screen position (x, y)
    """
    smiley_radius = 25

    marker_turtle.setheading(0)

    # smiley yellow face
    marker_turtle.penup()
    marker_turtle.goto(x, y - smiley_radius)
    marker_turtle.pencolor("#ffe100")
    marker_turtle.fillcolor("#ffe100")
    marker_turtle.pensize(4)
    marker_turtle.begin_fill()
    marker_turtle.pendown()
    marker_turtle.circle(smiley_radius)
    marker_turtle.end_fill()
    marker_turtle.penup()

    # eyes
    marker_turtle.pencolor("#000000")
    marker_turtle.penup()
    marker_turtle.goto(x - 5, y + 10)
    marker_turtle.pendown()
    marker_turtle.goto(x - 5, y + 2)
    marker_turtle.penup()
    marker_turtle.goto(x + 5, y + 10)
    marker_turtle.pendown()
    marker_turtle.goto(x + 5, y + 2)

    # smile
    marker_turtle.penup()
    marker_turtle.goto(x + smiley_radius - 5, y)
    marker_turtle.setheading(90)
    marker_turtle.pendown()
    marker_turtle.circle(smiley_radius - 5, -180)
    marker_turtle.penup()

draw_smiley(secretX, secretY)

screen.update()

time.sleep(5)

## Game results
# clear all drawings
main_turtle.clear()
marker_turtle.clear()

# Display a black final summary screen
screen.bgcolor("#000000")
main_turtle.color("#ffffff")
main_turtle.goto(0, 100)
main_turtle.write("Final Summary Screen", align="center", font=("Arial", 30, "normal"))

# Display the total score, total distance, best (closest) guess.
main_turtle.goto(0, 0)
main_turtle.write(f"Total Score: {total_score:.2f}", align="center", font=("Arial", 15, "normal"))
main_turtle.goto(0, -50)
main_turtle.write(f"Total Distance: {round(total_distance)}px", align="center", font=("Arial", 15, "normal"))
main_turtle.goto(0, -100)
main_turtle.write(f"Best (closest) Guess: {round(closest_distance)}px", align="center", font=("Arial", 15, "normal"))

# update the screen to display the game's results
screen.update()

## End of your code

# Make a clean exit
screen.exitonclick()