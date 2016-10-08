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
    
    if direction == 'u':
        return 'l'
    elif direction == 'l':
        return 'd'
    elif direction == 'd':
        return 'r'
    elif direction == 'r':
        return 'u'

def turnRight(direction):
    
    if direction == 'u':
        return 'r'
    elif direction == 'r':
        return 'd'
    elif direction == 'd':
        return 'l'
    elif direction == 'l':
        return 'u'

# Draw line with curved corners
def drawLine(currentDirection, nextDirection):
    global currentPoint
    global direction
    
    if currentDirection == 'u':
        if nextDirection == 'l':
            pygame.draw.line(screen, (255, 255, 255), currentPoint, (currentPoint[0] - 4, currentPoint[1] - 4))
            pygame.draw.line(screen, (255, 255, 255), (currentPoint[0] - 4, currentPoint[1] - 4), (currentPoint[0] - 12, currentPoint[1] - 4))
            currentPoint = (currentPoint[0] - 12, currentPoint[1] - 4)
        elif nextDirection == 'r':
            pygame.draw.line(screen, (255, 255, 255), currentPoint, (currentPoint[0] + 4, currentPoint[1] - 4))
            pygame.draw.line(screen, (255, 255, 255), (currentPoint[0] + 4, currentPoint[1] - 4), (currentPoint[0] + 12, currentPoint[1] - 4))
            currentPoint = (currentPoint[0] + 12, currentPoint[1] - 4)
    
    elif currentDirection == 'l':
        if nextDirection == 'u':
            pygame.draw.line(screen, (255, 255, 255), currentPoint, (currentPoint[0] - 4, currentPoint[1] - 4))
            pygame.draw.line(screen, (255, 255, 255), (currentPoint[0] - 4, currentPoint[1] - 4), (currentPoint[0] - 4, currentPoint[1] - 12))
            currentPoint = (currentPoint[0] - 4, currentPoint[1] - 12)
        elif nextDirection == 'd':
            pygame.draw.line(screen, (255, 255, 255), currentPoint, (currentPoint[0] - 4, currentPoint[1] + 4))
            pygame.draw.line(screen, (255, 255, 255), (currentPoint[0] - 4, currentPoint[1] + 4), (currentPoint[0] - 4, currentPoint[1] + 12))
            currentPoint = (currentPoint[0] - 4, currentPoint[1] + 12)

    elif currentDirection == 'd':
        if nextDirection == 'r':
            pygame.draw.line(screen, (255, 255, 255), currentPoint, (currentPoint[0] + 4, currentPoint[1] + 4))
            pygame.draw.line(screen, (255, 255, 255), (currentPoint[0] + 4, currentPoint[1] + 4), (currentPoint[0] + 12, currentPoint[1] + 4))
            currentPoint = (currentPoint[0] + 12, currentPoint[1] + 4)
        elif nextDirection == 'l':
            pygame.draw.line(screen, (255, 255, 255), currentPoint, (currentPoint[0] - 4, currentPoint[1] + 4))
            pygame.draw.line(screen, (255, 255, 255), (currentPoint[0] - 4, currentPoint[1] + 4), (currentPoint[0] - 12, currentPoint[1] + 4))
            currentPoint = (currentPoint[0] - 12, currentPoint[1] + 4)

    elif currentDirection == 'r':
        if nextDirection == 'u':
            pygame.draw.line(screen, (255, 255, 255), currentPoint, (currentPoint[0] + 4, currentPoint[1] - 4))
            pygame.draw.line(screen, (255, 255, 255), (currentPoint[0] + 4, currentPoint[1] - 4), (currentPoint[0] + 4, currentPoint[1] - 12))
            currentPoint = (currentPoint[0] + 4, currentPoint[1] - 12)
        elif nextDirection == 'd':
            pygame.draw.line(screen, (255, 255, 255), currentPoint, (currentPoint[0] + 4, currentPoint[1] + 4))
            pygame.draw.line(screen, (255, 255, 255), (currentPoint[0] + 4, currentPoint[1] + 4), (currentPoint[0] + 4, currentPoint[1] + 12))
            currentPoint = (currentPoint[0] + 4, currentPoint[1] + 12)

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


