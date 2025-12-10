# dm = drone_movements

from constants import ORIGIN

# Moves drone "up" a single block
def up():
	move(North)
	
# Moves drone to the "top" of the world
def top():
	while get_pos_y() != get_world_size() - 1:
		up()
		
# Moves drone "down" a single block
def down():
	move(South)
	
# Moves drone to the "bottom" of the world
def bottom():
	while get_pos_y() != 0:
		down()
		
# Moves drone "right" one block
def right():
	move(East)
	
# Moves drone to the "far right" of the world
def far_right():
	while get_pos_x() != get_world_size() - 1:
		right()
		
# Moves drone "left" one block
def left():
	move(West)
	
# Moves drone to the "far left" of the world
def far_left():
	while get_pos_x() != 0:
		left()

# Moves the drone to the origin (0,0)
def goto_origin():
	goto_world_pos(ORIGIN)

def reverse_dir(dir):
	if dir == North:
		return South
	elif dir == South:
		return North
	elif dir == East:
		return West
	elif dir == West:
		return East

# args: direction to move drone, found = True when treasure found.
# Recursively moves till treasure is found 
def find_treasure(dir = North, found = False, visited = set()):
	old_pos = (get_pos_x(), get_pos_y())
	move(dir)
	new_pos = (get_pos_x(), get_pos_y())
	if new_pos in visited:
		if new_pos != old_pos:
			move(reverse_dir(dir))
		return found
	visited.add(new_pos)

	found = (get_entity_type() == Entities.Treasure)
	if found:
		harvest()
		return found
	
	found = find_treasure(North, found, visited)
	found = find_treasure(East, found, visited)
	found = find_treasure(South, found, visited)
	found = find_treasure(West, found, visited)
	
# Traverses the drone through every position in the list
def goto_all_pos(all_pos):
	for pos in all_pos:
		goto_world_pos(pos)

# args: a tuple pos containing (x, y) coordinates
# moves the drone to the given position by taking the shortest path
def goto_world_pos(target_pos):
	current_pos = (get_pos_x(), get_pos_y())
	
	move_right, move_left, move_up, move_down = False, False, False, False
	
	# quick_print(target_pos)
	if target_pos[0] > current_pos[0]:
		far_left_dist = current_pos[0]
		left_target_dist = far_left_dist + (get_world_size() - (target_pos[0]))
		right_target_dist = abs(target_pos[0] - current_pos[0])
		
		move_right = right_target_dist < left_target_dist
		move_left = not move_right
	else:
		far_right_dist = get_world_size() - (current_pos[0])
		right_target_dist = far_right_dist + target_pos[0]
		left_target_dist = abs(current_pos[0] - target_pos[0])
		
		move_left = left_target_dist < right_target_dist
		move_right = not move_left
	
	if target_pos[1] > current_pos[1]:
		far_down_dist = current_pos[1]
		down_target_dist = far_down_dist + (get_world_size() - (target_pos[1]))
		up_target_dist = abs(target_pos[1] - current_pos[1])
		
		move_up = up_target_dist < down_target_dist
		move_down = not move_up
	else:
		far_up_dist = get_world_size() - (current_pos[1])
		up_target_dist = far_up_dist + target_pos[1]
		down_target_dist = abs(current_pos[1] - target_pos[1])
		
		move_down = down_target_dist < up_target_dist
		move_up = not move_down
	
	while get_pos_x() != target_pos[0]:
		if move_right:
			right()
		elif move_left:
			left()
	
	while get_pos_y() != target_pos[1]:
		if move_up:
			up()
		elif move_down:
			down()

# args: start and end coordinates (x,y) with two movements scales for the x and y directions
# returns: coordinates for the drone to follow
def get_route(start_pos, end_pos, as_matrix = False, i_scale = 1, j_scale = 0):
	if j_scale == 0:
		j_scale = i_scale
		
	route = []
	x_len = end_pos[0] - start_pos[0]
	y_len = end_pos[1] - start_pos[1]
	
	x_dir = 1
	y_dir = 1
	
	if x_len < 0:
		x_dir = -1
	if y_len < 0:
		y_dir = -1
	
	for i in range(abs(y_len)):
		temp = []
		for j in range(abs(x_len)):
			x = start_pos[0] + j * j_scale * x_dir
			y = start_pos[1] + i * i_scale * y_dir
			if (x >= 0 and x < get_world_size()) and (y >= 0 and y < get_world_size()):
				if as_matrix:
					temp.append((x, y))
				else:
					route.append((x, y))

		if as_matrix:
			route.append(temp)
			
	return(route)
		
# Makes the drone do a thousand flips
def thousand_flips():
	for i in range(1, 1000):
		do_a_flip()
		quick_print("flip: " + str(i))