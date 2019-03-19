#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
KiCad EEschema common definitions
Arjen Klaverstijn 2018
"""
from __future__ import print_function
import time

GUID_SEED = int(time.time())

def createId():
    global GUID_SEED
    guid = format(int(GUID_SEED),'x')
    GUID_SEED += 1
    return guid

def component(type, value, ref, guid, xPos, yPos, footprint = str(), matrix = [1,0,0,-1]):

    comp = '$Comp\n'
    comp += 'L {} {}?\n'.format(type, ref)
    comp += 'U 1 1 {}\n'.format(guid)
    comp += 'P {:.0f} {:.0f}\n'.format(xPos, yPos)
    comp += 'F 0 "{}?" H {:.0f} {:.0f} 50  0000 L CNN\n'.format(ref, xPos+10, yPos+200)
    comp += 'F 1 "{}" H {:.0f} {:.0f} 50  0000 C CNN\n'.format(value, xPos, yPos-100)
    comp += 'F 2 "{}" H {:.0f} {:.0f} 50  1000 C CNN\n'.format(footprint, xPos, yPos+200)
    comp += 'F 3 "" H {:.0f} {:.0f} 50  1000 C CNN\n'.format(xPos, yPos+200)
    comp += '\t1    {:.0f} {:.0f}\n'.format(xPos, yPos)
    comp += '\t{}    {}    {}    {}\n'.format(*matrix)
    comp += '$EndComp\n'
    return comp

def label(name, xPos, yPos, orient, type = 'Input'):
    labelText =  'Text GLabel {:.0f} {:.0f} {}    60   {} ~ 0\n{}\n'.format(xPos, yPos, orient, type, name)
    return labelText

def wire(xStart, yStart, xEnd, yEnd):
    return 'Wire Wire Line\n {:.0f} {:.0f} {:.0f} {:.0f}\n'.format(xStart, yStart, xEnd, yEnd)

def textBlock(text, posX, posY, vertical = 0, dimension = 180):
    return 'Text Notes {:.0f} {:.0f} {:.0f} {:.0f}  ~ 24\n{}\n'.format(posX, posY, vertical, dimension, text)

def connection(posX, posY):
    return 'Connection ~ {:.0f} {:.0f}\n'.format(posX, posY)
