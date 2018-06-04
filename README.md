## create_key_matrix.py
#### Examples:

6x10 matrix with diodes pointing at the collumns:

```sh
/home/user/kicad_projects/60key_keyboard/$ create_key_matrix.py -r 6 -c 10 -t "Keyboard matrix" -rl "key_row" -cl "key_col" --revDiode 60key_keyboard.sch
```
```
Found a KiCad schematic file!
Creating 2x10 matrix... in /home/user/kicad_projects/60key_keyboard/60key_keyboard.sch
■ ■ ■ ■ ■ ■ ■ ■ ■ ■
■ ■ ■ ■ ■ ■ ■ ■ ■ ■
Done!
```

### KiCad

![Imgur](https://i.imgur.com/OdTqsCL.png)

output only the matrix to a file via stdout

```sh
$ create_key_matrix.py -r 6 -c 10 -t "Keyboard matrix" -rl "key_row" -cl "key_col" --revdiode > matrix.txt
```

### All parameters:

```
$ create_key_matrix.py -h
```
```
usage: create_key_matrix.py [-h] -r NUMROWS -c NUMCOLS [-x XPOS] [-y YPOS]
                            [-t TITLE] [-rl ROWLABEL] [-cl COLLABEL]
                            [-df DFOOTPRINT] [-sf SFOOTPRINT] [-rd] [-v]
                            [output]

Generate a switch/ diode key matrix in EEschema by Arjen Klaverstijn

positional arguments:
  output                Output schematic file (*.sch), it will insert the
                        matrix into it! (default: <open file '<stdout>', mode
                        'w' at 0x01CC5078>)

optional arguments:
  -h, --help            show this help message and exit
  -r NUMROWS, --numRows NUMROWS
                        The number of rows (default: None)
  -c NUMCOLS, --numCols NUMCOLS
                        The number of collumns (default: None)
  -x XPOS, --xPos XPOS  The x position of the first switch in the matrix
                        (default: 0)
  -y YPOS, --yPos YPOS  The y position of the first switch in the matrix
                        (default: 0)
  -t TITLE, --title TITLE
                        Title label for the matrix (default: Key Matrix)
  -rl ROWLABEL, --rowLabel ROWLABEL
                        Row label prefix (default: row)
  -cl COLLABEL, --colLabel COLLABEL
                        Row label prefix (default: col)
  -df DFOOTPRINT, --dFootprint DFOOTPRINT
                        Diode footprint association (default: )
  -sf SFOOTPRINT, --sFootprint SFOOTPRINT
                        Switch footprint association (default: )
  -rd, --revDiode       Reverse diode direction (default: False)
  -v, --version         show program's version number and exit
  ```
