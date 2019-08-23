# -*- coding: utf-8 -*-
"""
Created on Tue Aug 13 14:37:00 2019

@author: ajarmira
"""

import pygame as pg
def create_window(width, height):
    """create a width x height resizable window/frame"""
    win = pg.display.set_mode((width, height), pg.RESIZABLE)
    # optional fill bg red, default is black
    win.fill((255, 0, 0))
    # optional title info
    sf = "size x=%s  y=%s" % (width, height)
    pg.display.set_caption(sf)

    # any extra code here ...
    # draw a white circle
    white = (255, 255, 255)
    # center can be fixed or calculated for resize
    center = (150, 150)
    radius = 100
    pg.draw.circle(win, white, center, radius)

    pg.display.flip()
    return win
pg.init()
width = 300
height = 200
win = create_window(width, height)
# event loop and exit conditions (windows titlebar x click)
while True:
    for event in pg.event.get():
        if event.type == pg.VIDEORESIZE:
            width, height = event.size
            # redraw win in new size
            win = create_window(width, height)
            print(win.get_size())  # test
        if event.type == pg.QUIT:
            raise SystemExit