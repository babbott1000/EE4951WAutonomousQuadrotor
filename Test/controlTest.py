import numpy as np
import math
import time
import keyboard

import logging
import time
from threading import Thread


import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.log import LogConfig
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.positioning.motion_commander import MotionCommander
from cflib.utils import uri_helper

ALT_MODE_THRUST = 0
ALT_MODE_HEIGHT = 1

POS_MODE_PITCH_ROLL_THRUST = 0
POS_MODE_XYZ_VELOCITY = 1

POS_SET_DISABLED = 0

STAB_MODE_RATE = 0
STAB_MODE_ANGLE = 1

YAW_MODE_CAREFREE = 0
YAW_MODE_PLUSMODE = 1
YAW_MODE_XMODE = 2

ALT_MODE = ALT_MODE_THRUST
POS_MODE = POS_MODE_PITCH_ROLL_THRUST
POS_SET_MODE = POS_SET_DISABLED
YAW_MODE = YAW_MODE_XMODE
STAB_MODE_ROLL = STAB_MODE_ANGLE
STAB_MODE_PITCH = STAB_MODE_ANGLE
STAB_MODE_YAW = STAB_MODE_RATE

THRUST_INCREMENT = 200

URI = uri_helper.uri_from_env(default='radio://0/80/2M/E7E7E7E7E7')

def paramCallback(param, value):
    print(f"Param {param} has a default value of {value}")

thrust = 0

def increment_thrust(e):
    global thrust
    thrust += THRUST_INCREMENT

def decrement_thrust(e):
    global thrust
    thrust -= THRUST_INCREMENT

if __name__ == '__main__':
    keyboard.on_press_key('w', increment_thrust)
    keyboard.on_press_key('s', decrement_thrust)

    print("Initializing drivers")

    # Initialize the low-level drivers
    cflib.crtp.init_drivers()
    
    print("Connecting to drone")

    with SyncCrazyflie(URI, cf=Crazyflie(rw_cache='./cache')) as scf:
        print("Connected to drone")

        print("The link is open" if scf.is_link_open() else "The link is not open")

        print("Setting parameters")

        scf.wait_for_params()

        scf.cf.param.set_value("flightmode.althold", ALT_MODE)
        scf.cf.param.set_value("flightmode.poshold", POS_MODE)
        scf.cf.param.set_value("flightmode.posSet", POS_SET_MODE)
        scf.cf.param.set_value("flightmode.yawMode", YAW_MODE)
        scf.cf.param.set_value("flightmode.stabModeRoll", STAB_MODE_ROLL)
        scf.cf.param.set_value("flightmode.stabModePitch", STAB_MODE_PITCH)
        scf.cf.param.set_value("flightmode.stabModeYaw", STAB_MODE_YAW)

        time.sleep(1)

        print("Sending arming request")
        
        scf.cf.platform.send_arming_request(True)
        
        time.sleep(1)

        print("Starting control")
        
        while not keyboard.is_pressed('q'):
            scf.cf.commander.send_setpoint(0, 0, 0, thrust)
            print(f"Thrust is {thrust}, isconnected: {scf.cf.is_connected()}")
            time.sleep(0.02)

            
    keyboard.unhook_all()

    print("Successfully Disconnected")