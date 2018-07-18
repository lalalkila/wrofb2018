import math

def ProcessInput():
	raw_value = ir_seeker.direction()
	if raw_value == 5:
		return 5
	elif raw_value == 0:
		return 0
	elif raw_value < 5:
		return 4
	else:
		return 6

def update(main_heading, ir_direction):
	if ir_direction == 5:
		#khong lam gi het
		continue
	elif ir_direction == 4:
		#def_trai
		while compass.relative(main_heading) >= -45:
			move(0.01, 100, 100)
		while motor.rotation() < 0.5:
			move(0, 100, 100)
		while ir_seeker.direction > 5:
			move(0, -100, -100)
		CanBang()
	elif ir_direction == 6:
		while compass.relative(main_heading) >= 45:
			move(0.01, -100, -100)
		while motor.rotation() < -0.5:
			move(0, -100, -100)
		while ir_seeker.direction > 5:
			move(0, 100, 100)
		CanBang()

	else:
		CanBang()


def CurrentPOS(current_pos = 0, ):
	if (current_pos > 0 && motor.port('A'). rotation() > 0) ||
		(current_pos < 0 && motor.port('A').rotation() < 0):
		if motor.port('A').rotation() >= 0:
			current_pos += motor.port('A').rotation()
		else:
			current_pos = motor.port('A').rotation() - current_pos
	else:
		if abs(motor.port('A').rotation()) > abs(current_pos):
			if motor.port('A').rotation() >= 0:
				current_pos = abs(motor.port('A').rotation()) - abs(current_pos)
			else:
				current_pos	= -(abs(motor.port('A').rotation()) - abs(current_pos))
	return current_pos

while __name__ == '__main__':
	main_heading = compass.direction()
	while True:
		ir_direction = ProcessInput()
		update(main_heading, ir_direction)
