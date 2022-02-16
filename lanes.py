"""
Lanes module for Froggit

This module contains the lane classes for the Frogger game. The lanes are the vertical
slice that the frog goes through: grass, roads, water, and the exit hedge.

Each lane is like its own level. It has hazards (e.g. cars) that the frog has to make
it past.  Therefore, it is a lot easier to program frogger by breaking each level into
a bunch of lane objects (and this is exactly how the level files are organized).

You should think of each lane as a secondary subcontroller.  The level is a subcontroller
to app, but then that subcontroller is broken up into several other subcontrollers, one
for each lane.  That means that lanes need to have a traditional subcontroller set-up.
They need their own initializer, update, and draw methods.

There are potentially a lot of classes here -- one for each type of lane.  But this is
another place where using subclasses is going to help us A LOT.  Most of your code will
go into the Lane class.  All of the other classes will inherit from this class, and
you will only need to add a few additional methods.

If you are working on extra credit, you might want to add additional lanes (a beach lane?
a snow lane?). Any of those classes should go in this file.  However, if you need additional
obstacles for an existing lane, those go in models.py instead.  If you are going to write
extra classes and are now sure where they would go, ask on Piazza and we will answer.

# Julia Ludwig (jal545)
# 12/21/20
"""
from game2d import *
from consts import *
from models import *

# PRIMARY RULE: Lanes are not allowed to access anything in any level.py or app.py.
# They can only access models.py and const.py. If you need extra information from the
# level object (or the app), then it should be a parameter in your method.

class Lane(object):         # You are permitted to change the parent class if you wish
    """
    Parent class for an arbitrary lane.

    Lanes include grass, road, water, and the exit hedge.  We could write a class for
    each one of these four (and we will have classes for THREE of them).  But when you
    write the classes, you will discover a lot of repeated code.  That is the point of
    a subclass.  So this class will contain all of the code that lanes have in common,
    while the other classes will contain specialized code.

    Lanes should use the GTile class and to draw their background.  Each lane should be
    GRID_SIZE high and the length of the window wide.  You COULD make this class a
    subclass of GTile if you want.  This will make collisions easier.  However, it can
    make drawing really confusing because the Lane not only includes the tile but also
    all of the objects in the lane (cars, logs, etc.)
    """
    # LIST ALL HIDDEN ATTRIBUTES HERE
    #
    #Attribute _tile: the GTile object representing the lane
    #Invariant: must be a GTile object
    #
    #Attribute _objs: the list of objects in the lane
    #Invariant: must be a list of GImage objects
    #
    #Attribue _lane_speed: the speed of the objects in the lane
    #Invariant: must be an int or a float
    #
    #Attribute _buffer: the width of the offscreen buffer value
    #Invariant: must be a number >= 0
    #
    #Attribute _window_width: the width of the window in pixels
    #Invariant: must be a number >= 0- (int or float)


    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getTile(self):
        """
        returns the GTile object for the Lane
        """
        return self._tile

    def getLaneSpeed(self):
        """
        returns the Lane speed
        """
        return self._lane_speed

    # INITIALIZER TO SET LANE POSITION, BACKGROUND,AND OBJECTS
    def __init__(self,level_dict,lane_dict,bottom_coord,hitbox_dict):
        """
        Initializes the Lane object

        Parameter self: the Lane object to initialize
        Precondition: must be an instance of a Lane object

        Parameter level_dict: the dictionary representing the level
        Precondition: must be a dictionary

        Parameter lane_dict: the dictionary representing one lane
        Precondition: must be a dictionary

        Parameter bottom_coord: the bottom coordinate for the lane
        Precondition: must be a number (int or float) >= 0

        Parameter hitbox_dict: dictionary of all image hitboxes
        Precondition: must be a dict
        """
        lane_file = str(lane_dict['type']) + '.png'
        self._window_width = level_dict['size'][0]*GRID_SIZE

        self._tile = GTile(left = 0,
                     bottom = bottom_coord,
                     width = self._window_width,
                     height = GRID_SIZE,
                     source = lane_file)

        self._objs = []
        if 'objects' in lane_dict:
            for object in lane_dict['objects']:
                type = object['type']
                obj_file = str(type) + '.png'
                obj_hitbox = tuple(hitbox_dict['images'][type]['hitbox'])
                x_pos = (object['position']+0.5)*GRID_SIZE
                obj = GImage(y = self._tile.y,
                             x = x_pos,
                             source = obj_file,
                             hitbox = obj_hitbox)
                if 'speed' in lane_dict and lane_dict['speed']<0:
                    obj.angle = 180
                self._objs.append(obj)

        if 'speed' in lane_dict:
            self._lane_speed = lane_dict['speed']
        else:
            self._lane_speed = 0

        self._buffer = level_dict['offscreen']

    # ADDITIONAL METHODS (DRAWING, COLLISIONS, MOVEMENT, ETC)
    def update(self,dt):
        """
        Animates the obstacles in the Lane

        Paramter dt: the time since the last animation frame
        Precondition: number >= 0 (int or float)
        """
        change = self._lane_speed * dt
        for obj in self._objs:
            obj.x += change

        self._wrapAround(dt)

    def draw(self,view):
        """
        Draws the lanes

        Parameter view: the window to draw the lanes
        Precondition: must be a GView object
        """
        self._tile.draw(view)
        if self._objs != []:
            for obj in self._objs:
                obj.draw(view)

    def _wrapAround(self, dt):
        """
        Wraps the lane objects around the screen with an offscreen buffer

        Paramter dt: the time since the last animation frame
        Precondition: number >= 0 (int or float)
        """
        right_edge = -self._buffer * GRID_SIZE
        left_edge = self._window_width + self._buffer * GRID_SIZE

        for obj in self._objs:
            if self._lane_speed < 0:
                d = obj.x - right_edge  #negative d
                if obj.x <= right_edge:
                    obj.x = left_edge + d
            elif self._lane_speed >0:
                d = obj.x - left_edge #positive d
                if obj.x >= left_edge:
                    obj.x = right_edge + d


class Grass(Lane):                           # We recommend AGAINST changing this one
    """
    A class representing a 'safe' grass area.

    You will NOT need to actually do anything in this class.  You will only do anything
    with this class if you are adding additional features like a snake in the grass
    (which the original Frogger does on higher difficulties).
    """
    pass

    # ONLY ADD CODE IF YOU ARE WORKING ON EXTRA CREDIT EXTENSIONS.


class Road(Lane):                           # We recommend AGAINST changing this one
    """
    A class representing a roadway with cars.

    If you implement Lane correctly, you do really need many methods here (not even an
    initializer) as this class will inherit everything.  However, roads are different
    than other lanes as they have cars that can kill the frog. Therefore, this class
    does need a method to tell whether or not the frog is safe.
    """
    #Attribute _carCollided: whether the Frog object has collided with a car
    #Invariant: must be a bool

    # DEFINE ANY NEW METHODS HERE
    def getCarCollided(self, frog):
        """
        returns True if frog collided with a car, else False

        Parameter frog: the Frog to check
        Precondition: must be an instance of Frog
        """
        print('getCarCollided() in lanes')
        if frog.isFrogVisible():
            self._carCollide(frog)
        return self._carCollided

    def __init__(self,level_dict,lane_dict,bottom_coord,hitbox_dict):
        """
        Initializes the Hedge object

        Parameter self: the Lane object to initialize
        Precondition: must be an instance of a Lane object

        Parameter level_dict: the dictionary representing the level
        Precondition: must be a dictionary

        Parameter lane_dict: the dictionary representing one lane
        Precondition: must be a dictionary

        Parameter bottom_coord: the bottom coordinate for the lane
        Precondition: must be a number (int or float) >= 0
        """
        super().__init__(level_dict,lane_dict,bottom_coord,hitbox_dict)
        self._carCollided = False

    def _carCollide(self, frog):
        """
        sets attribute _carCollided to True if frog collided with a car,
        else False

        Paramter self: the Road object
        Precondition: must be an instance of Road

        Parameter frog: the Frog object to check for
        Precondition: must be an instance of Frog
        """
        print('_carCollide() in lanes')
        assert isinstance(frog,Frog), repr(frog)+' is not a Frog'

        if frog.isFrogVisible():
            collided = False
            for car in self._objs:
                if car.collides(frog):
                    collided = True
                    break
            self._carCollided = collided


class Water(Lane):
    """
    A class representing a waterway with logs.

    If you implement Lane correctly, you do really need many methods here (not even an
    initializer) as this class will inherit everything.  However, water is very different
    because it is quite hazardous. The frog will die in water unless the (x,y) position
    of the frog (its center) is contained inside of a log. Therefore, this class needs a
    method to tell whether or not the frog is safe.

    In addition, the logs move the frog. If the frog is currently in this lane, then the
    frog moves at the same rate as all of the logs.
    """

    # DEFINE ANY NEW METHODS HERE
    def frogOnLog(self,frog):
        """
        returns True if a frog is on a log, else False

        Parameter frog: the Frog to check
        Precondition: must be an instance of Frog
        """
        onLog = False
        for log in self._objs:
            point = (frog.x,frog.y)
            if log.contains(point):
                onLog = True
        return onLog

    def frogDrowned(self,frog):
        """
        returns True if the frog is on Water but not on a log

        Parameter frog: the Frog to check
        Precondition: must be an instance of Frog
        """
        return self._tile.collides(frog) and not self.frogOnLog(frog)


class Hedge(Lane):
    """
    A class representing the exit hedge.

    This class is a subclass of lane because it does want to use a lot of the features
    of that class. But there is a lot more going on with this class, and so it needs
    several more methods.  First of all, hedges are the win condition. They contain exit
    objects (which the frog is trying to reach). When a frog reaches the exit, it needs
    to be replaced by the blue frog image and that exit is now "taken", never to be used
    again.

    That means this class needs methods to determine whether or not an exit is taken.
    It also need to take the (x,y) position of the frog and use that to determine which
    exit (if any) the frog has reached. Finally, it needs a method to determine if there
    are any available exits at all; once they are taken the game is over.

    These exit methods will require several additional attributes. That means this class
    (unlike Road and Water) will need an initializer. Remember to user super() to combine
    it with the initializer for the Lane.
    """
    # LIST ALL HIDDEN ATTRIBUTES HERE
    #
    #Attribute _frogAtObstacle: whether a frog is at a hedge obstacle
    #Invariant: must be a bool
    #
    #Attribute _reachedExit: whether a frog has reached an exit
    #Invariant: must be a bool
    #
    #Attribute _openexits: a list of the open exits
    #Inavariant: must be a list
    #
    #Attribute _closedexits: a list of the blocked exits
    #Inavariant: must be a list
    #
    #Attribute _safefrogs: the list of FROG_SAFE images
    #Inavariant: must be a list of GImages
    #
    #Attribute _fullExits: whether the exits in a Hedge are full
    #Invariant: must be a bool

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getFrogAtObstacle(self,frog):
        """
        returns True if frog is at an obstacle, else False

        Parameter frog: the Frog object to check for
        Precondition: must be an instance of Frog
        """
        self._frogInObstacles(frog)
        return self._frogAtObstacle

    def getReachedExit(self,frog,key):
        """
        returns True if frog has reached an exit, else False

        Parameter frog: the Frog object to check for
        Precondition: must be an instance of Frog

        Parameter key: they key that has been pressed
        Precondition: must be one of 'left','right','up', or 'down'
        """
        assert isinstance(frog, Frog), repr(frog)+' is not an instance of Frog'

        self._checkReachedExit(frog,key)
        return self._reachedExit

    def getOpenExits(self):
        """
        returns the list of open exits
        """
        return self._openexits

    def getClosedExits(self):
        """
        returns the list of closed exits
        """
        return self._closedexits

    def isHedgeFull(self):
        """
        returns True if all exits in a Hedge are full
        """
        self._exitsFull()
        return self._fullExits

    # INITIALIZER TO SET ADDITIONAL EXIT INFORMATION
    def __init__(self,level_dict,lane_dict,bottom_coord,hitbox_dict):
        """
        Initializes the Hedge object

        Parameter self: the Lane object to initialize
        Precondition: must be an instance of a Lane object

        Parameter level_dict: the dictionary representing the level
        Precondition: must be a dictionary

        Parameter lane_dict: the dictionary representing one lane
        Precondition: must be a dictionary

        Parameter bottom_coord: the bottom coordinate for the lane
        Precondition: must be a number (int or float) >= 0
        """
        super().__init__(level_dict,lane_dict,bottom_coord,hitbox_dict)
        self._frogAtObstacle = False
        self._safefrogs = []

        self._openexits = []
        self._closedexits = []
        self._fullExits = False

        for obj in self._objs:
            dot = obj.source.find('.')
            if obj.source[:dot]=='exit':
                self._openexits.append(obj)

    # ANY ADDITIONAL METHODS
    def draw(self,view):
        """
        Draws the road
        """
        super().draw(view)
        for safefrog in self._safefrogs:
            safefrog.draw(view)

    def goingToObstacle(self,key,frog):
        """
        returns True if frog's movement due to the key press will result in the
        frog colliding with an obstacle, else False

        An obstacle is an object not including open exits or paths

        Parameter key: they key that has been pressed
        Precondition: must be one of 'left','right','up', or 'down'

        Parameter frog: the Frog object to check for
        Precondition: must be an instance of Frog
        """
        if key == 'up':
            point = (frog.x,frog.y+GRID_SIZE)
        elif key == 'down':
            point = (frog.x,frog.y-GRID_SIZE)
        elif key == 'left':
            point = (frog.x-GRID_SIZE,frog.y)
        elif key == 'right':
            point = (frog.x+GRID_SIZE,frog.y)

        toObstacle = False
        for obstacle in self._objs:
            if obstacle.contains(point) and obstacle not in self._openexits:
                toObstacle = True
                break
        return toObstacle

    def willReachExit(self,frog,key):
        """
        determines is a frog is at an OPEN exit

        Parameter frog: the Frog object to check for
        Precondition: must be an instance of Frog

        Parameter key: they key that has been pressed
        Precondition: must be one of 'left','right','up', or 'down'
        """
        assert isinstance(frog,Frog), repr(frog)+' is not a Frog'

        if key == 'up':
            point = (frog.x,frog.y+GRID_SIZE)
        elif key == 'down':
            point = (frog.x,frog.y-GRID_SIZE)
        elif key == 'left':
            point = (frog.x-GRID_SIZE,frog.y)
        elif key == 'right':
            point = (frog.x+GRID_SIZE,frog.y)

        inExit = False
        for obj in self._objs:
            if obj.contains(point) and obj in self._openexits and key != 'down':
                inExit = True
                break
        return inExit

    def _frogInObstacles(self, frog):
        """
        sets attribute _frogAtObstacle to True if an obstacle contains the frog

        Paramter self: the Hedge object
        Precondition: must be an instance of Hedge

        Parameter frog: the Frog object to check for
        Precondition: must be an instance of Frog
        """
        point = (frog.x,frog.y)
        inObstacle = False
        for obstacle in self._objs:
            if obstacle.contains(point):
                inObstacle = True
                break
        self._frogAtObstacle = inObstacle

    def _checkReachedExit(self,frog,key):
        """
        determines is a frog is at an exit and stores the bool

        Parameter frog: the Frog object to check for
        Precondition: must be an instance of Frog

        Parameter key: the last key pressed
        Precondition: any key as a string
        """
        assert isinstance(frog,Frog), repr(frog)+' is not a Frog'

        point = (frog.x,frog.y)

        inExit = False
        for obj in self._objs:
            if obj.contains(point) and obj in self._openexits and not key == 'down':
                inExit = True
                safe_frog = GImage(source = FROG_SAFE,
                                   x = obj.x,
                                   y = obj.y)
                self._safefrogs.append(safe_frog)
                self._closedexits.append(obj)
                self._openexits.remove(obj)
                break
            elif obj.contains(point) and obj in self._openexits and key == 'down':
                frog.y += GRID_SIZE
        self._reachedExit = inExit

    def _exitsFull(self):
        """
        determines if all exits in a hedge are full and stores in _fullExits
        """
        self._fullExits = self._openexits == []

# IF YOU NEED ADDITIONAL LANE CLASSES, THEY GO HERE
