import RPi.GPIO as GPIO
import time
GPIO.cleanup()
GPIO.setmode(GPIO.BOARD)
motor_1_pins = 13, 15
motor_2_pins =  16, 18
ena = 38
enb = 40
for pin in motor_1_pins + motor_2_pins:
    GPIO.setup(pin, GPIO.OUT)
def set_motor_a(direction):
    if direction == 0:
        GPIO.output(ena, False)
    elif direction == 1:
        GPIO.output(ena, True)
        GPIO.output(motor_1_pins[0], False)
        GPIO.output(motor_1_pins[1], True)
    elif direction == 2:
        GPIO.output(ena, True)

        GPIO.output(motor_1_pins[1], False)
        GPIO.output(motor_1_pins[0], True)
def set_motor_b(direction):
    if direction == 0:
        GPIO.output(enb, False)
    elif direction == 1:
        GPIO.output(enb, True)
        GPIO.output(motor_2_pins[0], False)
        GPIO.output(motor_2_pins[1], True)
    elif direction == 2:
        GPIO.output(enb, True)

        GPIO.output(motor_2_pins[1], False)
        GPIO.output(motor_2_pins[0], True)
def move(seconds, direction):
    assert direction in (0, 1, 2, 3)
    if direction == 0:
        set_motor_a(1)
        set_motor_b(1)
    elif direction == 1:
        set_motor_a(2)
        set_motor_b(2)
    elif direction == 2:
        set_motor_a(2)
        set_motor_b(1)
    elif direction == 3:
        set_motor_a(1)
        set_motor_b(2)
    time.sleep(seconds)
    set_motor_a(0)
    set_motor_b(0)
if __name__ == "__main__":
    move(9, 1)
