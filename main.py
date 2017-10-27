import sys, pygame

pygame.init()


class Player:
    def __init__(self, position=None, sz=None, img_filename='player.bmp'):

        self.MAX_SPEED = 2000

        # Default value for position
        if position is None:
            self.position = [0, 0]
        else:
            self.position = position

        # Velocity and acceleration initializations
        self.velocity = [0, 0]
        self.acceleration = [0, 0]

        # Load image and optionally resize it
        temp = pygame.image.load(img_filename).convert()
        if sz is None:
            self.img = temp
        else:
            self.img = pygame.transform.scale(temp, sz)

        # Crosshair initialization
        self.crosshair = [200, 200]
        temp = pygame.image.load('crosshair.bmp').convert()
        self.crosshair_img = pygame.transform.scale(temp, (70, 70))
        self.crosshair_img.set_colorkey((0, 0, 0))

    # Returns rectangle around the player image
    def get_rect(self):
        r = self.img.get_rect()
        r.center = (self.position[0], self.position[1])
        return r

    # Updates the state of the player, depending on which action(s) was(were) taken in this time step
    def update(self, actions, delta_t):
        alpha = 20000
        k = 3000

        # Update position (CA model)
        self.position[0] += self.velocity[0] * delta_t + self.acceleration[0] * (delta_t ** 2) / 2
        self.position[1] += self.velocity[1] * delta_t + self.acceleration[1] * (delta_t ** 2) / 2

        # Update velocity (CA model)
        self.velocity[0] += self.acceleration[0] * delta_t
        self.velocity[1] += self.acceleration[1] * delta_t

        # Update acceleration
        thrust = [actions['right'] - actions['left'],
                  actions['down'] - actions['up']]
        thrust_mag = (thrust[0] ** 2 + thrust[1] ** 2) ** 0.5
        if thrust_mag > 0:
            self.acceleration[0] = alpha * thrust[0] / thrust_mag
            self.acceleration[1] = alpha * thrust[1] / thrust_mag
        else:
            self.acceleration = [0, 0]

        # Limit maximum speed
        speed = (self.velocity[0] ** 2 + self.velocity[1] ** 2) ** 0.5
        if speed > self.MAX_SPEED:
            limiting_factor = self.MAX_SPEED/speed
            self.velocity[0] *= limiting_factor
            self.velocity[1] *= limiting_factor

        # Threshold the velocities to zero (this makes the player stop eventually, if no acceleration is given)
        if speed < 30:
            self.velocity = [0, 0]

        # Add friction-like component
        if speed > 0.1:
            self.acceleration[0] -= self.velocity[0] / speed * k
            self.acceleration[1] -= self.velocity[1] / speed * k

        # Update crosshair position
        if actions['move_ch']:
            self.crosshair = actions['move_ch']
        else:
            beta = 30
            self.crosshair[0] += beta * (actions['ch_right'] - actions['ch_left'])
            self.crosshair[1] += beta * (actions['ch_down'] - actions['ch_up'])

    # Draws the player and its crosshair to the screen
    def draw(self, scr):
        scr.blit(self.img, self.get_rect())

        r_crosshair = self.crosshair_img.get_rect()
        r_crosshair.center = self.crosshair
        scr.blit(self.crosshair_img, r_crosshair)


class Game:

    def __init__(self, width=1600, height=800):

        # Create screen for the game
        self.screen_width = width
        self.screen_height = height
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()

        # Initialize dictionary for key presses
        self.key_pressed = {}
        for key in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_DOWN, pygame.K_UP,
                    pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d]:
            self.key_pressed[key] = False

        # Load player
        self.players = []

    def add_player(self, position=None):
        if position is None:
            position = [0, 0]
        self.players.append(Player(position))

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

        for player in self.players:

            # Decide actions for player
            action_names = ['up', 'down', 'left', 'right', 'ch_up', 'ch_down', 'ch_left', 'ch_right']
            key_bindings = [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT,
                            pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d]
            actions = {}
            for action_name, key_binding in zip(action_names, key_bindings):
                actions[action_name] = self.key_pressed[key_binding]
            actions['move_ch'] = pygame.mouse.get_pos()

            # Update player using chosen actions
            player.update(actions, delta_t)

            # Limit crosshair position
            if player.crosshair[0] < 0:
                player.crosshair[0] = 0
            if player.crosshair[0] > self.screen_width:
                player.crosshair[0] = self.screen_width
            if player.crosshair[1] < 0:
                player.crosshair[1] = 0
            if player.crosshair[1] > self.screen_height:
                player.crosshair[1] = self.screen_height

            # Check collisions with walls
            r = player.get_rect()
            if r.left < 0:
                player.position[0] = r.width / 2
                player.velocity[0] = -player.velocity[0]*0.8
            if r.top < 0:
                player.position[1] = r.height / 2
                player.velocity[1] = -player.velocity[1]*0.8
            if r.right > self.screen_width:
                player.position[0] = self.screen_width - r.width / 2
                player.velocity[0] = -player.velocity[0]*0.8
            if r.bottom > self.screen_height:
                player.position[1] = self.screen_height - r.height / 2
                player.velocity[1] = -player.velocity[1]*0.8

    def draw_frame(self):
        self.screen.fill((0, 0, 0))
        for player in self.players:
            player.draw(self.screen)
        pygame.display.flip()
        self.clock.tick(60)


myGame = Game()
myGame.add_player([37.5, 37.5])
myGame.add_player([500, 500])

while 1:
    myGame.handle_events()
    myGame.update_physics()
    myGame.draw_frame()

