#!/usr/bin/env pybricks-micropython

from threading import Thread

from pybricks.ev3devices import (ColorSensor, GyroSensor, InfraredSensor,
                                 Motor, TouchSensor, UltrasonicSensor)
from pybricks.parameters import (Align, Button, Color, Direction, ImageFile,
                                 Port, SoundFile, Stop)
from pybricks.robotics import DriveBase
from pybricks.tools import StopWatch, print, wait

from pybricks.hubs import EV3Brick

from pybricks.media.ev3dev import Font

import random
import time

big_font = Font(size=20, bold=True, monospace=True)

ev3 = EV3Brick()
ev3.screen.set_font(big_font)


def reset(motor: Motor):
    motor.run_until_stalled(100, Stop.BRAKE, 50)


def scan(motor: Motor):
    global scan_done
    global scan_started
    scan_started = True
    motor.run_until_stalled(-50, Stop.BRAKE, 25)
    scan_done = True


def read_colors(motor: Motor, color: ColorSensor):
    detected = color.color()
    detected_colors = []
    global scan_done
    global scan_started

    while not len(detected_colors) == 4:
        detected_colors.clear()
        scan_started = False
        scan_done = False
        scan.start()

        while(not(scan_started)):
            pass

        while(not(scan_done)):
            detected = color.color()
            if (detected in POSSIBLE_COLORS and detected not in detected_colors):
                detected_colors.append(detected)

        if len(detected_colors) < 4:
            reset(motor)

    return detected_colors


scan_started = False
scan_done = False

motor = Motor(Port.A)
color = ColorSensor(Port.S1)
start = TouchSensor(Port.S4)

POSSIBLE_COLORS = [Color.YELLOW, Color.GREEN, Color.RED, Color.BLUE]

scan = Thread(target=scan, args=[motor])

colors_to_guess = list.copy(POSSIBLE_COLORS)

while True:
    ev3.screen.clear()
    seed = int(round(time.time() * 1000))
    random.seed(seed)
    random.shuffle(colors_to_guess)
    attempt = []

    while colors_to_guess != attempt:
        reset(motor)
        while not start.pressed():
            pass

        attempt = read_colors(motor, color)
        score = []

        for idx in range(len(colors_to_guess)):
            if attempt[idx] == colors_to_guess[idx]:
                score.append('[OK]')
            else:
                score.append('[__]')

        ev3.screen.print(" ".join(map(str, score)))
        if (colors_to_guess != attempt):
            ev3.speaker.play_file(SoundFile.CRYING)
        wait(2000)

    ev3.speaker.play_file(SoundFile.BRAVO)
    reset(motor)
