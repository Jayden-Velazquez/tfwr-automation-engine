# Keeps water level at a minimum level
def maintain_water_level(min_water_level = 0.25):
	while get_water() < min_water_level:
		use_item(Items.water)
	