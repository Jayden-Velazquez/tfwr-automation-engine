import dm

dm.goto_origin()

# Assuming drone is at (0, 0)
quick_print("--- Testing Scenario 2a: (0, 0) to (9, 0) ---")
dm.goto_world_pos((8, 0))
dm.goto_world_pos((7, 0))

# Visual verification: Did the drone move East 9 times, or West 1 time?
# Check current position:
quick_print("Final X Position: ", get_pos_x()) # Should output 9

# Reset drone position to (0, 0) if needed for the next test
# ... (Use your game's reset function here)