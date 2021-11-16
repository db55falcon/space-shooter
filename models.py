from pygame.math import Vector2  # this will allow us to perform pygame math on our objects
from utils import load_sprite, wrap_position  # this is so we can load_sprite method in the child class "Ship"
from pygame.transform import rotozoom
import random

DIRECTION_UP = Vector2(0, -1)  # constant that represents the upward direction, This solves negative upward movement


class GameObject:  # this is a simple generic class for our objects (they will all use this)
    def __init__(self, position, sprite, velocity):
        self.position = Vector2(position)  # we convert position to Vector2 (a vector is just two numbers in a pygame
        # format for us to perform useful pygame methods on.
        self.sprite = sprite
        self.radius = sprite.get_width() / 2  # our sprite is a square, so to get the radius for our collision circle
        # we divide by 2
        self.velocity = Vector2(velocity)  # we convert our velocity to Vector2

    def draw(self, surface):
        position = self.position - Vector2(self.radius)  # because we start our position from the center of the object(
        # for collision detection), and pygame uses the top left corner this new position must be calculated as written.
        surface.blit(self.sprite, position)  # now we can blit the sprite to our screen surface

    def move(self, surface):
        move_to = self.position + self.velocity  # we move position according to the speed and direction stored
        # in velocity vector.
        self.position = wrap_position(move_to, surface)  # if object out of bounds wrap_position will return the
        # object to inbounds

    def collides_with(self, other):  # this method will allows detection of another overlapping collision circle
        distance = self.position.distance_to(other.position)  # the distance_to method returns the distance between 2
        # points, the center of the current object and  the center of the object that's passed into "other"
        return distance < self.radius + other.radius  # this will return True boolean if the objects collide


class SpaceShip(GameObject):
    ROTATION_SPEED = 3  # constant represents number of degrees the ship will rotate for each event
    ACCELERATION = 0.08  # be careful with this number as ship can become uncontrollable
    DE_ACCELERATION = -0.08

    def __init__(self, position):
        self.direction = Vector2(DIRECTION_UP)  # direction attribute will equal DIRECTION_UP with Vector applied
        super().__init__(position, load_sprite("spaceship3"), Vector2(0))  # inheriting from Game_Object with super,
        # pass in our load_sprite method and set default specific to SpaceShip class

    def rotate(self, clockwise=True):  # method needed for the rotation math
        sign = 1 if clockwise else -1  # dealing with rotation math, we must multiply by -1 for counter clockwise
        angle = self.ROTATION_SPEED * sign
        self.direction.rotate_ip(angle)  # we use the rotate_ip method on the angle

    def accelerate(self):
        self.velocity += self.direction * self.ACCELERATION  # we simply add these results to our velocity

    def de_accelerate(self):
        self.velocity += self.direction * self.DE_ACCELERATION

    def draw(self, surface):  # we must draw according to the angle
        angle = self.direction.angle_to(DIRECTION_UP)
        rotated_surface = rotozoom(self.sprite, angle, 1.0)  # rotozoom method handles both the rotation and scaling
        # of sprite at the same time, we pass in the scale factor as our last argument
        rotated_surface_size = Vector2(rotated_surface.get_size())  # returns a new bounding box to avoid clipping
        # with .get_size method

        blit_position = self.position - rotated_surface_size * 0.5  # use our bounding box instead of the radius
        surface.blit(rotated_surface, blit_position)  # blitting to screen


class Rock(GameObject):
    MIN_START_GAP = 250  # we will use this to specify the distance between the ship and our randomly generated rocks
    MINIMUM_SPEED = 1
    MAXIMUM_SPEED = 3

    def __init__(self, surface, ship_position):
        while True:  # this is kind of a brute force position generator, we will generate until a valid position is
            # found
            position = Vector2(
                random.randrange(surface.get_width()),
                random.randrange(surface.get_height()),
            )
            if position.distance_to(ship_position) > self.MIN_START_GAP:
                break
        speed = random.randint(self.MINIMUM_SPEED, self.MAXIMUM_SPEED)
        angle = random.randint(0, 360)
        velocity = Vector2(speed, 0).rotate(angle)
        super().__init__(position, load_sprite("asteroid2"), velocity)


