# Killer Sudoku Solver using Z3
Killer sudoku is a modified version of sudoku which adds the rule of cages to the game. Each cage is indicated by a dotted line surrounding one or more cells, and in each cage a number is written which indicates the sum of the surrounded cells. All other sudoku rules apply here as well.

## Setup
Install the Z3 theorem solver Python library by using the command:
`pip install z3`
assuming that you already have Python 3 and Pip installed on your device. If not, you can [download Python 3 here](https://www.python.org/downloads/) which also includes pip.

## Usage
To run the killer-sudoku.py file:
  * On Windows, use command `python killer-sudoku.py --file_path <insert game json file here>`
  * On Linux, use command `./killer-sudoku.py --file_path <insert game json file here>`

## File formatting
The JSON board files have two arguments, an integer length (which indicates the size of the board) and a list called boxes. The boxes argument is a list of pairs containg cells and a sum for each box. The cells list is a series of ordered pairs which indicate which cells make up each box, and the sum indicates the integer sum of the box. When the boxes list is empty or not complete for the entire grid, the solver still works and produces an answer if possible. In the case of no boxes, the game could be considered a very easy version of normal sudoku. 
Below is an example of a 4x4 board JSON file.

    {"length": 4,
        "boxes": [
            {
                "cells": [[0,0], [1,0], [1,1]],
                "sum": 6
            },
            {
                "cells": [[0,1], [0,2]],
                "sum": 7
            },
            {
                "cells": [[0,3], [1,3]],
                "sum": 5
            },
            {
                "cells": [[1,2], [2,2]],
                "sum": 6
            },
            {
                "cells": [[2,0], [3,0]],
                "sum": 7
            },
            {
                "cells": [[2,1], [3,1]],
                "sum": 3
            },
            {
                "cells": [[2,3], [3, 2], [3,3]],
                "sum": 6
            }
        ]
    }
