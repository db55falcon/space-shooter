import pygame
from utils import load_sprite
from models import Rock, SpaceShip


class SpaceAsteroids:
    def __init__(self):
        pygame.init()  # we must initialize our pygame inside of our __init__ method
        pygame.display.set_caption("Space Asteroids")  # This method simply displays our games title
        self.clock = pygame.time.Clock()  # creating our clock attribute for FPS control

        self.screen = pygame.display.set_mode((800, 600))  # we set our screen size in pixels, passed in as a tuple
        self.background = load_sprite("space2", False)  # using the load_sprite function to pass in our background,
        # because this is a background it will remain False for using convert_alpha

        bg_music = pygame.mixer.Sound("assets/sounds/bg.wav")  # we are loading our sound asset into bg_music variable
        bg_music.play(loops=-1)  # we initiate play sound and specify our loops, we specify -1 for infinite loops

        self.ship = SpaceShip((400, 300))  # ship will start in screen middle position, we pass in
        # our sprite, and set our velocity

        self.rocks = [Rock(self.screen, self.ship.position) for _ in range(4)]  # this is using list comprehension to
        # call the rock constructor 4 times

        self.collision_counter = 0  # this will count our collisions

    def main_loop(self):
        while True:  # this loop seems infinite but our first method call will check for a quit event.
            self._handle_input()  # checking quit event
            self._game_logic()
            self._draw()

    def _handle_input(self):
        for event in pygame.event.get():  # quits on X clickable button
            if event.type == pygame.QUIT:
                quit()

        is_key_pressed = pygame.key.get_pressed()  # bringing in our key press events
        if is_key_pressed[pygame.K_ESCAPE]:  # allows us to quit with our escape key
            quit()
        elif is_key_pressed[pygame.K_d]:
            self.ship.rotate(clockwise=True)  # we multiply by 1 for clockwise
        elif is_key_pressed[pygame.K_a]:
            self.ship.rotate(clockwise=False)  # we multiply by -1 for counterclockwise
        elif is_key_pressed[pygame.K_w]:  # forward acceleration w key bind
            self.ship.accelerate()
        elif is_key_pressed[pygame.K_s]:  # reverse acceleration s key bind
            self.ship.de_accelerate()

    @property  # this will return a list of all objects in the game
    def game_objects(self):
        return [*self.rocks, self.ship]  # we break down the rocks and then pass in the ship

    def _game_logic(self):  # we iterate over each object in the game and call their move method
        for obj in self.game_objects:
            obj.move(self.screen)

    def _draw(self):
        self.screen.blit(self.background, (0, 0))  # we are blitting our background to the screen at position 0,0,

        for obj in self.game_objects:  # we iterate over each object and call their draw method.
            obj.draw(self.screen)

        pygame.display.flip()  # flips the buffer to our screen (we always draw to a buffer first)
        self.clock.tick(60)  # here we pass in our FPS, or in this case 60, must be the last method of the entire loop
