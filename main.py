import sys, pygame

pygame.init()


class Player:
    def __init__(self, sz=None, position=None, img_filename='player.bmp'):

        self.START_SPEED = 10
        self.MAX_SPEED = 40

        # Default value for position
        if position is None:
            self.position = [0, 0]

        # Speed and acceleration initializations
        self.speed = self.START_SPEED
        self.accel = 1

        # Load image and optionally resize it
        temp = pygame.image.load(img_filename)
        if sz is None:
            self.img = temp
        else:
            self.img = pygame.transform.scale(temp, sz)

    # Returns rectangle around the player image
    def get_rect(self):
        r = self.img.get_rect()
        r.center = (self.position[0], self.position[1])
        return r

    # Draws the player to the screen
    def draw(self, scr):
        scr.blit(self.img, self.get_rect())


size = width, height = 1600, 800
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

# Initialize dictionary for key presses
key_pressed = {}
for key in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_DOWN, pygame.K_UP]:
    key_pressed[key] = False

# Load player
player = Player([75, 75])

while 1:
    clock.tick(60)

    for event in pygame.event.get():

        # Handle closing event
        if event.type == pygame.QUIT:
            sys.exit()

        # Handle key presses
        if event.type == pygame.KEYDOWN:
            if event.key in key_pressed:
                key_pressed[event.key] = True

        # Handle key releases
        if event.type == pygame.KEYUP:
            if event.key in key_pressed:
                key_pressed[event.key] = False

    # Update position
    player.position[0] += player.speed*(key_pressed[pygame.K_RIGHT] - key_pressed[pygame.K_LEFT])
    player.position[1] += player.speed*(key_pressed[pygame.K_DOWN] - key_pressed[pygame.K_UP])

    # Check collision
    r = player.get_rect()
    if r.left < 0:
        player.position[0] = r.width / 2
    if r.top < 0:
        player.position[1] = r.height / 2
    if r.right > width:
        player.position[0] = width - r.width/2
    if r.bottom > height:
        player.position[1] = height - r.height/2

    # Update velocity
    if key_pressed[pygame.K_LEFT] or  \
       key_pressed[pygame.K_RIGHT] or \
       key_pressed[pygame.K_UP] or    \
       key_pressed[pygame.K_DOWN]:
        if player.speed <= player.MAX_SPEED:
            player.speed += 1
    else:
        player.speed = player.START_SPEED

    # Update display
    screen.fill((0, 0, 0))
    player.draw(screen)
    pygame.display.flip()