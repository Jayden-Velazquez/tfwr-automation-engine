import dm
from watering import *

# Plants a pumpkin on every block of the world until a pumpkin with side
# lengths = the worls size is created. 
def create_world_pumpkin():
	not_grown = []
	for i in range(get_world_size()):
		for j in range(get_world_size()):
			if get_ground_type() != Grounds.Soil:
				till()
			plant(Entities.Pumpkin)
			#maintain_water_level()
			not_grown.append((get_pos_x(), get_pos_y()))
			dm.right()
		dm.up()
		
	pumpkin_treatment(not_grown)
	dm.goto_origin()
	
# args: a list of positions (x,y) corresponding to all immature pumpkins.
# Makes drone scan immature pumpkins and replant over dead_pumpkins
def pumpkin_treatment(not_grown):
	while not_grown:
		temp = []
		for pos in not_grown:
			dm.goto_world_pos(pos)
			if not can_harvest():
				temp.append((get_pos_x(), get_pos_y()))
			if get_entity_type() != Entities.Pumpkin:
				plant(Entities.Pumpkin)
			#maintain_water_level()
		not_grown = temp
		
# args: list of not_grown pumpkin coordinates (x,y).
# checks the positions in the list once and replants dead_pumpkins
def pumpkin_check_up(not_grown):
	for pos in not_grown:
		dm.goto_world_pos(pos)
		if get_entity_type() != Entities.Pumpkin:
			plant(Entities.Pumpkin)
		else:
			not_grown.remove(pos)

# args: a list of positions (x,y).
# plants pumpkins at each position
def plant_pumpkins(all_pos, edge = -1):
	start_x, start_y = all_pos[len(all_pos) - 1][0], all_pos[len(all_pos) - 1][1]
	for pos in all_pos:
		if (pos[0] != start_x - edge) and (pos[1] != start_y - edge):
			dm.goto_world_pos(pos)
			if get_ground_type() != Grounds.Soil:
				till()
			plant(Entities.Pumpkin)

if __name__ == "__main__":
	create_world_pumpkin()