import sys, pygame

pygame.init()


class Player:

    def __init__(self, sz=None, position=(0, 0), img_filename='player.bmp'):

        temp = pygame.image.load(img_filename)
        if sz is None:
            self.img = temp
        else:
            self.img = pygame.transform.scale(temp, sz)

        self.rect = self.img.get_rect()
        self.position = position
        self.rect.center = position

        self.start_speed = 10
        self.max_speed = 40
        self.accel = 1
        self.speed = self.start_speed

    def draw(self, scr):
        scr.blit(self.img, self.rect)


size = width, height = 1600, 800
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()


# Initialize dictionary for key presses
key_pressed = {}
for key in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_DOWN, pygame.K_UP]:
    key_pressed[key] = False

# Load player
player = Player((75, 75))

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
    newx = player.rect.center[0] + player.speed*(key_pressed[pygame.K_RIGHT] - key_pressed[pygame.K_LEFT])
    newy = player.rect.center[1] + player.speed*(key_pressed[pygame.K_DOWN] - key_pressed[pygame.K_UP])
    player.rect.center = (newx, newy)

    # Check collision
    if player.rect.left < 0:
        player.rect.left = 0
    if player.rect.top < 0:
        player.rect.top = 0
    if player.rect.right > width:
        player.rect.right = width
    if player.rect.bottom > height:
        player.rect.bottom = height

    # Update velocity
    if key_pressed[pygame.K_LEFT] or  \
       key_pressed[pygame.K_RIGHT] or \
       key_pressed[pygame.K_UP] or    \
       key_pressed[pygame.K_DOWN]:
        if player.speed <= player.max_speed:
            player.speed += 1
    else:
        player.speed = player.start_speed

    # Update display
    screen.fill((0, 0, 0))
    player.draw(screen)
    pygame.display.flip()