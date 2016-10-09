# Generates a Sierpinski Curve
import pygame

# Set value for n
n = 4

# Set window dimensions
dimensions = (800, 800)

# Initialise other variables
currentPoint = ((dimensions[0] / 2) + (0.5 * 2 * 2 ** n * 16), (dimensions[1] / 2) - (0.5 * 2 * 2 ** n * 16))
currentDirection = 'u'
nextDirection = ''
n = 2 ** n

# Recursive ZIG and ZAG functions
def ZIG(n):
    global currentDirection
    global nextDirection
    
    # Draw the lines once n gets to 1, or call functions again until n = 1
    if n == 1:
        nextDirection = turnLeft(currentDirection)
        drawLine(currentDirection, nextDirection)
        currentDirection = nextDirection
        nextDirection = turnLeft(currentDirection)
        drawLine(currentDirection, nextDirection)
        currentDirection = nextDirection
    else:
        ZIG(n/2)
        ZAG(n/2)
        ZIG(n/2)
        ZAG(n/2)

def ZAG(n):
    global currentDirection
    global nextDirection
    
    # Draw the lines once n gets to 1, or call functions again until n = 1
    if n == 1:
        nextDirection = turnRight(currentDirection)
        drawLine(currentDirection, nextDirection)
        currentDirection = nextDirection
        nextDirection = turnRight(currentDirection)
        drawLine(currentDirection, nextDirection)
        currentDirection = nextDirection
        nextDirection = turnLeft(currentDirection)
        drawLine(currentDirection, nextDirection)
        currentDirection = nextDirection
    else:
        ZAG(n/2)
        ZAG(n/2)
        ZIG(n/2)
        ZAG(n/2)

# Convert directions
def turnLeft(direction):
    
    directions = ['u', 'l', 'd', 'r']
    index = directions.index(direction)
    if index == 3: index = -1
    return directions[index + 1]

def turnRight(direction):
    
    directions = ['u', 'r', 'd', 'l']
    index = directions.index(direction)
    if index == 3: index = -1
    return directions[index + 1]

# Draw line with curved corners
def drawLine(currentDirection, nextDirection):
    global currentPoint
    global direction
    
    directions = []
    order = []
    
    # Draw corner diagonal
    if (currentDirection == 'u' and nextDirection == 'l') or (currentDirection == 'l' and nextDirection == 'u'):
        directions = [-1, -1]
    elif (currentDirection == 'u' and nextDirection == 'r') or (currentDirection == 'r' and nextDirection == 'u'):
        directions = [1, -1]
    elif (currentDirection == 'd' and nextDirection == 'l') or (currentDirection == 'l' and nextDirection == 'd'):
        directions = [-1, 1]
    elif (currentDirection == 'd' and nextDirection == 'r') or (currentDirection == 'r' and nextDirection == 'd'):
        directions = [1, 1]
    
    pygame.draw.line(screen, (255, 255, 255), currentPoint, (currentPoint[0] + directions[0] * 4, currentPoint[1] + directions[1] * 4))

    # Draw straight line part
    if currentDirection == 'u' or currentDirection == 'd':
        order = [12, 4]
    else:
        order = [4, 12]
    
    pygame.draw.line(screen, (255, 255, 255), (currentPoint[0] + directions[0] * 4, currentPoint[1] + directions[1] * 4), (currentPoint[0] + directions[0] * order[0], currentPoint[1] + directions[1] * order[1]))
    
    # Save current point
    currentPoint = (currentPoint[0] + directions[0] * order[0], currentPoint[1] + directions[1] * order[1])

# Initialise screen
screen = pygame.display.set_mode(dimensions)
screen.fill((0, 0, 0))

# Call functions
ZIG(n)
ZIG(n)

# Keep window open until closed
pygame.display.flip()
running = True

while running:
    event = pygame.event.poll()
    if event.type == pygame.QUIT:
        running = False
