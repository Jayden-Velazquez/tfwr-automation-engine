import dm

positions = [(0,0), (5,5), (4,1), (4,5), (5,5), (1,1)]

for pos in positions:
	quick_print(pos)
	dm.goto_world_pos(pos)