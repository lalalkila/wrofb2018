from ev3dev import ev3
from math import sin, cos

def Init():
    color_sensor_1 = ColorSensor('in1')
    assert color_sensor_1.connected(), "color_sensor_1 undetected!"
    color_sensor_1.mode = 'COL-AMBIENT'

    color_sensor_2 = ColorSensor('in2')
    assert color_sensor_2.connected(), "color_sensor_2 undetected!"
    color_sensor_2.mode = 'COL-AMBIENT'

    IR_seeker = Sensor(address = 'in4', driver = 'ht-nxt-ir-seek-v2')
    assert IR_seeker.connected(), "IR_seeker-v2 undetected!"
    IR_seeker.mode = 'DC'

    compass_sensor = Sensor(address = 'in2', driver = 'ht-nxt-compass')
    assert compass_sensor.connected(), "compass_sensor undetected"

    motorA = MediumMotor('outA')
    motorB = MediumMotor('outB')
    motorC = MediumMotor('outC')
    motorD = MediumMotor('outD')

    return color_sensor_1, color_sensor_2, IR_seeker, compass_sensor, motorA, motorB, motorC, motorD

class compass():
    global compass_sensor, main_heading
    def __init__():
        compass.relative = ((main_heading - compass_sensor.value() + 180) % 360) - 180
        compass.direction = compass_sensor.value()


def CanBang():
    if not compass.relative() < 3 && compass.relative() > -3:
        while True:
            if compass.relative > 3:
                move(-1000, -1000, 0.01)
            elif compass.relative < -3:
                move(1000, 1000, 0.01)
            else:
                break


def move(Vx, Vy, omega = 0, radius = 1):
    global motorA, motorB, motorC, motorD
    motorA.run_forever(omega * radius - Vx * cos(45) - Vy * sin(45))
    motorB.run_forever(omega * radius - Vx * sin(45) + Vy * cos(45))
    motorC.run_forever(omega * radius + Vx * sin(45) + Vy * cos(45))
    motorD.run_forever(omega * radius + Vx * cos(45) - Vy * cos(45))


def ProcessInput():
    global IR_seeker
    raw_value = IR_seeker.value()
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
        pass
    elif ir_direction == 4:
        while compass.relative(main_heading) >= 45:
            move(1000, 1000, 0.01)
        while Ev3.MotorRotation() < 0.5:
            move(1000, 1000, 0)
        while IR_seeker.value() > 5:
            move(-1000,-1000,0)
        CanBang()
    elif ir_direction == 6:
        while compass.relative(main_heading) >= -45:
            move(-1000, -1000, 0.01)
        while Ev3.MotorRotation() < 0.5:
            move(-1000, -1000, 0)
        while IR_seeker.value() > 5:
            move(1000,1000,0)
        CanBang()
    else:
        CanBang()

while __name__=='__main__':
    color_sensor_1, color_sensor_2, IR_seeker, compass_sensor, motorA, motorB, motorC, motorD = Init()
    main_heading = compass.direction()
    while True:
        ir_direction = ProcessInput()
        update(main_heading, ir_direction)
        except Exception:
            #Quitting