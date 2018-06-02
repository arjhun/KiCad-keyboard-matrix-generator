#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
KiCad EEschema key matrix generator
Arjen Klaverstijn 2018
"""
from __future__ import print_function

import argparse
import time
import sys
import os

tm = int(time.time())

def createId():
    global tm
    id = format(int(tm),'x')
    tm += 1
    return id

def component(type, value, ref, timestamp, xPos, yPos, mirrorH = False):

    comp = '$Comp\n'
    comp += 'L {} {}?\n'.format(type, ref)
    comp += 'U 1 1 {}\n'.format(timestamp)
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

def create_key_matrix(numRows, numCols, startX, startY, title = "Key Matrix", rowId = 'R', colId = 'C', revDiode = False):
    #create a hex ecoded string as timestamp id
    #loop through rows
    matrix = []
    blockHeight = 500

    for row in range(numRows):

        posY = startY+(blockHeight*row)
        labelX = startX-500
        labelY = posY
        matrix +=  label(rowId+str(row), labelX , labelY, 0, 'Output')
        posY+=blockHeight/2

        for col in range(numCols):
            posX = startX+(col*750)
            #place components
            matrix += component('SW_Push', 'KEY', 'SW', createId(), posX, posY)
            matrix += component('D', 'Diode', 'D', createId(), posX+350, posY, revDiode)
            #switch left side wire and junction
            matrix += connection(posX-200, labelY)
            matrix += wire(posX-200,labelY,posX-200,posY)
            #diode right side junction
            if row > 0 :
                matrix += connection(posX+500, posY)
            #last row operations
            if row == numRows-1 :
                colLabelX = posX+500
                colLabelY = posY+400
                matrix += label(colId+str(col), colLabelX, colLabelY, 3)
                matrix += wire(posX+500,startY+blockHeight/2,posX+500,colLabelY)
                matrix += textBlock('{} {}x{}'.format(title,numRows,numCols),startX,startY-100)

        matrix += wire(labelX,labelY,posX-200,labelY)

    return matrix

if __name__ == "__main__":
    #parse arguments
    parser = argparse.ArgumentParser(description='Generate a switch/ diode key matrix in EEschema by Arjen Klaverstijn',formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('-r', '--numRows', type=int, help='The number of rows', required=True)
    parser.add_argument('-c', '--numCols', type=int, help='The number of collumns', required=True)
    parser.add_argument('-x', '--xPos', type=int, help='The x position of the first switch in the matrix', default=0)
    parser.add_argument('-y', '--yPos', type=int, help='The y position of the first switch in the matrix', default=0)
    parser.add_argument('-t', '--title', type=str, help='Title label for the matrix', default="Key Matrix")
    parser.add_argument('-rl', '--rowLabel', type=str, help='Row label prefix', default="row")
    parser.add_argument('-cl', '--colLabel', type=str, help='Row label prefix', default="col")
    parser.add_argument('-rd','--revDiode', help='Reverse diode direction', action='store_true')
    parser.add_argument('output', help='Output schematic file (*.sch), it will insert the matrix into it!', nargs='?', type=argparse.FileType('r'), default=sys.stdout )

    args = parser.parse_args()

    matrix = create_key_matrix(args.numRows,args.numCols, args.xPos, args.yPos, args.title, args.rowLabel, args.colLabel, args.revDiode)

    #check if output is stdout
    if not args.output == sys.stdout:
        #check if eeschema file format
        firstLine = args.output.readline()
        args.output.seek(0)

        if 'EESchema Schematic File' in firstLine:
            print('Found a KiCad schematic file!')
            #loop through lines and coppy to buffer so we can make a backup of the original file later
            buffPath = os.path.dirname(args.output.name)+'\\temp.buf'
            buff = open(buffPath, 'w')
            print('Creating matrix...')
            #create a little visual representation of the matrix
            for r in range(args.numRows):
                k = ""
                for c in range(args.numCols):
                    k+=chr(254)
                print(k)
            #write the matrix to the eeschema file
            for line in args.output:
                if line.startswith('$EndSCHEMATC'):
                    buff.writelines(matrix)
                buff.write(line)
            #close files
            buff.close()
            args.output.close()
            os.rename(args.output.name, args.output.name+'.'+str(createId())+'.bak')
            os.rename(buff.name, args.output.name)
            print ('Done!')
        else:
            sys.exit('Not a KiCad EEschema file! exiting!')
    else:
        args.output.writelines(matrix)
