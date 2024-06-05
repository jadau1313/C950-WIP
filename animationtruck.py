import time
import os

# Define frames
frame1 = """
  __________________
 |                  |_____
 |  ===WGUPS===     |----|
 |                  |____|_____
 |                  |       []|
 |   _____          | _____-- |
 |__/ OOO \\_________|/ OOO \\__|
     OOOOO            OOOOO
      OOO  	       OOO 
      
      
	"""

frame2 = """
  __________________
 |                  |_____
 |  ===WGUPS===     |----|
 |                  |____|_____
 |                  |       []|
 |   _____          | _____-- |
 |__/  O  \\_________|/  O  \\__|
      OOO              OOO
      OOO  	       OOO    
      OOO              OOO
       O                O
"""
'''
frame3 = """

   o   *
  /|==-
 / |  |
  / \\ m
 /   \\

"""
'''
# Store frames in a list
frames = [frame1, frame2]


# Function to clear the console
def clear_console():
    # For Windows
    if os.name == 'nt':
        os.system('cls')
    # For macOS and Linux
    else:
        os.system('clear')


# Number of times the animation will loop
num_loops = 3

# Main animation loop
for _ in range(num_loops):
    for frame in frames:
        clear_console()
        print(frame)
        print('=============WGUPS=============')
        print('=========Let\'s   Roll!=========')
        time.sleep(0.5)  # Delay in seconds