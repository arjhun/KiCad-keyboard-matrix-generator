#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
KiCad EEschema key matrix generator
Arjen Klaverstijn 2018
"""
from __future__ import print_function

import argparse
import sys
import os
import eeschema_common as eeschema

__version__ = '0.1'

def create_key_matrix(args):
    #create a hex ecoded string as id
    #loop through rows
    matrix = []
    blockHeight = 500
    labelConnectionWidth = 200
    switchWidth = 400
    diodeWidth = 300
    gap = 50

    for row in range(args.numRows):

        posY = args.yPos+(blockHeight*row)
        rowLabelX = args.xPos
        rowLabelY = posY
        matrix +=  eeschema.label(args.rowLabel+str(row), rowLabelX , rowLabelY, 0, 'Output')
        posY+=blockHeight/2

        for col in range(args.numCols):
            posX = args.xPos + labelConnectionWidth + ((switchWidth+diodeWidth+gap)*col)
            blockRs = posX+switchWidth+diodeWidth
            switchX = posX + switchWidth/2
            diodeX = switchX + switchWidth/2 + diodeWidth/2
            #place components
            matrix += eeschema.component('Switch:SW_Push', 'SW_Push', 'SW', eeschema.createId(), switchX, posY, args.sFootprint)
            orientMatrix = [-1 if args.revDiode else 1, 0,0,-1]
            matrix += eeschema.component('Diode:1N4148', '1N4148', 'D', eeschema.createId(), diodeX, posY, args.dFootprint, orientMatrix)
            #switch left side wire and junction
            matrix += eeschema.connection(posX, rowLabelY)
            matrix += eeschema.wire(posX,rowLabelY,posX, posY)
            #diode right side junction
            if row > 0 :
                matrix += eeschema.connection(blockRs, posY)
            #last row operations
            if row == args.numRows-1 :
                colLabelY = posY+labelConnectionWidth
                matrix += eeschema.label(args.colLabel+str(col), blockRs, colLabelY, 3)
                matrix += eeschema.wire(blockRs,args.yPos+blockHeight/2,blockRs,colLabelY)
                matrix += eeschema.textBlock('{} {}x{}'.format(args.title,args.numRows,args.numCols),args.xPos,args.yPos-100)

        matrix += eeschema.wire(rowLabelX,rowLabelY,posX,rowLabelY)

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
    parser.add_argument('-df', '--dFootprint', type=str, help='Diode footprint association', default="")
    parser.add_argument('-sf', '--sFootprint', type=str, help='Switch footprint association', default="")
    parser.add_argument('-rd','--revDiode', help='Reverse diode direction', action='store_true')
    parser.add_argument('output', help='Output schematic file (*.sch), it will insert the matrix into it!', nargs='?', type=argparse.FileType('r'), default=sys.stdout )
    parser.add_argument('-v','--version', action='version', version='%(prog)s '+__version__)

    args = parser.parse_args()
    matrix = create_key_matrix(args)

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
            print('Creating {}x{} matrix... in {}'.format(args.numRows, args.numCols,args.output.name))
            #create a little visual representation of the matrix
            for r in range(args.numRows):
                k = ""
                for c in range(args.numCols):
                    k+=chr(254)+" "
                print(k)
            #write the matrix to the eeschema file
            for line in args.output:
                if line.startswith('$EndSCHEMATC'):
                    buff.writelines(matrix)
                buff.write(line)
            #close files
            buff.close()
            args.output.close()
            os.rename(args.output.name, args.output.name+'.'+str(eeschema.createId())+'.bak')
            os.rename(buff.name, args.output.name)
            print ('Done!')
        else:
            sys.exit('Not a KiCad EEschema file! exiting!')
    else:
        args.output.writelines(matrix)
