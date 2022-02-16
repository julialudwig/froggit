"""
Subcontroller module for Froggit

This module contains the subcontroller to manage a single level in the Froggit game.
Instances of Level represent a single game, read from a JSON  Whenever you load a new
level, you are expected to make a new instance of this class.

The subcontroller Level manages the frog and all of the obstacles However, those are
all defined in models.py  The only thing in this class is the level class and all of
the individual lanes.

This module should not contain any more classes than Levels If you need a new class,
it should either go in the lanes.py module or the models.py module.

# Julia Ludwig (jal545)
# 12/21/20
"""
from game2d import *
from consts import *
from lanes  import *
from models import *

# PRIMARY RULE: Level can only access attributes in models.py or lanes.py using getters
# and setters Level is NOT allowed to access anything in app.py (Subcontrollers are not
# permitted to access anything in their parent To see why, take CS 3152)


class Level(object):
    """
    This class controls a single level of Froggit.

    This subcontroller has a reference to the frog and the individual lanes  However,
    it does not directly store any information about the contents of a lane (e.g the
    cars, logs, or other items in each lane) That information is stored inside of the
    individual lane objects.

    If you want to pause the game, tell this controller to draw, but do not update  See
    subcontrollers.py from Lesson 27 for an example  This class will be similar to that
    one in many ways.

    All attributes of this class are to be hidden  No attribute should be accessed
    without going through a getter/setter first  However, just because you have an
    attribute does not mean that you have to have a getter for it  For example, the
    Froggit app probably never needs to access the attribute for the Frog object, so
    there is no need for a getter.

    The one thing you DO need a getter for is the width and height  The width and height
    of a level is different than the default width and height and the window needs to
    resize to match  That resizing is done in the Froggit app, and so it needs to access
    these values in the level  The height value should include one extra grid square
    to suppose the number of lives meter.
    """
    pass
    # LIST ALL HIDDEN ATTRIBUTES HERE
    #
    #Attribute _level_dict: the dictionary describing the level
    #Invariant: must be a dictionary
    #
    #Attribute _lanes: the list of lanes
    #Invariant: must be a list of Lane objects
    #
    #Attribute _frog: the Frog object
    #Invariant: must be a Frog object
    #
    #Attrrbute _lives: a list of images representing lives
    #Invariant: must be a list of GImage objects
    #
    #Attribute _lives_label: a label indicating the lives
    #Invariant: must be a GLabel object
    #
    #Attribute _frogKilled: whether the _frog has been killed
    #Inavariant: must be a bool
    #
    #Attribute _initial_x: the initial x-position of the Frog in pixels
    #Invariant: must be a number >= 0 (int or float)
    #
    #Attribute _initial_y: the initial y-position of the Frog in pixels
    #Invariant: must be a number >= 0 (int or float)
    #
    #Attribute _gameOver: whether the game is over
    #Invariant: must be a bool
    #
    #Attribute _inExit: whether the frog has reached an exit
    #Inavariant: must be a bool
    #
    #Attribute _gameWon: whether the game has been won yet
    #Invariant: must be a bool
    #
    # Attribute _animator: A coroutine for performing an animation
    # Invariant: _animator is a generator-based coroutine (or None)

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getLevelWidth(self):
        """
        returns the level width in terms of grid squares
        """
        return self._level_dict['size'][0]

    def getLevelHeight(self):
        """
        returns the level height in terms of grid squares
        """
        return self._level_dict['size'][1]

    def isFrogKilled(self):
        """
        returns True if the Frog has been killed, else False
        """
        print('isFrogKilled() in level')
        self._checkFrogKilled()
        print('self._frogKilled: '+str(self._frogKilled))
        return self._frogKilled

    def setInitialFrog(self):
        """
        initializes frog state at the beginning of each round
        """
        self._frog.y = (self._initial_y+0.5)*GRID_SIZE
        self._frog.x = (self._initial_x+0.5)*GRID_SIZE
        self._frog.setFrogVisibility(True)
        self._frogKilled = False
        self._animator = None
        self._frog.setFrame(FROG_REST)

    def isGameOver(self):
        """
        returns True if there are no more lives left, else False
        """
        print('isGameOver() in level')
        return self._gameOver

    def isInExit(self,key):
        """
        returns True if the frog is at an exit, else False

        Parameter key: they key that has been pressed
        Precondition: must be one of 'left','right','up', or 'down'
        """
        self._frogInOpenExit(key)
        return self._inExit

    def isGameWon(self):
        """
        returns True if the game has been won and all exits are full
        """
        self._checkWin()
        return self._gameWon

    # INITIALIZER (standard form) TO CREATE THE FROG AND LANES
    def __init__(self,level_info,hitboxes):
        """
        Parameter self: the Level object to initialize
        Precondition: must be an instance of Level

        Parameter level_info: the dictionary containing the level information
        Precondition: is a dictionary containing the key 'lanes'

        Parameter hitboxes: the dictionary that lists image hitboxes
        Precondition: must be a dictionary
        """
        self._level_dict = level_info
        self._lanes = []
        bottom_coord = 0

        for lane in level_info['lanes']:
            if lane['type']=='grass':
                lane_obj = Grass(level_info,lane,bottom_coord,hitboxes)
            elif lane['type']=='road':
                lane_obj = Road(level_info,lane,bottom_coord,hitboxes)
            elif lane['type']=='water':
                lane_obj = Water(level_info,lane,bottom_coord,hitboxes)
            elif lane['type']=='hedge':
                lane_obj = Hedge(level_info,lane,bottom_coord,hitboxes)

            self._lanes.append(lane_obj)
            bottom_coord += GRID_SIZE

        self._initial_x = self.getLevelWidth()//2
        self._initial_y = 0

        self._frog = Frog(self._initial_x, self._initial_y,hitboxes)
        self._frog.setFrogVisibility(True)
        self._frogKilled = False
        self._inExit = False
        self._gameWon = False

        self._displayLives()
        self._gameOver = False
        self._frogKilled = False
        self._animator = None

    # UPDATE METHOD TO MOVE THE FROG AND UPDATE ALL OF THE LANES
    def update(self,dt,key):
        """
        Updates the level each frame

        Parameter dt: The time (in seconds) since last update
        Precondition: dt is an int or a float)

        Parameter key: they key that has been pressed
        Precondition: must be one of 'left','right','up', or 'down'
        """
        if not self._animator is None:
            try:
                self._animator.send(dt)
            except StopIteration:
                self._animator = None
        elif key == 'left':
            self._leftKey(dt)
        elif key == 'right':
            self._rightKey(dt)
        elif key == 'up':
            self._upKey(dt)
        elif key == 'down':
            self._downKey(dt)
        else:
            if self._checkDeath():
                self._frogDies()

        for lane in self._lanes:
            lane.update(dt)

        self._moveFrogOnLog(dt)

    # DRAW METHOD TO DRAW THE FROG AND THE INDIVIDUAL LANES
    def draw(self,view):
        """
        Draws all of the lanes in the window

        Parameter self: the Lane object to draw
        Precondition: must be a Lane object

        Parameter view: the window to draw the lanes
        Precondition: must be a GView object
        """
        for lane in self._lanes:
            lane.draw(view)

        if not self._frog is None and self._frog.isFrogVisible():
            self._frog.draw(view)

        self._lives_label.draw(view)

        for life in self._lives:
            life.draw(view)

    # ANY NECESSARY HELPERS (SHOULD BE HIDDEN)
    def _displayLives(self):
        """
        Helper for the initializer to initialize the label and the frog lives
        """
        self._lives_label = GLabel(font_name = ALLOY_FONT,
                                   font_size = ALLOY_SMALL,
                                   right = (self.getLevelWidth()-3)*GRID_SIZE,
                                   y = (self.getLevelHeight()+0.5)*GRID_SIZE,
                                   text = 'Lives:',
                                   linecolor = 'dark green')
        life3 = GImage(source = FROG_HEAD,
                       width = GRID_SIZE,
                       height = GRID_SIZE,
                       right = self.getLevelWidth()*GRID_SIZE,
                       top = (self.getLevelHeight()+1)*GRID_SIZE)
        life2 = GImage(source = FROG_HEAD,
                       width = GRID_SIZE,
                       height = GRID_SIZE,
                       right = (self.getLevelWidth()-1)*GRID_SIZE,
                       top = (self.getLevelHeight()+1)*GRID_SIZE)
        life1 = GImage(source = FROG_HEAD,
                       width = GRID_SIZE,
                       height = GRID_SIZE,
                       right = (self.getLevelWidth()-2)*GRID_SIZE,
                       top = (self.getLevelHeight()+1)*GRID_SIZE)
        self._lives = [life1,life2,life3]

    def _frogInHedge(self):
        """
        returns True if _frog has collided with the hedge, else False
        """
        collided = False
        for lane in self._lanes:
            if isinstance(lane,Hedge) and self._frog.collides(lane.getTile()):
                collided = True
                if lane.getFrogAtObstacle(self._frog) and \
                not self._frogInClosedExit():
                    collided = False
                break
        return collided

    def _checkFrogKilled(self):
        """
        Actions to do when the _frog has been killed

        Sets the _frog attribute to None and the _frogKilled attribute to True
        """
        print('_checkFrogKilled() in level')
        if not self._frog is None:
            if self._frog.isFrogVisible():
                for lane in self._lanes:
                    if isinstance(lane,Road) and lane.getCarCollided(self._frog):
                        self._frogDies()
                        break

    def _frogInOpenExit(self,key):
        """
        checks if Frog has reached open exit

        Parameter key: they key that has been pressed
        Precondition: must be one of 'left','right','up', or 'down'
        """
        exited = False
        if not self._frog is None:
            for lane in self._lanes:
                if isinstance(lane,Hedge):
                    reached = lane.getReachedExit(self._frog,key)
                    if reached:
                        exited = True
                        self._frog.setFrogVisibility(False)
                        break
        self._inExit = exited

    def _frogInClosedExit(self):
        """
        checks if Frog has reached closed exit
        """
        inClosedExit = False
        for lane in self._lanes:
            if isinstance(lane, Hedge):
                for exit in lane.getClosedExits():
                    if exit.contains((self._frog.x,self._frog.y)):
                        inClosedExit = True
        return inClosedExit

    def _checkWin(self):
        """
        determines if all exits are full and the game has been won
        """
        hedges = 0
        full_hedges = 0
        for lane in self._lanes:
            if isinstance(lane,Hedge):
                hedges += 1
                if lane.isHedgeFull():
                    full_hedges += 1
        self._gameWon = hedges == full_hedges

    def _moveFrogOnLog(self, dt):
        """
        Moves frog when it is on a log
        """
        for lane in self._lanes:
            if isinstance(lane, Water) and lane.frogOnLog(self._frog):
                self._frog.x += lane.getLaneSpeed() * dt

    def _frogDies(self):
        """
        removes a life from the frog
        """
        print('_frogDies() in level')
        self._frog.setFrogVisibility(False)
        self._frogKilled = True
        del self._lives[-1]
        if self._lives ==[]:
            self._gameOver = True

    def _checkDeath(self):
        """
        determines is frog has died
        """
        for lane in self._lanes:
            if isinstance(lane,Water) and lane.frogDrowned(self._frog):
                return True
        if self._frog.x > self.getLevelWidth() * GRID_SIZE \
        or self._frog.x < 0:
            return True
        return False

    def _goingToHedge(self,key):
        """
        returns True if the next movement will cause _frog to be in Hedge

        Parameter key: they key that has been pressed
        Precondition: must be one of 'left','right','up', or 'down'
        """
        if key == 'up':
            point = (self._frog.x,self._frog.y+GRID_SIZE)
        elif key == 'down':
            point = (self._frog.x,self._frog.y-GRID_SIZE)
        elif key == 'left':
            point = (self._frog.x-GRID_SIZE,self._frog.y)
        elif key == 'right':
            point = (self._frog.x+GRID_SIZE,self._frog.y)

        collided = False
        for lane in self._lanes:
            if isinstance(lane,Hedge) and lane.getTile().contains(point):
                collided = True
                if lane.goingToObstacle(key,self._frog) or \
                lane.willReachExit(self._frog,key):
                    collided = False
                break
        return collided

    def _leftKey(self,dt):
        """
        Helper to animate frog movement to left

        Parameter dt: The time (in seconds) since last update
        Precondition: dt is an int or a float)
        """
        self._frog.angle = FROG_WEST
        if not self._goingToHedge('left'):
            final_x = self._frog.x - GRID_SIZE
            if final_x > 0:
                self._animator = self._frog.animateSlide(dt,'left')
                next(self._animator)
            if self._checkDeath():
                self._frogDies()

    def _rightKey(self,dt):
        """
        Helper to animate frog movement to right

        Parameter dt: The time (in seconds) since last update
        Precondition: dt is an int or a float)
        """
        self._frog.angle = FROG_EAST
        if not self._goingToHedge('right'):
            final_x = self._frog.x + GRID_SIZE
            if final_x < self.getLevelWidth()*GRID_SIZE:
                self._animator = self._frog.animateSlide(dt,'right')
                next(self._animator)
            if self._checkDeath():
                self._frogDies()

    def _upKey(self,dt):
        """
        Helper to animate frog movement up

        Parameter dt: The time (in seconds) since last update
        Precondition: dt is an int or a float)
        """
        self._frog.angle = FROG_NORTH
        if not self._goingToHedge('up'):
            final_y = self._frog.y + GRID_SIZE
            if final_y < self.getLevelHeight()*GRID_SIZE:
                self._animator = self._frog.animateSlide(dt,'up')
                next(self._animator)
            if self._checkDeath():
                self._frogDies()

    def _downKey(self,dt):
        """
        Helper to animate frog movement down

        Parameter dt: The time (in seconds) since last update
        Precondition: dt is an int or a float)
        """
        self._frog.angle = FROG_SOUTH
        if not self._goingToHedge('down'):
            final_y = self._frog.y - GRID_SIZE
            if final_y > 0 and not self.isInExit(key) and not self._frogInHedge():
                self._animator = self._frog.animateSlide(dt,'down')
                next(self._animator)
            if self._checkDeath():
                self._frogDies()
