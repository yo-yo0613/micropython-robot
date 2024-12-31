import wemotor
import time

motor = wemotor.Motor()

while True:
    motor.constantSpeed('forward' ,0.05,0.05)