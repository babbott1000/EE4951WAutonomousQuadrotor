import time
import cflib.crtp
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.crazyflie import Crazyflie
from cflib.utils import uri_helper

URI = uri_helper.uri_from_env(default='radio://0/80/2M/E7E7E7E7E7')

if __name__ == '__main__':
    cflib.crtp.init_drivers()
    
    print("Connecting...")

    with SyncCrazyflie(URI, cf=Crazyflie(rw_cache='./cache')) as scf:
        
        print("Waiting for parameters...")
        scf.wait_for_params()

        print("========= PARAMETERS =========")
        print(f"motorPowerSet.enable: {scf.cf.param.get_value("motorPowerSet.enable")}")
        print(f"motorPowerSet.m1: {scf.cf.param.get_value("motorPowerSet.m1")}")
        print(f"motorPowerSet.m2: {scf.cf.param.get_value("motorPowerSet.m2")}")
        print(f"motorPowerSet.m3: {scf.cf.param.get_value("motorPowerSet.m3")}")
        print(f"motorPowerSet.m4: {scf.cf.param.get_value("motorPowerSet.m4")}")

        print("Sending reset command...")
        scf.cf.commander.send_setpoint(0, 0, 0, 0)
        time.sleep(0.5)

        print("Sending minimal command...")
        scf.cf.commander.send_setpoint(0, 0, 0, 10000)
        time.sleep(2.5)
        
        print("Sending stop command...")
        scf.cf.commander.send_stop_setpoint()
        time.sleep(0.5)
        
        print("Disconnecting...")
        scf.close_link()
        time.sleep(1.0)