#!/usr/bin/env python
# coding: utf8

"""
DrawRoom - Distraction free drawing.

This program is free software. It comes without any warranty, to
the extent permitted by applicable law. You can redistribute it
and/or modify it under the terms of the Do What The Fuck You Want
To Public License, Version 2, as published by Sam Hocevar. See
http://sam.zoy.org/wtfpl/COPYING for more details.
"""

try:
    from sys import exit, argv
    import random
    import pygame
    from pygame.locals import *

except ImportError, err:
    print "Error, couldn't load module. %s" % (err)
    exit(2)

class Screen:
    def __init__(self, resolution=(0, 0), cmdline=""):
        self.color = (255,255,255)
        self.resolution = resolution
        if "--nofullscreen" in cmdline:
            self.window = pygame.display.set_mode(self.resolution, pygame.RESIZABLE)
        else:
            self.window = pygame.display.set_mode(self.resolution, pygame.FULLSCREEN)

        pygame.display.set_caption('DrawRoom')

        # pygame.mouse.set_visible(0) # Hide mouse
        self.screen = pygame.display.get_surface() # Create surface on window
        self.screen_rect = self.screen.get_rect() # Rectangle of window

    def size(self):
        return self.screen_rect

    def fill(self):
        self.screen.fill(self.color)

    def quit():
        exit(0)

class Brush:
  def __init__(self):
    self.size = 10
    self.down = False
    self.color = random_color()

  def erase(self):
    if self.color == (255,255,255):
      self.color = random_color()
    else:
      self.color = (255,255,255)

  def bigger(self, step = 10):
    self.size += step

  def smaller(self, step = 10):
    if self.size >= step:
      self.size -= step

def random_color():
  r = random.randint(0, 255)
  g = random.randint(0, 255)
  b = random.randint(0, 255)
  return (r, g, b)

def key_pressed(event, key):
  return event.type == KEYDOWN and event.key == key

def game(events, screen, brush):

    for event in events:
        if event.type == QUIT:
          exit()
          return
        elif key_pressed(event, K_ESCAPE):
          exit()
          return
        elif key_pressed(event, K_f):
          pygame.display.set_mode(screen.resolution, pygame.RESIZABLE)
          return
        elif key_pressed(event, K_e):
          brush.erase()
          return
        elif key_pressed(event, K_r):
          brush.color = random_color()
          return
        elif key_pressed(event, K_UP):
          brush.bigger()
          return
        elif key_pressed(event, K_DOWN):
          brush.smaller()
          return
        elif event.type == pygame.MOUSEBUTTONDOWN:
          brush.down = True
          return
        elif event.type == pygame.MOUSEBUTTONUP:
          brush.down = False
          return
        elif event.type == pygame.MOUSEMOTION:
          if brush.down:
            s = pygame.display.get_surface()
            pygame.draw.circle(s, brush.color, event.pos, brush.size)

    pygame.display.update() # Update screen

def main():
    pygame.init() # Initialize pygame library

    pygame.key.set_repeat(1, 1) # Control how held keys are repeated
    clock = pygame.time.Clock() # Clock for game loop

    screen = Screen(cmdline=argv) # Create screen instance

    screen.fill()
    brush = Brush()

    while True:
        clock.tick(30) # Set to a decent framerate
        game(pygame.event.get(), screen, brush)

main()
