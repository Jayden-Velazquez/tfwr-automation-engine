from watering import *
from pumpkin import create_world_pumpkin
from harvest import *
from constants import *
import dm

clear()
change_hat(Hats.Traffic_Cone_Stack)
while True:
	dm.goto_origin()
	harvest_entities([SUNFLOWER, GRASS, BUSH, CARROT, PUMPKIN], True)
	