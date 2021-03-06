'''An agent with Seek, Flee, Arrive, Pursuit behaviours
Created for COS30002 AI for Games by Clinton Woodward cwoodward@swin.edu.au
'''

from vector2d import Vector2D
from vector2d import Point2D
from graphics import egi, KEY
from math import sin, cos, radians
from random import random, randrange, uniform

AGENT_MODES = {
    KEY._1: 'seek',
    KEY._2: 'arrive_slow',
    KEY._3: 'arrive_normal',
    KEY._4: 'arrive_fast',
    KEY._5: 'flee',
    KEY._6: 'pursuit',
}

class Agent(object):
    # NOTE: Class Object (not *instance*) variables!
    DECELERATION_SPEEDS = {
        'slow': 0.9, 'normal': 0.4, 'fast': 0.1
        ### ADD 'normal' and 'fast' speeds here: ###
    }
    
    # mass is here.
    def __init__(self, world=None, scale=30.0, mass=2.0, mode='seek'):
        # keep a reference to the world object.
        self.world = world
        self.mode = mode    
        # where am i and where am i going? random start pos.
        dir = radians(random()*360)
        self.pos = Vector2D(randrange(world.cx), randrange(world.cy))
        self.vel = Vector2D()
        self.heading = Vector2D(sin(dir), cos(dir))
        self.side = self.heading.perp()
        self.scale = Vector2D(scale, scale)
        # easy scaling of agent size.
        self.force = Vector2D()
        # current steering force.
        self.accel = Vector2D()
        # current acceleration due to force.
        self.mass = mass
        # data for drawing this agent.
        self.color = 'ORANGE'
        self.vehicle_shape = [
            Point2D(-1.0,  0.6),
            Point2D( 1.0,  0.0),
            Point2D(-1.0, -0.6)
        ]
        
    def calculate(self, delta):
        # reset the steering force
        mode = self.mode
        if mode == 'seek':
            force = self.seek(self.world.target)
        elif mode == 'arrive_slow':
            force = self.arrive(self.world.target, 'slow')
        elif mode == 'arrive_normal':
            force = self.arrive(self.world.target, 'normal')
        elif mode == 'arrive_fast':
            force = self.arrive(self.world.target, 'fast')
        elif mode == 'flee':
            force = self.flee(self.world.target)    
        elif mode == 'pursuit':
            force = self.pursuit(self.world.hunter)      
        else:
            force = Vector2D()
        self.force = force
        return force
            

    def update(self, delta):
        ''' update vehicle position and orientation. '''
        acceleration = self.calculate()
        # new velocity.
        self.vel += self.accel * delta
        # check for limits of new velocity.
        self.vel.truncate(self.max_speed)
        # update position
        self.pos += self.vel * delta
        # update heading is non-zero velocity (moving).
        if self.vel.length_sq() > 0.00000001:
            self.heading = self.vel.get_normalised()
            self.side = self.heading.perp()
        # treat world as continuous space - wrap new position if needed.
        self.world.wrap_around(self.pos)

    def render(self, color=None):
       ''' Draw the triangle agent with color. '''
       egi.set_pen_color(name=self.color)
       pts = self.world.transform_points(self.vehicle_shape, self.pos,
                                          self.heading, self.side, self.scale)
       # draw it!
       egi.closed_shape(pts)

    def speed(self):
        return self.vel.length()
    #--------------------------------------------------------------------------

    def seek(self, target_pos):
        ''' move towards target position '''
        desired_vel = (target_pos - self.pos).normalise() * self.max_speed
        return (desired_vel - self.vel)

    def flee(self, hunter_pos):
        ''' move away from hunter position '''
        ## add panic distance (second).
        panic_dist = 1000.0
        hunter = hunter_pos - self.pos
        distance = hunter.length()
        if distance < panic_dist:
            ## add flee calculations (first).
            return(self.pos - hunter_pos).normalise() * self.max_speed
            return Vector2D

    def arrive(self, target_pos, speed):
        ''' this behaviour is similar to seek() but it attempts to arrive at
            the target position with a zero velocity. '''
        decel_rate = self.DECELERATION_SPEEDS[speed]
        to_target = target_pos - self.pos
        dist = to_target.length()
        if dist > 0:
            # calculate the speed required to reach the target given the,
            # desired deceleration rate.
            speed = dist / decel_rate
            # make sure the velocity does not exceed the max.
            speed = min(speed, self.max_speed)
            # from here proceed just like Seek except we don't need to,
            # normalize the to_target vector because we have already gone to,
            # trouble of calculating its length for dist.
            desired_vel = to_target * (speed / dist)
            return (desired_vel - self.vel)
        return Vector2D(0, 0)

    def pursuit(self, evader):
        ''' this behaviour predicts where an agent will be in time T and seeks
            towards that point to intercept it. '''
        ## OPTIONAL EXTRA... pursuit (you'll need something to pursue!).
        # desired_vel = (evader - self.pos).normalise() * self.max_speed
        return Vector2D(0, 0)
