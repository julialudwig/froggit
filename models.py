"""
Models module for Froggit

This module contains the model classes for the Frogger game. Anything that you
interact with on the screen is model: the frog, the cars, the logs, and so on.

Just because something is a model does not mean there has to be a special class for
it. Unless you need something special for your extra gameplay features, cars and logs
could just be an instance of GImage that you move across the screen. You only need a new
class when you add extra features to an object.

That is why this module contains the Frog class.  There is A LOT going on with the
frog, particularly once you start creating the animation coroutines.

If you are just working on the main assignment, you should not need any other classes
in this module. However, you might find yourself adding extra classes to add new
features.  For example, turtles that can submerge underneath the frog would probably
need a custom model for the same reason that the frog does.

If you are unsure about  whether to make a new class or not, please ask on Piazza. We
will answer.

# Julia Ludwig (jal545)
# 12/21/20
"""
from consts import *
from game2d import *

# PRIMARY RULE: Models are not allowed to access anything in any module other than
# consts.py.  If you need extra information from a lane or level object, then it
# should be a parameter in your method.


class Frog(GSprite):         # You will need to change this by Task 3
    """
    A class representing the frog

    The frog is represented as an image (or sprite if you are doing timed animation).
    However, unlike the obstacles, we cannot use a simple GImage class for the frog.
    The frog has to have additional attributes (which you will add).  That is why we
    make it a subclass of GImage.

    When you reach Task 3, you will discover that Frog needs to be a composite object,
    tracking both the frog animation and the death animation.  That will like caused
    major modifications to this class.
    """
    # LIST ALL HIDDEN ATTRIBUTES HERE
    #
    #Attribute _frogvisible: whether the frog is visible
    #Inavariant: must be a bool
    #
    #Attribute _skullvisible: whether the skull is visible
    #Inavariant: must be a bool
    #
    #Attribute _frog: the frog sprite
    #Inavariant: must be a GSprite
    #
    #Attribute _skull: the death sprite
    #Invariant: must be a GSprite
    #
    #Attribute _jumpSound: the sound played during jump
    #Invariant: must be a Sound object

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def isFrogVisible(self):
        """
        returns True if the Frog is visible, else False
        """
        return self._frogvisible

    def setFrogVisibility(self,value):
        """
        Sets the Frog's visibility

        True means the Frog is visible, False is invisible

        Parameter value: whether the Frog is visible
        Precondition: must be a bool
        """
        assert isinstance(value,bool), repr(value)+' is not a bool'

        self._frogvisible = value

    def setFrame(self,value):
        """
        Sets the Frog sprite's frame
        """
        self.frame = value

    def getFrog(self):
        """
        returns the GSprite for the Frog
        """
        return self._frog

    # INITIALIZER TO SET FROG POSITION
    def __init__(self, x, y, hitbox_dict):
        """
        Initializes the Frog object

        Parameter self: the Frog object to initialize
        Precondition: must be a Frog object

        Parameter x: the x-coordinate for the grid position of the Frog
        Precondition: x >=0 and is an int

        Parameter y: the y-coordinate for the grid position of Frog
        Precondition: y >=0 and is an int

        Parameter hitbox_dict: dictionary of all image hitboxes
        Precondition: must be a dict
        """
        x_pixel = (x+0.5)*GRID_SIZE
        y_pixel = (y+0.5)*GRID_SIZE
        frog_hitboxes = tuple(hitbox_dict['sprites']['frog']['hitboxes'])
        frog_format = tuple(hitbox_dict['sprites']['frog']['format'])
        frog_source = hitbox_dict['sprites']['frog']['file']

        super().__init__(source = frog_source,
                             x = x_pixel,
                             y = y_pixel,
                             angle = FROG_NORTH,
                             hitboxes = frog_hitboxes,
                             format = frog_format,
                             frame = FROG_REST)

        self._jumpSound = Sound(CROAK_SOUND)
        #skull_format = tuple(hitbox_dict['sprites']['frog']['format'])
        #skull_source = hitbox_dict['sprites'][DEATH_SPRITE]['file']

        #self._skull = super().__init__(source = skull_source,
        #                     x = x_pixel,
        #                     y = y_pixel,
        #                     #angle = FROG_NORTH,
        #                     hitboxes = None,
        #                     format = skull_format)
        self._frogvisible = True
        #self._skullvisible = False

    # ADDITIONAL METHODS (DRAWING, COLLISIONS, MOVEMENT, ETC)
    #def draw(self,view):
        #if self._frogvisible: #and not self._frog is None:
            #self.draw(view)
        #if self._skullvisible and not self._skull is None:
        #    self._skull.draw(view)

    def animateSlide(self,dt,direction):
        """
        Animates a Frog movement over FROG_SPEED seconds using coroutine

        Parameter dt: The time since the last animation frame.
        Precondition: dt is a float.

        Parameter direction: the direction to slide
        Precondition: direction is a string and one of 'up','down','right','left'
        """
        initial_y = self.y
        final_y = self._determineFinalY(direction)
        initial_x = self.x
        final_x = self._determineFinalX(direction)

        if final_y == initial_y:
            steps = (final_x - initial_x) / FROG_SPEED
            animating = True
            self._jumpSound.play()
            while animating:
                dt = (yield)
                amount = steps*dt
                self.x = self.x+ amount
                if abs(self.x-initial_x) >= GRID_SIZE:
                    self.x = final_x
                    animating = False
                self._determineXFrame(initial_x,final_x,direction)
        elif final_x == initial_x:
            steps = (final_y - initial_y) / FROG_SPEED
            animating = True
            self._jumpSound.play()
            while animating:
                dt = (yield)
                amount = steps*dt
                self.y = self.y + amount
                if abs(self.y-initial_y) >= GRID_SIZE:
                    self.y = final_y
                    animating = False
                self._determineYFrame(initial_y,final_y,direction)

    def _determineFinalX(self,direction):
        """
        Helper for animateSlide, determines final x-value

        Parameter direction: the direction to slide
        Precondition: direction is a string and one of 'up','down','right','left'
        """
        initial_x = self.x

        if direction == 'left':
            final_x = initial_x - GRID_SIZE
        elif direction == 'right':
            final_x = initial_x +GRID_SIZE
        else:
            final_x = initial_x

        return final_x

    def _determineFinalY(self,direction):
        """
        Helper for animateSlide

        Determines final y-value

        Parameter direction: the direction to slide
        Precondition: direction is a string and one of 'up','down','right','left'
        """
        initial_y = self.y
        if direction == 'up':
            final_y = initial_y + GRID_SIZE
        elif direction == 'down':
            final_y = initial_y - GRID_SIZE
        else:
            final_y = initial_y
        return final_y

    def _determineXFrame(self,initial_x,final_x,direction):
        """
        Helper for animateSlide, determines the frame during frog jump in x

        Parameter initial_x: the starting x during the jump
        Precondition: must be a number (int of float)

        Parameter final_x: the final x of the jump
        Precondition: must be a number (int of float)

        Parameter direction: the direction to slide
        Precondition: direction is a string and one of 'up','down','right','left'
        """
        if final_x - initial_x != 0:
            frac_x = 2*(self.x - initial_x)/(final_x - initial_x)
            if frac_x < 1:
                if direction == 'right' or direction == 'left':
                    frame = FROG_REST+frac_x*(FROG_STRETCHED-FROG_REST)
                    self.frame = round(frame)
            else:
                frac_x = frac_x - 1
                if direction == 'right' or direction == 'left':
                    frame = FROG_STRETCHED+frac_x*(FROG_REST-FROG_STRETCHED)
                    self.frame = round(frame)

    def _determineYFrame(self,initial_y,final_y,direction):
        """
        Helper for animateSlide, determines the frame during frog jump in y

        Parameter initial_x: the starting x during the jump
        Precondition: must be a number (int of float)

        Parameter final_x: the final x of the jump
        Precondition: must be a number (int of float)

        Parameter direction: the direction to slide
        Precondition: direction is a string and one of 'up','down','right','left'
        """
        if final_y - initial_y != 0:
            frac_y = 2*(self.y - initial_y)/(final_y - initial_y)
            if frac_y < 1:
                if direction == 'up' or direction == 'down':
                    frame = FROG_REST+frac_y*(FROG_STRETCHED-FROG_REST)
                    self.frame = round(frame)
            else:
                frac_y = frac_y - 1
                if direction == 'up' or direction == 'down':
                    frame = FROG_STRETCHED+frac_y*(FROG_REST-FROG_STRETCHED)
                    self.frame = round(frame)

    def _animateDeath(self,dt):
        """
        Attempt at animating sprite death (not implemented)

        Parameter dt: The time since the last animation frame.
        Precondition: dt is a float.
        """
        self._skull.x = self.x
        self._skull.y = self.y

        steps = self._skull.count / DEATH_SPEED
        animating = True
        while animating:
            # Get the current time
            dt = (yield)
            amount = steps*dt

            # Update the angle
            self._skull.frame = round(self._skull.frame + amount)

            # If we go to far, clamp and stop animating
            if self.skull.frame >= self._skull.count-1:
                self._skull.frame = self._skull.count - 1
                animating = False

# IF YOU NEED ADDITIONAL LANE CLASSES, THEY GO HERE
