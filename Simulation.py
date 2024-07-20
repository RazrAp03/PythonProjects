import pygame
import random
import math

# Initialize pygame
pygame.init()

# Constants
WINDOW_WIDTH = 810
WINDOW_HEIGHT = 800
ENTITY_RADIUS = 5
SPEED = 3
DETECTION_RADIUS = 100
CONVERSION_RADIUS = 20
EDGE_AVOID_RADIUS = 50
REPULSION_RADIUS = 20
ICON_WIDTH = 30
ICON_HEIGHT = 30

# Load and scale entity icons
rock_icon = pygame.image.load('rock.png')
rock_icon = pygame.transform.scale(rock_icon, (ICON_WIDTH, ICON_HEIGHT))

paper_icon = pygame.image.load('paper.png')
paper_icon = pygame.transform.scale(paper_icon, (ICON_WIDTH, ICON_HEIGHT))

scissors_icon = pygame.image.load('sciss.png')
scissors_icon = pygame.transform.scale(scissors_icon, (ICON_WIDTH, ICON_HEIGHT))

# Initialize pygame mixer
pygame.mixer.init()

# Load sound files
rock_sound = pygame.mixer.Sound("rockSound.mp3")
paper_sound = pygame.mixer.Sound("paperSound.mp3")
scissors_sound = pygame.mixer.Sound("scissors.mp3")

class Entity:
    def __init__(self, x, y, tribe):
        self.x = x
        self.y = y
        self.tribe = tribe

    def move_towards(self, target_x, target_y):
        angle = math.atan2(target_y - self.y, target_x - self.x)        # atan2->Return the arc tangent (measured in radians) of y/x.
        self.x += (SPEED + random.uniform(-0.3, 0.3)) * math.cos(angle)
        self.y += (SPEED + random.uniform(-0.3, 0.3)) * math.sin(angle)
        self.avoid_edges()

    def move_away_from(self, target_x, target_y):
        angle = math.atan2(target_y - self.y, target_x - self.x)
        self.x -= (SPEED + random.uniform(-0.3, 0.3)) * math.cos(angle)
        self.y -= (SPEED + random.uniform(-0.3, 0.3)) * math.sin(angle)
        self.avoid_edges()

    def distance_to(self, other):
        return math.sqrt((self.x-other.x)**2 + (self.y-other.y)**2)

    def repel_from(self, other):
        if self.distance_to(other) < REPULSION_RADIUS:
            self.move_away_from(other.x, other.y)

    def draw(self): # The screen.blit() function is used to draw various images onto the game window. 
                    #This allows you to display objects, backgrounds, icons, or any other graphical elements within the game.
        if self.tribe == 'rock':
            screen.blit(rock_icon, (self.x - ICON_WIDTH//2, self.y - ICON_HEIGHT//2))
        elif self.tribe == 'paper':
            screen.blit(paper_icon, (self.x - ICON_WIDTH//2, self.y - ICON_HEIGHT//2))
        else:
            screen.blit(scissors_icon, (self.x - ICON_WIDTH//2, self.y - ICON_HEIGHT//2))

    def avoid_edges(self):
        if self.x < EDGE_AVOID_RADIUS:
            self.move_towards(self.x + EDGE_AVOID_RADIUS, self.y)
        elif self.x > WINDOW_WIDTH - EDGE_AVOID_RADIUS:
            self.move_towards(self.x - EDGE_AVOID_RADIUS, self.y)
        if self.y < EDGE_AVOID_RADIUS:
            self.move_towards(self.x, self.y + EDGE_AVOID_RADIUS)
        elif self.y > WINDOW_HEIGHT - EDGE_AVOID_RADIUS:
            self.move_towards(self.x, self.y - EDGE_AVOID_RADIUS)

entities = [Entity(random.randint(0, WINDOW_WIDTH), random.randint(0, WINDOW_HEIGHT), 'rock') for _ in range(50)] + \
           [Entity(random.randint(0, WINDOW_WIDTH), random.randint(0, WINDOW_HEIGHT), 'paper') for _ in range(50)] + \
           [Entity(random.randint(0, WINDOW_WIDTH), random.randint(0, WINDOW_HEIGHT), 'scissors') for _ in range(50)]


def adjust_movement(screen):
    for entity in entities:
        if entity.tribe == 'rock':
            targets = [e for e in entities if e.tribe == 'scissors']
            threats = [e for e in entities if e.tribe == 'paper']
        elif entity.tribe == 'paper':
            targets = [e for e in entities if e.tribe == 'rock']
            threats = [e for e in entities if e.tribe == 'scissors']
        else:
            targets = [e for e in entities if e.tribe == 'paper']
            threats = [e for e in entities if e.tribe == 'rock']

        for other in entities:
            if entity != other and entity.tribe == other.tribe:
                entity.repel_from(other)

        closest_target = min(targets, key=entity.distance_to, default=None)
        closest_threat = min(threats, key=entity.distance_to, default=None)

        if closest_threat and entity.distance_to(closest_threat) < DETECTION_RADIUS:
            entity.move_away_from(closest_threat.x, closest_threat.y)
        elif closest_target and entity.distance_to(closest_target) < DETECTION_RADIUS:
            entity.move_towards(closest_target.x, closest_target.y)
            if entity.distance_to(closest_target) < CONVERSION_RADIUS:
                closest_target.tribe = entity.tribe
        else:
            entity.move_towards(random.randint(0, WINDOW_WIDTH), random.randint(0, WINDOW_HEIGHT))

        entity.draw()

'''pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT)):

This function is used to create a game window or display surface with a specified width and height.
It takes a tuple as an argument, where the first element is the width of the window, and the second element is the height.
In your code, WINDOW_WIDTH and WINDOW_HEIGHT are constants that define the dimensions of the game window.'''

'''pygame.display.set_caption("Rock Paper Scissors Simulation"):

This function sets the title or caption for the game window. The caption appears at the top of the window's frame.
It takes a single string argument, which is the text you want to display as the window's caption.
In your code, it sets the caption of the game window to "Rock Paper Scissors Simulation."'''

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Rock Paper Scissors Simulation")
clock = pygame.time.Clock()
running = True

# Game loop
while running:
    screen.fill((0,0,0))
    adjust_movement(screen)

    # Initialize counters for each tribe
    rock_count = 0
    paper_count = 0
    scissors_count = 0

    # Count entities for each tribe
    for entity in entities:
        if entity.tribe == 'rock':
            rock_sound.play()
            rock_count += 1
        elif entity.tribe == 'paper':
            paper_sound.play()
            paper_count += 1
        elif entity.tribe == 'scissors':
            scissors_sound.play()
            scissors_count += 1

    # Render text surfaces for counts
    font = pygame.font.SysFont(None, 36)
    rock_text = font.render("Rock: " + str(rock_count), True, (255, 255, 255))
    paper_text = font.render("Paper: " + str(paper_count), True, (255, 255, 255))
    scissors_text = font.render("Scissors: " + str(scissors_count), True, (255, 255, 255))

    # Blit text surfaces onto the screen
    screen.blit(rock_text, (10, 10))
    screen.blit(paper_text, (10, 50))
    screen.blit(scissors_text, (10, 90))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    winner_text = None
    if rock_count == len(entities):
        winner_text = "Rock"
    elif paper_count == len(entities):
        winner_text = "Paper"
    elif scissors_count == len(entities):
        winner_text = "Scissors"
    
    if winner_text:
        pygame.font.init()
        font_large = pygame.font.Font(None, 100)
        font_small = pygame.font.Font(None, 74)

        winner_title_surface = font_large.render("Winner!", True, pygame.Color("#6aff9b"))
        tribe_name_surface = font_small.render(winner_text, True, (255, 255, 255))

        padding = 20
        box_width = max(winner_title_surface.get_width(), tribe_name_surface.get_width()) + 2 * padding
        box_height = winner_title_surface.get_height() + tribe_name_surface.get_height() + 3 * padding

        # Draw the black box
        pygame.draw.rect(screen, (0, 0, 0), (WINDOW_WIDTH // 2 - box_width // 2, WINDOW_HEIGHT // 2 - box_height // 2, box_width, box_height))

        # Blit the texts onto the screen
        screen.blit(winner_title_surface, (WINDOW_WIDTH // 2 - winner_title_surface.get_width() // 2, WINDOW_HEIGHT // 2 - box_height // 2 + padding))
        screen.blit(tribe_name_surface, (WINDOW_WIDTH // 2 - tribe_name_surface.get_width() // 2, WINDOW_HEIGHT // 2 + padding))

        pygame.display.flip()
        pygame.time.wait(10000)
        running = False

    pygame.display.flip()
    clock.tick(60)

pygame.quit()


                                                    # DOCUMENTATION 


'''Loading and Scaling Images: The code loads and scales three images - background_image, rock_icon, paper_icon, 
and scissors_icon - which are used for the game's visuals.'''

'''Entity Class: The Entity class is defined to represent the entities in the simulation.
It has methods to move towards or away from a target, calculate the distance to another entity, repel from other entities, 
and draw the entity on the screen.'''

'''Creating Entities: A list of Entity objects is created with random positions and assigned to one of three tribes: 'rock,' 
'paper,' or 'scissors.' This list represents the initial state of the simulation.'''

'''adjust_movement Function: This function handles the movement logic for entities based on their tribes and interactions.
It calculates the closest target and threat entities and adjusts the movement of the current entity accordingly.
Entities of the same tribe repel each other to avoid overlapping.
The function also handles edge avoidance and updates the entity's position on the screen.'''

'''Game Loop: The main game loop runs continuously until the running variable becomes False.
It continuously updates the screen, adjusts entity movement, and checks for a winner based on the counts of each tribe.
If there is a winner, it displays a message with the winning tribe and exits the loop.'''