"""
Clone of 2048 game.
"""

import poc_2048_gui
import random

# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Offsets for computing tile indices in each direction.
# DO NOT MODIFY this dictionary.
OFFSETS = {UP: (1, 0),
           DOWN: (-1, 0),
           LEFT: (0, 1),
           RIGHT: (0, -1)}

def merge(line):
    """
    Helper function that merges a single row or column in 2048
    """
    # replace with your code from the previous mini-project
    result = [0 for value in line]
        
    
    dummy_idx = 0    
    
    for idx, value in enumerate(line):
        if value != 0 :
            result[dummy_idx] = value
            dummy_idx += 1
            
    #new_result = [value for value in result]
    
    for idx in range(len(result)-1):
        
        if result[idx] == result[idx+1]:
            result[idx] = (2*result[idx])
            for dummy_idx in range(idx+1,len(result)-1):
                result[dummy_idx]=result[dummy_idx+1]
            result[len(result)-1] = 0    
 
        
    
    return result

class TwentyFortyEight:
    """
    Class to run the game logic.
    """

    def __init__(self, grid_height, grid_width):
        # replace with your code
        self._grid_height = grid_height
        self._grid_width = grid_width
        self.reset()
        
        self._ini_tiles = {UP : [(0,idxu) for idxu in range(self._grid_width)],
                          DOWN : [(self._grid_height-1,idxd) for idxd in range(self._grid_width)],
                          LEFT : [(idxl,0) for idxl in range(self._grid_height)],
                          RIGHT : [(idxr,self._grid_width-1) for idxr in range(self._grid_height)]} 
        
    def reset(self):
        """
        Reset the game so the grid is empty except for two
        initial tiles.
        """
        # replace with your code
        self._board = [[0 for dummy_col in range(self._grid_width)] 
                       for dummy_row in range(self._grid_height)]
        for dummy_idx in range(2):
            self.new_tile()
         

    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        # replace with your code
        return str([val for val in self._board]).replace("],", "]\n") 
    
    def get_grid_height(self):
        """
        Get the height of the board.
        """
        # replace with your code
        return self._grid_height

    def get_grid_width(self):
        """
        Get the width of the board.
        """
        # replace with your code
        return self._grid_width

    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        # replace with your code
        
        legal_move= False
        
        for my_list in self._ini_tiles[direction]:
            temp_list = []
            
            list_row = my_list[0]
            list_col = my_list[1]
            
            if direction == UP or direction == DOWN:
                
                num_steps = self._grid_height
            
            else:
                
                num_steps = self._grid_width
                
            for step in range(num_steps):
                
                temp_list.append(self._board[list_row][list_col])
                list_row += OFFSETS[direction][0]
                list_col += OFFSETS[direction][1]
                
            temp_list = merge(temp_list)
            
            list_row = my_list[0]
            list_col = my_list[1]
            
            for step in range(num_steps):
                
                if self._board[list_row][list_col] != temp_list[step]:
                    legal_move = True
                
                self._board[list_row][list_col] = temp_list[step]
                list_row += OFFSETS[direction][0]
                list_col += OFFSETS[direction][1]
            
        if legal_move:
            self.new_tile()
                
            
    def new_tile(self):
        """
        Create a new tile in a randomly selected empty
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        # replace with your code
        
        random_init_tile = random.random()
        if random_init_tile < 0.9:
            tile_value = 2
        else:
            tile_value = 4
        
            
        new_tile = (random.randrange(0, self._grid_height),
                               random.randrange(0, self._grid_width))
        
        while self.get_tile(new_tile[0], new_tile[1]) != 0:
            
            new_tile = (random.randrange(0, self._grid_height),
                               random.randrange(0, self._grid_width))
        
        self.set_tile(new_tile[0], new_tile[1],tile_value)	
           

    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """
        # replace with your code
        self._board[row][col] = value

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """
        # replace with your code
        return self._board[row][col]


poc_2048_gui.run_gui(TwentyFortyEight(4, 4))