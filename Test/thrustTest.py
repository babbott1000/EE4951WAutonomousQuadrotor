import time
import logging
import cflib.crtp
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.log import LogConfig
from cflib.crazyflie.syncLogger import SyncLogger
from cflib.utils import uri_helper

URI = uri_helper.uri_from_env(default='radio://0/80/2M/E7E7E7E7E7')

def callback(msg):
    print(f"CRAZYFLIE: {msg}", end="")

def log():
    scf.cf.param.set_value('supervisor.infdmp', 1)

if __name__ == '__main__':
    print("Initializing drivers")

    cflib.crtp.init_drivers()
    
    print("Connecting...")
    
    with SyncCrazyflie(URI, cf=Crazyflie(rw_cache='./cache')) as scf:

        scf.cf.console.receivedChar.add_callback(callback)
        
        print("Waiting for parameters...")
        scf.wait_for_params()

        print("Sending reset command...")
        scf.cf.commander.send_setpoint(0, 0, 0, 0)
        time.sleep(1.5)

        log()

        print("Sending minimal command...")

        for i in range(60):
            scf.cf.commander.send_setpoint(0, 0, 0, 30000)
            time.sleep(0.25)

            log()
        
        print("Sending stop command...")
        
        for i in range(15):
            scf.cf.commander.send_setpoint(0, 0, 0, 0)
            time.sleep(0.25)

            log()
        
        print("Disconnecting...")
        scf.close_link()
        time.sleep(1.0)