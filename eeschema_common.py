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

def component(type, value, ref, guid, xPos, yPos, mirrorH = False):

    comp = '$Comp\n'
    comp += 'L {} {}?\n'.format(type, ref)
    comp += 'U 1 1 {}\n'.format(guid)
    comp += 'P {} {}\n'.format(xPos, yPos)
    comp += 'F 0 "{}?" H {} {} 50  0 000 L CNN\n'.format(ref, xPos+10, yPos+200)
    comp += 'F 1 "{}" H {} {} 50  0 000 C CNN\n'.format(value, xPos, yPos-100)
    comp += 'F 2 "" H {} {} 50  0 000 C CNN\n'.format(xPos, yPos+200)
    comp += 'F 3 "" H {} {} 50  0 000 C CNN\n'.format(xPos, yPos+200)
    comp += '\t1    {} {}\n'.format(xPos, yPos)
    comp += '\t{}    0    0    -1\n'.format('-1' if mirrorH else '1')
    comp += '$EndComp\n'
    return comp

def label(name, xPos, yPos, orient, type = 'Input'):
    labelText =  'Text GLabel {} {} {}    60   {} ~ 0\n{}\n'.format(xPos, yPos, orient, type, name)
    return labelText

def wire(xStart, yStart, xEnd, yEnd):
    return 'Wire Wire Line\n {} {} {} {}\n'.format(xStart, yStart, xEnd, yEnd)

def textBlock(text, posX, posY, vertical = 0, dimension = 180):
    return 'Text Notes {} {} {} {}  ~ 24\n{}\n'.format(posX, posY, vertical, dimension, text)

def connection(posX, posY):
    return 'Connection ~ {} {}\n'.format(posX, posY)
