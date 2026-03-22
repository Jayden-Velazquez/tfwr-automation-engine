from watering import *
from pumpkin import create_world_pumpkin
from harvest import *
from constants import *
import dm

farm_info = None

clear()
change_hat(Hats.Traffic_Cone_Stack)
while True:
	dm.goto_origin()
	if farm_info == None:
		farm_info = plan_plots([SUNFLOWER, CARROT, GRASS, PUMPKIN, BUSH])
	harvest_entities(farm_info)
	