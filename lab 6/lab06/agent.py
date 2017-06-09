'''An agent with Seek, Flee, Arrive, Pursuit behaviours
Created for COS30002 AI for Games by Clinton Woodward cwoodward@swin.edu.au
'''
from vector2d import Vector2D
from vector2d import Point2D
from graphics import egi, KEY
from math import sin, cos, radians
from random import random, randrange, uniform
from path import Path

AGENT_MODES = {
    KEY._1: 'seek',
    KEY._2: 'arrive_slow',
    KEY._3: 'arrive_normal',
    KEY._4: 'arrive_fast',
    KEY._5: 'flee',
    KEY._6: 'pursuit',
    
    ### new Keys ###
    KEY._7: 'follow_path',
    KEY._8: 'wander'
    ### new keys end ###
}

class Agent(object):
    # NOTE: Class Object (not *instance*) variables!
    DECELERATION_SPEEDS = {
        'slow': 0.9, 'normal': 0.4, 'fast': 0.1
        ### ADD 'normal' and 'fast' speeds here:
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

        ### follow path mode edit 1. ###
        self.path = Path()
        self.randomise_path()
        # <-- Doesn’t exist yet but you’ll create it.
        self.waypoint_threshold = 0.0
        # <-- Work out a value for this as you test!
        ### end follow path mode edit 1. ###

    ### added wonder info part 2. ###
	# NEW WANDER INFO.
	### wander details.
        self.wander_target = Vector2D(1, 0)
        self.wander_dist = 1.0 * scale
        self.wander_radius = 1.0 * scale
        self.wander_jitter = 10.0 * scale
        self.bRadius = scale
        # Force and speed limiting code.
        # max speed is here.
        # limits?
        self.max_speed = 20.0 * scale
        self.max_force = 500.0
        ### end add wander infor part 2. ###	

        # debug draw info?
        self.show_info = False

    ### Create randomise path method. ###
    def randomise_path(self, num_pts=1, minx=1, miny=1, maxx=1, maxy=1):
                cx = self.world.cx
                # width.
                cy = self.world.cy  
                # height.
                margin = min(cx, cy) * (1/6) 
                # use this for padding in the next line ...
                self.path.create_random_path(num_pts, minx, miny, maxx, maxy)
                # you have to figure out the parameters.
    ### end creation of randomise path ###
	
    def calculate(self, delta):
        # calculate the current steering force.
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
            
        ### added follow path mode. ###
        elif mode == 'follow_path':
            force = self.follow_path(self.world.target)
        ### added follow path mode end. ###

        ### added wonder mode. ###
        elif mode == 'wander':
            force = self.wander(delta)
        ### end added wonder path mode. ###
            
        else:
            force = Vector2D()
        self.force = force
        return force

    # This is most likely wrong.
    def follow_path(self, path):
        self.path = Path()
        
        # If heading to final point (is_finished?).
        if Path.is_finished: 
        # Return a slow down force vector (Arrive).
            return self.arrive(self.world.target, 'slow')
        # Else
        # If within threshold distance of current way point, inc to next in path.
        if self.waypoint_threshold == path.current_pt:
            Path.inc_current()   
        # Return a force vector to head to current point at full speed (Seek).
            return self.seek(path.current_pt(self))           

    def update(self, delta):
        ''' update vehicle position and orientation. '''
        # calculate and set self.force to be applied.
        # force = self.calculate()
        # <-- delta needed for wander (delta).
        ## limit force? <-- for wander
        force = self.calculate(delta)
        force.truncate(self.max_force)
        # <-- new force limiting code.
        # determine the new accelteration.
        self.accel = force / self.mass
        # not needed if mass = 1.0.
        # new velocity.
        self.vel += self.accel * delta
        # check for limits of new velocity.
        self.vel.truncate(self.max_speed)
        # update position.
        self.pos += self.vel * delta
        # update heading is non-zero velocity (moving).
        if self.vel.length_sq() > 0.00000001:
            self.heading = self.vel.get_normalised()
            self.side = self.heading.perp()
        # treat world as continuous space - wrap new position if needed.
        self.world.wrap_around(self.pos)

        ### added wander to render function. ###
        # draw wander info?
        if self.mode == 'wander':
            # calculate the center of the wander circle in front of the agent.
            wnd_pos = Vector2D(self.wander_dist, 0)
            wld_pos = self.world.transform_point(wnd_pos, self.pos, self.heading, self.side)
            # draw the wander circle.
            egi.green_pen()
            egi.circle(wld_pos, self.wander_radius)
            # draw the wander target (little circle on the big circle).
            egi.red_pen()
            wnd_pos = (self.wander_target + Vector2D(self.wander_dist, 0))
            wld_pos = self.world.transform_point(wnd_pos, self.pos, self.heading, self.side)
            egi.circle(wld_pos, 3)
            pass
        ### end wander addtion part 1. ###

    def render(self, color= 'Red'):
        # graphics,
        ''' Draw the triangle agent with color'''
        # self.graphics = Graphics() 
        # draw the path if it exists and the mode is follow.
        if self.mode == 'follow_path':
            self.path.render()
            pass 
        # draw the ship.
        egi.set_pen_color(name=self.color)
        pts = self.world.transform_points(self.vehicle_shape, self.pos,
                                          self.heading, self.side, self.scale)
        # draw it!
        egi.closed_shape(pts)
        
        # add some handy debug drawing info lines - force and velocity.
        if self.show_info:
            s = 0.5 
	    # <-- scaling factor.
            # force.
            egi.red_pen()
            egi.line_with_arrow(self.pos, self.pos + self.force * s, 5)
            # velocity.
            egi.grey_pen()
            egi.line_with_arrow(self.pos, self.pos + self.vel * s, 5)
            # net (desired) change.
            egi.white_pen()
            egi.line_with_arrow(self.pos+self.vel * s, self.pos+ (self.force+self.vel) * s, 5)
            egi.line_with_arrow(self.pos, self.pos+ (self.force+self.vel) * s, 5)

    def speed(self):
        return self.vel.length()
		
    #--------------------------------------------------------------------------
	
    def seek(self, target_pos):
        ''' move towards target position. '''
        desired_vel = (target_pos - self.pos).normalise() * self.max_speed
        return (desired_vel - self.vel)

    def flee(self, hunter_pos):
        ''' move away from hunter position. '''
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

    ### create wonder function for agent class. ###	
    def wander(self, delta):
        '''random wandering using a projected jitter circle'''
        wt = self.wander_target
        # this behaviour is dependent on the update rate, so this line must
        # be included when using time independent framerate.
        jitter_tts = self.wander_jitter * delta 
		# this time slice
        # first, add a small random vector to the target's position.
        wt += Vector2D(uniform(-1,1) * jitter_tts, uniform(-1,1) * jitter_tts)
        # re-project this new vector back on to a unit circle.
        wt.normalise()
        # increase the length of the vector to the same as the radius
        # of the wander circle.
        wt *= self.wander_radius
        # move the target into a position WanderDist in front of the agent.
        target = wt + Vector2D(self.wander_dist, 0)
        # project the target into world space
        wld_target = self.world.transform_point(target, self.pos, self.heading, self.side)
        # and steer towards it
        return self.seek(wld_target)
        ## end wander function for agent class. ###
