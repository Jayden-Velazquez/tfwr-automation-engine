import dm
from math_utils import *
from watering import *
from pumpkin import *
from constants import *

# Harvests all mature crops in the world
def harvest_all():
	dm.goto_origin()
	for i in range(get_world_size()):
		for j in range(get_world_size()):
			if can_harvest():
				harvest()
			dm.right()
		dm.up()

# Harvests all mature crops and then clears the world
def harvest_all_clear():
	harvest_all()
	clear()
	
# Fulfills prerequisites before planting the crop
def smart_plant(crop):
	if crop == GRASS:
		if get_ground_type() != GRASSLAND:
			till()
	
	elif crop == CARROT or crop == PUMPKIN or crop == SUNFLOWER:
		if get_ground_type() != SOIL:
			till()
	
	elif crop == BUSH or crop == TREE:
		even = ((get_pos_x() + get_pos_y()) % 2 == 0)
		crop = BUSH
		if even:
			crop = TREE
	
	if crop != GRASS:
		plant(crop)

# plants a crop in all positions given
def multi_plant(crop, all_pos, edge = -999):
	start_x, start_y = all_pos[len(all_pos) - 1][0], all_pos[len(all_pos) - 1][1]
	for pos in all_pos:
		if (pos[0] != start_x - edge) and (pos[1] != start_y - edge):
			dm.goto_world_pos(pos)
			smart_plant(crop)

# plants a crop in a plot (matrix)
def plant_plot_matrix(crop, plot_matrix, edge = -1):
	size = len(plot_matrix)
	end = plot_matrix[len(size) - 1][len(plot_matrix[size - 1])]

	for i in range(crop, size - 1):
		for j in range(len(plot_matrix[size - 1]) - 1):
			pos = plot_matrix[i][j]
			if (pos[0] != (end[0] - edge)) and (pos[1] != (end[1] - edge)):
				dm.goto_world_pos(plot_matrix[i][j])
				smart_plant(crop)


def harvest_entities(crop_list, fit_to_world = False):
	farm_info = plan_plots(crop_list, fit_to_world)

	all_plots = farm_info["all_plots"]
	sunflowers_dict = farm_info["sunflowers_dict"]
	replant_sunflowers = True

	while True:
		for key in all_plots:
			this_plot = all_plots[key]
			route = this_plot["route"]
			plot_crop = this_plot["plot_crop"]
			block_crops = this_plot["block_crops"]

			dm.goto_world_pos(key)

			for pos in route:
				crop = block_crops[pos]

				if crop == GRASS or crop == BUSH or crop == TREE or crop == CARROT:
					dm.goto_world_pos(pos)
					if can_harvest():
						harvest()
						smart_plant(crop)

				elif crop == PUMPKIN:
					not_grown = this_plot["not_grown"]
					# using set() is required here to make a new set and not use the actual reset_not_grown set
					reset_not_grown = set(this_plot["reset_not_grown"])

					if pos in not_grown:
						dm.goto_world_pos(pos)
						if can_harvest() and get_entity_type() == PUMPKIN:
							not_grown.remove(pos)
							if len(not_grown) == 0:
								harvest()
								this_plot["not_grown"] = reset_not_grown

						if not can_harvest() or get_entity_type() != PUMPKIN:
							smart_plant(PUMPKIN)
				
				elif crop == SUNFLOWER:
					idx = sunflowers_dict["most_idx"]
					sorted_sunflowers = sunflowers_dict["sorted_sunflowers"]
					all_sunflowers = sunflowers_dict["all_sunflowers"]

					if pos in all_sunflowers and pos in sorted_sunflowers[idx]:
						dm.goto_world_pos(pos)
						if can_harvest():
							harvest()
							all_sunflowers.remove(pos)
							sorted_sunflowers[idx].remove(pos)

							while len(sorted_sunflowers[idx]) == 0 and idx != -1:
								idx -= 1

							sunflowers_dict["most_idx"] = idx

							if len(all_sunflowers) < 10:
								replant_sunflowers = True

					if pos not in all_sunflowers and replant_sunflowers:
						dm.goto_world_pos(pos)
						smart_plant(SUNFLOWER)
						petal_count = measure()

						all_sunflowers.add(pos)
						sorted_sunflowers[(petal_count - MIN_SUNFLOWER_PETALS)].add(pos)

						if (petal_count - MIN_SUNFLOWER_PETALS) > idx:
							sunflowers_dict["most_idx"] = petal_count - MIN_SUNFLOWER_PETALS

						if len(all_sunflowers) >= sunflowers_dict["expected_sunflowers"]:
							replant_sunflowers = False
							
	

def plan_plots(crop_list, fit_to_world = False):
	if fit_to_world:
		_ = 0
		while len(crop_list) < (get_world_size()):
			crop_list.append(crop_list[_])
			_ += 1
			
		while len(crop_list) > (get_world_size()):
			crop_list.pop()
		
	num_crops = len(crop_list)
	total_blocks = get_world_size() ** 2
	blocks_per_crop = total_blocks/num_crops
	plot_size = floor(sqrt(blocks_per_crop))
	
	world_corner = (get_world_size() - 1, get_world_size() - 1)
	outer_route = dm.get_route(ORIGIN, world_corner, False, plot_size)

	farm_info = dict()
	all_plots = dict()

	# Sunflower specific logic
	sunflower_plots = 0
	sunflowers_dict = dict()
	sunflowers_dict["sorted_sunflowers"] = [set(), set(), set(), set(), set(), set(), set(), set(), set()]
	sunflowers_dict["most_idx"] = -1
	sunflowers_dict["all_sunflowers"] = set()

	i = 0

	for out_pos in outer_route:
		inner_route_start = out_pos
		inner_route_end = (out_pos[0] + plot_size, out_pos[1] + plot_size)
		inner_route = dm.get_route(inner_route_start, inner_route_end)

		crop = crop_list[i]
		this_plot = dict()

		this_plot["route"] = inner_route
		this_plot["plot_crop"] = crop
		this_plot["plot_size"] = plot_size
		
		if crop == PUMPKIN:
			this_plot["not_grown"] = set()
			this_plot["reset_not_grown"] = set()

		if crop == SUNFLOWER:
			sunflower_plots += 1

		block_crops = dict()
		for in_pos in inner_route:
			if this_plot["plot_crop"] == PUMPKIN:
				out_x = out_pos[0]
				out_y = out_pos[1]

				in_x = in_pos[0]
				in_y = in_pos[1]

				if in_x == (out_x + plot_size - 1) or in_y == (out_y + plot_size - 1):
					crop = GRASS
				else:
					this_plot["not_grown"].add(in_pos)
					this_plot["reset_not_grown"].add(in_pos)
					crop = PUMPKIN


			block_crops[in_pos] = crop

		this_plot["block_crops"] = block_crops
		all_plots[out_pos] = this_plot

		i += 1
		if i >= len(crop_list):
			i = 0

	farm_info["all_plots"] = all_plots

	expected_sunflowers = (plot_size**2) * sunflower_plots
	sunflowers_dict["expected_sunflowers"] = expected_sunflowers
	farm_info["sunflowers_dict"] = sunflowers_dict

	return farm_info

