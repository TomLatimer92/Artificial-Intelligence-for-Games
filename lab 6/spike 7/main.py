'''Autonomous Agent Movement: Seek, Arrive and Flee
Created for COS30002 AI for Games, Lab 05
By Clinton Woodward cwoodward@swin.edu.au
'''
from graphics import egi, KEY
from pyglet import window, clock
from pyglet.gl import *
from path import Path
from vector2d import Vector2D
from world import World
from agent import Agent, AGENT_MODES  
# Agent with seek, arrive, flee and pursuit.
def on_mouse_press(x, y, button, modifiers):
    if button == 1:  
	# left
        world.target = Vector2D(x, y)

def on_key_press(symbol, modifiers):
    if symbol == KEY.P:
        world.paused = not world.paused
    elif symbol in AGENT_MODES:
        for agent in world.agents:
            agent.mode = AGENT_MODES[symbol]
            
    ## LAB 05 TASK 2: Add agent by pressing a key
    # Add agent here. (duplicate)
    # seek and another mode can be used at the same time.
    if symbol == KEY.C:
        world.agents.append(Agent(world))
    ## lab 5 task 2 end ##
        
    ## LAB 06 TASK 1: Reset all paths to new random ones. ##
    # not sure if it is right or not.
    if symbol == KEY.P:
        for agent in world.agents:
            agent.randomise_path()
            # world.
    ## end R key implementation ##
        
    # Toggle debug force line info on the agent.
    elif symbol == KEY.I:
        for agent in world.agents:
            agent.show_info = not agent.show_info

    # change flocking wt values
    elif symbol == KEY.Q:
        world.wander_wt += 0.2
        print(world.wander_wt)
    elif symbol == KEY.A:
        world.wander_wt -= 0.2
        print(world.wander_wt)
    # change flocking wt values
    elif symbol == KEY.W:
        world.alignment_wt += 5.0
        print(world.alignment_wt)
    elif symbol == KEY.S:
        world.alignment_wt -= 5.0
        print(world.alignment_wt)
    # change flocking wt values
    elif symbol == KEY.E:
        world.seperation_wt += 5.0 
        print(world.seperation_wt)
    elif symbol == KEY.D:
        world.seperation_wt -= 5.0 
        print(world.seperation_wt)
    # change flocking wt values
    elif symbol == KEY.R:
        world.cohesion_wt += 5.0
        print(world.cohesion_wt)
    elif symbol == KEY.F:
        world.cohesion_wt -= 5.0
        print(world.cohesion_wt)

def on_resize(cx, cy):
    world.cx = cx
    world.cy = cy

if __name__ == '__main__':

    # create a pyglet window and set glOptions.
    win = window.Window(width=500, height=500, vsync=True, resizable=True)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    # needed so that egi knows where to draw.
    egi.InitWithPyglet(win)
    # prep the fps display.
    fps_display = clock.ClockDisplay()
    # register key and mouse event handlers.
    win.push_handlers(on_key_press)
    win.push_handlers(on_mouse_press)
    win.push_handlers(on_resize)
    # create a world for agents.
    world = World(500, 500)
    # add one agent.
    for i in range(10):
        world.agents.append(Agent(world))
##    for a in world.agents:
##        a.mode = "flocking"
    # unpause the world ready for movement.
    world.paused = False

    while not win.has_exit:
        win.dispatch_events()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        # show nice FPS bottom right (default).
        delta = clock.tick()
        world.update(delta)
        world.render()
        fps_display.draw()
        # swap the double buffer.
        win.flip()
