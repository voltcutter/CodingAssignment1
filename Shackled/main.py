# Import the modules
import turtle
import math
import random
import time

## Game Constants
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 450
WINDOW_TITLE = "Hide & Seek"

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
PALM_TREE_CHANCE = 5
PALM_TRUNK_MAX_LEANING_ANGLE = 7
PALM_TRUNK_THICKNESS = 3
PALM_TRUNK_COLOUR = "#421C0A"
PALM_TRUNK_COLOUR_ALT = "#6C3615"
PALM_TRUNK_SEGMENTS = 5
PALM_TRUNK_SEGMENT_LENGTH = 4
PALM_LEAVES_THICKNESS = 2
PALM_LEAVES_COLOUR = "#5FC039"
PALM_LEAVES_SEGMENTS = 3
PALM_LEAVES_SEGMENT_LENGTH = 6
PALM_LEAVES_DROOP = 2
PALM_LEAVES_DROOP_INDEX_OFFSET = -1
PALM_LEAVES_TILT = 0.4
PALM_LEAVES_COUNT_MIN = 3
PALM_LEAVES_COUNT_MAX = 5

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
main_turtle.write("Hide & Seek", align="center", font=("Arial", 50, "normal"))
main_turtle.goto(0, 0)
main_turtle.write("Player 1 must type their secret location in pixels relative to the origin.", align="center", font=("Arial", 20, "normal"))
main_turtle.goto(0, -50)
main_turtle.write("Player 2 must make 4 guesses of the location.", align="center", font=("Arial", 20, "normal"))
main_turtle.goto(0, -100)
main_turtle.write("Good Luck.", align="center", font=("Arial", 20, "normal"))

screen.update()

# time.sleep(5)

main_turtle.clear()
screen.update()

## Generate background
"""
EXPLANATION OF TERRAIN GENERATION:

To generate terrain, we will use a concept called 'metaballs'.
Metaballs are commonly used to create organic looking shapes from just a few points.
It's common in particle simulations to smooth out the shape of the particles, which is where I learned this concept!

A 'metaball' is a point in space that has a value that decreases as the distance to a sample point 'P' increases.
In other words, the metaball value is inversely proportional to the distance.
In this specific game, our metaball function is as follows:

f(x) = k/x

where 'f' represents the metaball function,
      'x' represents the distance between the metaball and 'P',
      'k' represents the metaball multiplier. (defined in the terrain constants)

To determine the 'total metaball value' at P, we will find f(x) for all metaballs and get the sum.
In other words, the sum of all metaball functions at P is defined as the 'total metaball value'.
This value is then used to determine the colour of the tile at P.

If the total metaball value is greater than the beach threshold, the colour is the beach colour.
If the total metaball value is greater than the land threshold, the colour is the land colour.
Otherwise, it's water colour.
"""
# math utility methods
def clamp(x, a, b):
    """
    Clamps x between minimum and maximum
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
    Linearly interpolates between two colours, a and b, by t
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

        total_metaball_value = total_metaball_value + metaball_value
    return total_metaball_value

def determine_colour_of_tile(tileX, tileY):
    """
    Determines the colour of a tile given its coordinates.
    """
    total_metaball_value = get_total_metaball_value(tileX, tileY)

    deepness = 1 - inverse_lerp(DEEP_SEA_THRESHOLD, BEACH_THRESHOLD, total_metaball_value) # calculate deepness of water
    t_value = deepness * 0.5 + 0.5 # adjusts the t value to be within the range [0.5, 1], making it appear more visually appealing
    for i in range(1 - ((x // 2 + y // 2) % 2)): # if the sum of the x // 2 and y // 2 coordinates is even, choose the colour of a slightly deeper depth (this creates a checkboard pattern where each checker is 2 tiles large)
        t_value = clamp(t_value + 0.1, 0, 1)
    colour = blend_colour(SEA_COLOUR_SHALLOW_R, SEA_COLOUR_SHALLOW_G, SEA_COLOUR_SHALLOW_B, SEA_COLOUR_DEEP_R, SEA_COLOUR_DEEP_G, SEA_COLOUR_DEEP_B, t_value)

    # set colour to beach, if the metaball value is above BEACH_THRESHOLD.
    # if total_metaball_value > BEACH_THRESHOLD, the expression will evaluate to a value that is at least 1, which runs the for loop and overwrites the colour to beach colour.
    # otherwise, it will evaluate to a value below 1, which does not run the for loop, and keeps it as sea colour.
    # an if statement is much more optimal here, however, if statements are disallowed.
    for i in range(math.ceil(total_metaball_value - BEACH_THRESHOLD)):
        colour = BEACH_COLOUR
        # same checkboard condition from above
        for j in range(1 - ((x // 2 + y // 2) % 2)):
            colour = BEACH_COLOUR_ALT

    # same condition from above, adjusted for land threshold and land colour
    for i in range(math.ceil(total_metaball_value - LAND_THRESHOLD)):
        colour = LAND_COLOUR
        # same checkboard condition from above
        for j in range(1 - ((x // 2 + y // 2) % 2)):
            colour = LAND_COLOUR_ALT

    return colour

def draw_rectangle(turtle, min_x, min_y, max_x, max_y):
    turtle.penup()
    turtle.goto(min_x, min_y)
    turtle.pendown()
    turtle.goto(max_x, min_y)
    turtle.goto(max_x, max_y)
    turtle.goto(min_x, max_y)
    turtle.penup()

def draw_rectangle_fill(turtle, min_x, min_y, max_x, max_y, fill_colour):
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
        current_displacement_x = 0
        current_displacement_y = 0
        base_displacement_x = PALM_LEAVES_SEGMENT_LENGTH * math.cos(angle)
        base_displacement_y = PALM_LEAVES_SEGMENT_LENGTH * math.sin(angle)
        main_turtle.penup()
        main_turtle.goto(trunk_tip_x, trunk_tip_y)
        main_turtle.pendown()
        for j in range(PALM_LEAVES_SEGMENTS):
            tilted_displacement_y = base_displacement_y * PALM_LEAVES_TILT - PALM_LEAVES_DROOP * (j + PALM_LEAVES_DROOP_INDEX_OFFSET)
            main_turtle.goto(
                trunk_tip_x + current_displacement_x + base_displacement_x,
                trunk_tip_y + current_displacement_y + tilted_displacement_y
            )
            current_displacement_x = current_displacement_x + base_displacement_x
            current_displacement_y = current_displacement_y + tilted_displacement_y
        angle = angle + (math.pi * 2) / palm_leaves_count

    main_turtle.penup()

FLOWER_CHANCE = 10
FLOWER_BUD_COLOUR = "#fff200"
FLOWER_BUD_RADIUS = 5
FLOWER_PETAL_RADIUS = 5
FLOWER_PETAL_OFFSET = 2
FLOWER_PETAL_COUNT = 5

def draw_flower(tileX, tileY):
    """
    Draws a round flower where its centre is at screen position (tileX * TILE_SIZE + TILE_SIZE // 2, tileY * TILE_SIZE + TILE_SIZE // 2)
    """
    x = tileX * TILE_SIZE + TILE_SIZE // 2
    y = tileY * TILE_SIZE + TILE_SIZE // 2

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
    draw_rectangle_fill(loading_turtle, -SCREEN_WIDTH // 2, -SCREEN_HEIGHT // 2, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, "#000000")

    loading_turtle.color("#ffffff")
    loading_turtle.penup()
    loading_turtle.goto(0, -25)
    for i in range(1 - is_generating_vegetation):
        loading_turtle.write("Generating terrain...", align="center", font=("Arial", 50, "normal"))
    for i in range(is_generating_vegetation):
        loading_turtle.write("Generating vegetation...", align="center", font=("Arial", 50, "normal"))

    loading_turtle.goto(0, -50)
    loading_turtle.write("(This may take a few seconds)", align="center", font=("Arial", 14, "normal"))

    loading_turtle.pencolor("#ffffff")
    draw_rectangle(loading_turtle, -100, -90, 100, -70)
    draw_rectangle_fill(loading_turtle, -100, -90, -100 + lerp(0, 200, progress), -70, "#ffffff")

draw_loading_screen(0, 0)
screen.update()

progress = 0
for x in range(int(-SCREEN_WIDTH / 2), int(SCREEN_WIDTH / 2), TILE_SIZE):
    for y in range(int(-SCREEN_HEIGHT / 2), int(SCREEN_HEIGHT / 2), TILE_SIZE):
        tileX = math.floor(x / TILE_SIZE)
        tileY = math.floor(y / TILE_SIZE)
        draw_tile(tileX, tileY)

        progress = progress + 1
        normalised_progress = progress / ((SCREEN_WIDTH / TILE_SIZE) * (SCREEN_HEIGHT / TILE_SIZE))
        for i in range(1 - clamp(progress % 2048, 0, 1)):
            loading_turtle.clear()
            draw_loading_screen(0, normalised_progress)
            screen.update()

progress = 0
for x in range(int(-SCREEN_WIDTH / 2), int(SCREEN_WIDTH / 2), TILE_SIZE):
    for y in range(int(-SCREEN_HEIGHT / 2), int(SCREEN_HEIGHT / 2), TILE_SIZE):
        tileX = math.floor(x / TILE_SIZE)
        tileY = math.floor(y / TILE_SIZE)
        total_metaball_value = get_total_metaball_value(tileX, tileY)
        random.seed(SEED + time.time())

        can_draw_palm_tree = 0
        for i in range(clamp(math.ceil(total_metaball_value - BEACH_THRESHOLD), 0, 1)): # if the total metaball value is above the beach threshold, there's a chance to draw a palm tree.
            can_draw_palm_tree = 1
        for i in range(clamp(math.ceil(total_metaball_value - LAND_THRESHOLD), 0, 1)): # if the total metaball value is above the land threshold, there's no longer a chance to draw a palm tree, because palm trees don't grow on grass
            can_draw_palm_tree = 0

        for i in range(can_draw_palm_tree):
            random_number = random.randint(1, 100)
            for j in range(clamp(random_number - (100 - PALM_TREE_CHANCE), 0, 1)):
                draw_palm_tree(tileX, tileY)

        can_draw_flower = 0
        for i in range(clamp(math.ceil(total_metaball_value - LAND_THRESHOLD), 0, 1)): # flowers can be drawn on land/grass.
            can_draw_flower = 1

        for i in range(can_draw_flower):
            random_number = random.randint(1, 100)
            for j in range(clamp(random_number - (100 - FLOWER_CHANCE), 0, 1)):
                draw_flower(tileX, tileY)

        progress = progress + 1
        normalised_progress = progress / ((SCREEN_WIDTH / TILE_SIZE) * (SCREEN_HEIGHT / TILE_SIZE))
        for i in range(1 - clamp(progress % 2048, 0, 1)):
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
    distance = math.sqrt((secretX - guessX) ** 2 + (secretY - guessY) ** 2)
    return distance

def get_score(guessX, guessY):
    distance = get_distance(guessX, guessY)
    score = (max(0, 200 - distance) ** 2) / 4000
    return score

def draw_guess(guessX, guessY):
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
    draw_guess(guessX, guessY)

    marker_turtle.goto(guessX + 50, guessY)
    score = get_score(guessX, guessY)
    distance = get_distance(guessX, guessY)
    marker_turtle.write(f"Score: {score:.2f}, Distance: {distance:.2f}")

    total_score = total_score + score
    total_distance = total_distance + distance

    closest_distance = min(closest_distance, distance)

    screen.update()
    time.sleep(2)

## Reveal secret
def draw_smiley(x, y):
    smiley_radius = 25

    marker_turtle.setheading(0)

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

    marker_turtle.pencolor("#000000")
    marker_turtle.penup()
    marker_turtle.goto(x - 5, y + 10)
    marker_turtle.pendown()
    marker_turtle.goto(x - 5, y + 2)
    marker_turtle.penup()
    marker_turtle.goto(x + 5, y + 10)
    marker_turtle.pendown()
    marker_turtle.goto(x + 5, y + 2)

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
main_turtle.clear()
marker_turtle.clear()

screen.bgcolor("#000000")
main_turtle.color("#ffffff")
main_turtle.goto(0, 100)
main_turtle.write("Result", align="center", font=("Arial", 30, "normal"))

main_turtle.goto(0, 0)
main_turtle.write(f"Total Score: {total_score}", align="center", font=("Arial", 15, "normal"))
main_turtle.goto(0, -50)
main_turtle.write(f"Total Distance: {total_distance}", align="center", font=("Arial", 15, "normal"))
main_turtle.goto(0, -100)
main_turtle.write(f"Best Distance: {closest_distance}", align="center", font=("Arial", 15, "normal"))

screen.update()

## End of your code

# Make a clean exit
screen.exitonclick()