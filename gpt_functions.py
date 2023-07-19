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
        
    elif direction == 1:
        pass
    elif direction == 2:
        pass
def move(seconds, direction):
    assert direction in (0, 1)
    if direction == 1:
        GPIO.output(11, True)
        GPIO.output(31, True)
        GPIO.output(12, False)
        GPIO.output(32, False)
    else:
        GPIO.output(12, True)
        GPIO.output(32, True)
        GPIO.output(11, False)
        GPIO.output(31, False)
    time.sleep(seconds)
    for pin in motor_1_pins + motor_2_pins:
        GPIO.output(pin, False)
if __name__ == "__main__":
    move(9, 1)
