# Returns a number rounded down
def floor(num):
	return num // 1
	
# Returns a number rounded up
def ceil(num):
	if num == floor(num):
		return num
	return floor(num) + 1
	
# Truncates the remainder of a number
def trunc(num):
	if num > 0:
		return floor(num)
	return ceil(num)

# Returns the square root of a number
def sqrt(num):
	return num ** 0.5
	