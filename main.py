import sys, pygame

pygame.init()


class Player:
    def __init__(self, position=None, sz=None, img_filename='player.bmp'):

        self.MAX_SPEED = 40

        # Default value for position
        if position is None:
            self.position = [0, 0]
        else:
            self.position = position

        # Velocity and acceleration initializations
        self.velocity = [0, 0]
        self.acceleration = [0, 0]

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


class Game:
    def __init__(self, width=1600, height=800):

        # Create screen for the game
        self.screen_width = width
        self.screen_height = height
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()

        # Initialize dictionary for key presses
        self.key_pressed = {}
        for key in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_DOWN, pygame.K_UP]:
            self.key_pressed[key] = False

        # Load player
        self.player = Player([37.5, 37.5])

    def handle_events(self):

        for event in pygame.event.get():

            # Handle closing event
            if event.type == pygame.QUIT:
                sys.exit()

            # Handle key presses
            if event.type == pygame.KEYDOWN:
                if event.key in self.key_pressed:
                    self.key_pressed[event.key] = True

            # Handle key releases
            if event.type == pygame.KEYUP:
                if event.key in self.key_pressed:
                    self.key_pressed[event.key] = False

    def update_physics(self):

        delta_t = 1/60
        alpha = 7000
        k = 3000

        # Update position (CA model)
        self.player.position[0] += self.player.velocity[0] * delta_t + self.player.acceleration[0] * (delta_t ** 2) / 2
        self.player.position[1] += self.player.velocity[1] * delta_t + self.player.acceleration[1] * (delta_t ** 2) / 2

        # Update velocity (CA model)
        self.player.velocity[0] += self.player.acceleration[0] * delta_t
        self.player.velocity[1] += self.player.acceleration[1] * delta_t

        # Threshold the velocities (this makes the player stop eventually, if no acceleration is given)
        if abs(self.player.velocity[0]) < 10:
            self.player.velocity[0] = 0
        if abs(self.player.velocity[1]) < 10:
            self.player.velocity[1] = 0

        # Update acceleration
        thrust = [self.key_pressed[pygame.K_RIGHT] - self.key_pressed[pygame.K_LEFT],
                  self.key_pressed[pygame.K_DOWN] - self.key_pressed[pygame.K_UP]]
        thrust_mag = (thrust[0]**2 + thrust[1]**2)**0.5
        if thrust_mag > 0:
            self.player.acceleration[0] = alpha * thrust[0]/thrust_mag
            self.player.acceleration[1] = alpha * thrust[1]/thrust_mag
        else:
            self.player.acceleration = [0, 0]

        speed = (self.player.velocity[0]**2 + self.player.velocity[1]**2)**0.5
        if speed > 0.1:
            self.player.acceleration[0] -= self.player.velocity[0] / speed * k
            self.player.acceleration[1] -= self.player.velocity[1] / speed * k

        # Check collisions
        r = self.player.get_rect()
        if r.left < 0:
            self.player.position[0] = r.width / 2
            self.player.velocity[0] = -self.player.velocity[0]*0.8
        if r.top < 0:
            self.player.position[1] = r.height / 2
            self.player.velocity[1] = -self.player.velocity[1]*0.8
        if r.right > self.screen_width:
            self.player.position[0] = self.screen_width - r.width / 2
            self.player.velocity[0] = -self.player.velocity[0]*0.8
        if r.bottom > self.screen_height:
            self.player.position[1] = self.screen_height - r.height / 2
            self.player.velocity[1] = -self.player.velocity[1]*0.8

    def draw_frame(self):
        self.screen.fill((0, 0, 0))
        self.player.draw(self.screen)
        pygame.display.flip()
        self.clock.tick(60)


myGame = Game()

while 1:
    myGame.handle_events()
    myGame.update_physics()
    myGame.draw_frame()

