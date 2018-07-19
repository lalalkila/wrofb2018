#!/usr/bin/env python3
from ev3dev.ev3 import * 
import ev3dev.ev3 as ev3
from math import sin, cos

def Init():
    color_sensor_1 = ev3.ColorSensor('in1')
    #assert color_sensor_1.connected(), "color_sensor_1 undetected!"
    color_sensor_1.mode = 'COL-AMBIENT'

    color_sensor_2 = ev3.ColorSensor('in2')
    #assert color_sensor_2.connected(), "color_sensor_2 undetected!"
    color_sensor_2.mode = 'COL-AMBIENT'

    IR_seeker = Sensor(address = 'i2c8', driver_name = 'ht-nxt-ir-seek-v2')
    #assert IR_seeker.connected(), "IR_seeker-v2 undetected!"
    IR_seeker.mode = 'DC'

    compass_sensor = Sensor(address = 'i2c1', driver_name = 'ht-nxt-compass')
    #assert compass_sensor.connected(), "compass_sensor undetected"

    motorA = MediumMotor('outA')
    motorB = MediumMotor('outB')
    motorC = MediumMotor('outC')
    motorD = MediumMotor('outD')

    return color_sensor_1, color_sensor_2, IR_seeker, compass_sensor, motorA, motorB, motorC, motorD

def relative():
    global compass_sensor, main_heading
    return ((main_heading - compass_sensor.value() + 180) % 360) - 180
    

def CanBang():
    if not relative() < 3 and relative() > -3:
        while True:
            if relative() > 3:
                move(-1000, -1000, 0.01)
            elif relative() < -3:
                move(1000, 1000, 0.01)
            else:
                break


def move(Vx, Vy, omega = 0, radius = 1):
    global motorA, motorB, motorC, motorD
    motorA.run_forever((omega * radius - Vx * cos(45) - Vy * sin(45)))
    motorB.run_forever((omega * radius - Vx * sin(45) + Vy * cos(45)))
    motorC.run_forever((omega * radius + Vx * sin(45) + Vy * cos(45)))
    motorD.run_forever((omega * radius + Vx * cos(45) - Vy * cos(45)))


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
        while relative() >= 45:
            move(1000, 1000, 0.01)
        motorA.COMMAND_RESET()
        while motorA.getTachoCount() < 0.5:
            move(1000, 1000, 0)
        while IR_seeker.value() > 5:
            move(-1000,-1000,0)
        CanBang()
    elif ir_direction == 6:
        while relative(main_heading) <= -45:
            move(-1000, -1000, 0.01)
        motorA.COMMAND_RESET()
        while motorA.getTachoCount() > -0.5:
            move(-1000, -1000, 0)
        while IR_seeker.value() < -5:
            move(1000,1000,0)
        CanBang()
    else:
        CanBang()

while __name__=='__main__':
    color_sensor_1 = ev3.ColorSensor('in1')
    #assert color_sensor_1.connected(), "color_sensor_1 undetected!"
    color_sensor_1.mode = 'COL-AMBIENT'

    color_sensor_2 = ev3.ColorSensor('in3')
    #assert color_sensor_2.connected(), "color_sensor_2 undetected!"
    color_sensor_2.mode = 'COL-AMBIENT'

    IR_seeker = Sensor(address = 'i2c8', driver_name = 'ht-nxt-ir-seek-v2')
    #assert IR_seeker.connected(), "IR_seeker-v2 undetected!"
    IR_seeker.mode = 'DC'

    compass_sensor = Sensor(address = 'i2c1', driver_name = 'ht-nxt-compass')
    #assert compass_sensor.connected(), "compass_sensor undetected"

    motorA = MediumMotor('outA')
    motorB = MediumMotor('outB')
    motorC = MediumMotor('outC')
    motorD = MediumMotor('outD')
    main_heading = compass_sensor.value()
    while True:
        ir_direction = ProcessInput()
        update(main_heading, ir_direction)