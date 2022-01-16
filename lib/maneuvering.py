""" Functions for basic maneuvering """

from picarx_improved import Picarx
import logging
from time import sleep

# Setup logging format
logging_format = "%(asctime)s: %(message)s"
logging.basicConfig(format=logging_format, level=logging.INFO,
    datefmt="%H:%M:%S")

LEFT = 1
RIGHT = 2

def move(px: Picarx, speed: int, angle: int)->None:
    # Enforce speed boundaries
    max_speed = 100
    if speed > max_speed:
        logging.warning("Requested forwards speed higher than max speed. Set speed to max forwards speed.")
        speed = max_speed
    elif speed < -max_speed:
        logging.warning("Requsted backwards speed higher than max speed. Set speed to max backwards speed.")
        speed = -max_speed
    
    # Enforce angle boundaries
    max_angle = 30
    if angle > max_angle:
        logging.warning("Requested right-steering angle greater than max angle. Set angle to max angle right.")
        angle = max_angle
    elif angle < -max_angle:
        logging.warning("Requested left-steering angle greater than max angle. Set angle to max angle left.")
        angle = -max_angle

    # Send movement commands to picar
    px.set_dir_servo_angle(angle)
    if speed >= 0:
        px.forward(speed)
    else:
        px.backward(abs(speed))

def parallel_park(px: Picarx, dir: int)->None:
    # Setup sign for LEFT or RIGHT
    if dir == LEFT:
        sign = 1
    else:
        sign = -1
    # Set parking parameters
    speed = 20
    angle = 20
    pause_duration = 2 # seconds
    # Send robot commands for parking
    # Comments are for LEFT parking
    # Left forward
    move(px, speed, sign* -angle)
    sleep(pause_duration)
    # Right forward
    move(px, speed, sign * angle)
    sleep(pause_duration)
    # Left backward
    move(px, -speed, sign * -angle)
    sleep(pause_duration)
    # Right backward
    move(px, -speed, sign * angle)
    sleep(pause_duration)
    # Stop
    move(px, 0, 0)

def k_turn(px: Picarx, dir: int)->None:
    # Setup sign for LEFT or RIGHT
    if dir == LEFT:
        sign = 1
    else:
        sign = -1
    # Set turn parameters
    speed = 20
    angle = 30
    pause_duration = 2 # seconds
    # Send robot commands for turn
    # Comments are for LEFT K-turn
    # Left forward
    move(px, speed, -angle)
    sleep(pause_duration)
    # Right backward
    move(px, -speed, angle)
    sleep(pause_duration/2)
    # Left forward
    move(px, speed, -angle)
    sleep(pause_duration)
    # Forward 
    move(px, speed, 0)
    sleep(pause_duration/2)
    # Stop
    move(px, 0, 0)