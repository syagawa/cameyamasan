# https://tutorialedge.net/python/concurrency/asyncio-event-loops-tutorial/
# sudo apt install bridge-utils bluez python-dbus python-gobject
# sudo service bluetooth restart
import os, sys, signal
import asyncio
from datetime import datetime
from typing import Callable, Any

from aioconsole import ainput
from bleak import BleakClient, discover

from variables import ssid, ps, camera_device_name, camera_shot_times, camera_shot_interval
import json
import camera

from interface.key import start_standby
from interface.screen import make_screen

from logger import log

com_start_server = '{"action":"start_server", "ssid": "%s", "pswd":"%s"}' % (ssid, ps)
device_name = camera_device_name

received_data = ""
server_is_started = False
server_ip = ""
shot_started = False
shot_times = camera_shot_times
shot_interval = camera_shot_interval
framesize_value = None

screen = None

action_callback_global = None

def set_action_callback(action_callback=None):
  global action_callback_global
  action_callback_global = action_callback

def do_action_callback(message):
    if action_callback_global != None:
        action_callback_global(message)


class Connection:
    
    client: BleakClient = None
    
    def __init__(
        self,
        loop: asyncio.AbstractEventLoop,
        read_characteristic: str,
        write_characteristic: str,
        data_dump_size: int = 256,
    ):
        log("in __init__ Connection")
        self.loop = loop
        self.read_characteristic = read_characteristic
        self.write_characteristic = write_characteristic

        self.last_packet_time = datetime.now()
        self.dump_size = data_dump_size
        self.connected = False
        self.connected_device = None

        self.rx_data = []
        self.rx_timestamps = []
        self.rx_delays = []

    def on_disconnect(self, client: BleakClient):
        log("in on_disconnect")
        self.connected = False
        # Put code here to handle what happens on disconnet.
        log(f"Disconnected from {self.connected_device.name}!")

    async def cleanup(self):
        log("in cleanup")
        if self.client:
            await self.client.stop_notify(read_characteristic)
            await self.client.disconnect()
            log("disconnected")

    async def manager(self):
        log("Starting connection manager.")
        do_action_callback("Starting connection manager.")

        while True:
            if self.client:
                await self.connect()
                break
            else:
                await self.select_device()
                await asyncio.sleep(10.0)

    async def connect(self):
        log("in connect")
        do_action_callback("in connect")

        if self.connected:
            return
        try:
            await self.client.connect()
            self.connected = self.client.is_connected()
            if self.connected:
                log(F"Connected to {self.connected_device.name}")
                self.client.set_disconnected_callback(self.on_disconnect)
                await self.client.start_notify(
                    self.read_characteristic, self.notification_handler,
                )
                # while True:
                #     if not self.connected:
                #         break
                #     await asyncio.sleep(1.0)
            else:
                log(f"Failed to connect to {self.connected_device.name}")
        except Exception as e:
            log(e)

    async def _select_device(self):
        log("Bluetooh LE hardware warming up 0")
        await asyncio.sleep(2.0) # Wait for BLE to initialize.
        log("Bluetooh LE hardware warming up 1")
        devices = None
        try:
            log("discovering...")
            devices = await discover()
        except Exception as e:
            log(e)
            return

        log("Please select device: ")
        target_index = -1
        for i, device in enumerate(devices):
            log(f"{i}: {device.name}")
            if device.name == device_name:
                target_index = i

        response = -1

        if target_index == -1:
            while True:
                response = await ainput("Select device: ")
                try:
                    response = int(response.strip())
                except:
                    log("Please make valid selection.")
                
                if response > -1 and response < len(devices):
                    break
                else:
                    log("Please make valid selection.")
        else:
            response = target_index

        log(f"Connecting to {devices[response].name}")
        try:
            self.connected_device = devices[response]
            self.client = BleakClient(devices[response].address, loop=self.loop)
        except:
            log("failed connecting device")
            

    async def select_device(self):
        log("Bluetooh LE hardware warming up 0")
        await asyncio.sleep(2.0) # Wait for BLE to initialize.
        log("Bluetooh LE hardware warming up 1")
        devices = None
        try:
            log("discovering...")
            devices = await discover()
        except Exception as e:
            log(e)
            return

        log("Please select device: ")
        response = -1
        target_index = -1
        for i, device in enumerate(devices):
            log(f"{i}: {device.name}")
            if device.name == device_name:
                target_index = i
                response = target_index



        if response == -1:
            return

        log(f"Connecting to {devices[response].name}")
        try:
            self.connected_device = devices[response]
            self.client = BleakClient(devices[response].address, loop=self.loop)
        except:
            log("failed connecting device")



    def record_time_info(self):
        log("in record_time_info")
        present_time = datetime.now()
        self.rx_timestamps.append(present_time)
        self.rx_delays.append((present_time - self.last_packet_time).microseconds)
        self.last_packet_time = present_time

    def clear_lists(self):
        log("in clear_lists")
        self.rx_data.clear()
        self.rx_delays.clear()
        self.rx_timestamps.clear()

    def notification_handler(self, sender: str, data: Any):
        log("in norific...handler")
        self.rx_data.append(int.from_bytes(data, byteorder="big"))
        self.record_time_info()
        global server_is_started
        global server_ip

        log(f"Received From ESP 32 Camera: {data}")
        received_data = data
        if hasattr(received_data, "decode"):
            str = received_data.decode()
            log(f"str {str}")
            j = json.loads(received_data)
            if("ip" in j):
                log(f"exitsts! IP: {j['ip']}")

                server_is_started = True
                server_ip = j["ip"]
        if len(self.rx_data) >= self.dump_size:
            self.clear_lists()


def finally_process():
    log("in finally_process")
    # loop.run_until_complete(connection.cleanup())
    signal.signal(signal.SIGTERM, signal.SIG_IGN)
    signal.signal(signal.SIGINT, signal.SIG_IGN)
    #cleanup()
    signal.signal(signal.SIGTERM, signal.SIG_DFL)
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    sys.exit(1)

def sig_handler(signum, frame) -> None:
    log("in sig_handler")
    finally_process()

def pressed_action(pressed_pin, state):
    log(f"pressed!! {pressed_pin}: {state}")


#############
# Loops
#############
async def send_wifi_info(connection: Connection):
    log("in send_wifi_info")
    do_action_callback("in send_wifi_info")
    loopable = True
    while loopable:
        do_action_callback("in while loopable")
        if connection.client and connection.connected:
            bytes_to_send = bytearray(map(ord, com_start_server))
            await connection.client.write_gatt_char(write_characteristic, bytes_to_send)
            log(f"Sent: Wi-Fi info")
            loopable = False
        else:
            await asyncio.sleep(1.0)

async def set_camera_shot_settings():
    log("in set_camera_shot_settings")
    framesizes = camera.framesizes
    while True:
        if server_is_started:
            log("Please select framesize by number: ")
            for i, elm in enumerate(framesizes):
                elm = framesizes[i]
                key = elm["key"]
                log(f"{i}: {key}")
            break
        else:
            await asyncio.sleep(5.0)

    global framesize_value
    while True:
        response = await ainput("Select framesize number: ")
        try:
            response = int(response.strip())
            tgt = framesizes[response]
            framesize_value = tgt["value"]
            log("framesize_value", framesize_value)
        except:
            log("Unknown Number. The default value will be selected.")
        
        break



async def start_shots():
    flg = True
    while flg:
        # YOUR APP CODE WOULD GO HERE.
        if server_is_started:
            log(f"server is started ! ip: {server_ip}")
            try:
                global shot_started
                if shot_started == False:
                    shot_started = True
                    log("shot started!")
                    res = False
                    try:
                        res = camera.shots(shot_times, shot_interval, server_ip, framesize_value)
                    except Exception as e:
                        log("catch Exception", e)
                    log("shot ended!")
                    if res == True:
                        connection.cleanup()


            except KeyboardInterrupt:
                log("except KeyboardInterrupt in start_camera()")
            finally:
                log("finally in start_camera()")
                # sys.exit(1)
                flg = False
                raise Exception("End process")
        await asyncio.sleep(5)


async def start_camera():
    log("in start_camera")
    await set_camera_shot_settings()
    await start_shots()




#############
# App Main
#############
read_characteristic = "00001143-0000-1000-8000-00805f9b34fb"
write_characteristic = "00001142-0000-1000-8000-00805f9b34fb"


def connect(action_callback=None):
    log("connect0 in controller.py")
    log("connect000 in controller.py")
    if action_callback != None:
        action_callback("0 connect in cpy")
        log("0 connect in cpy")
        set_action_callback(action_callback)

    log("connect001 in controller.py")

    do_action_callback("1 connect in cpy")
    log("connect0011 in controller.py")

    loop = asyncio.get_event_loop()
    # new_loop = asyncio.new_event_loop()
    # loop = asyncio.set_event_loop(new_loop)
    log("connect002 in controller.py")
    connection = Connection(
        loop, read_characteristic, write_characteristic
    )
    log("connect1 in controller.py")

    try:
        do_action_callback("2 connect in cpy")
        log("2 connect in cpy")
        signal.signal(signal.SIGTERM, sig_handler)
        do_action_callback("3 connect in cpy")
        asyncio.ensure_future(connection.manager())
        do_action_callback("4 connect in cpy")
        asyncio.ensure_future(send_wifi_info(connection))
        do_action_callback("5 connect in cpy")
        log("5 connect in cpy")
        loop.run_forever()
        do_action_callback("6 connect in cpy")
        log("6 connect in cpy")
    except KeyboardInterrupt:
        log()
        log("in except KeyboardInterrupt: User stopped program.")
    finally:
        log("in finally Disconnecting...")
        finally_process()

async def connect2(action_callback=None):
    log("connect2 in controller.py")

    if action_callback != None:
        action_callback("0 connect2 in cpy")
        set_action_callback(action_callback)

    do_action_callback("1 connect2 in cpy")

    new_loop = asyncio.new_event_loop()
    loop = asyncio.set_event_loop(new_loop)
    # loop = asyncio.get_event_loop()

    # new_loop = asyncio.new_event_loop()
    connection = Connection(
        loop, read_characteristic, write_characteristic
    )
    do_action_callback("2 connect2 in cpy")
    # signal.signal(signal.SIGTERM, sig_handler)
    do_action_callback("3 connect2 in cpy")
    # asyncio.ensure_future(connection.manager())
    await connection.manager()
    do_action_callback("4 connect2 in cpy")
    asyncio.ensure_future(send_wifi_info(connection))
    do_action_callback("5 connect2 in cpy")
    # loop.run_forever()
    do_action_callback("6 connect2 in cpy")




def connect_and_shot():
    # Create the event loop.
    loop = asyncio.get_event_loop()
    # new_loop = asyncio.new_event_loop()
    # loop = asyncio.set_event_loop(new_loop)

    connection = Connection(
        loop, read_characteristic, write_characteristic
    )
    log("Start Controller!!!")
    try:
        signal.signal(signal.SIGTERM, sig_handler)
        asyncio.ensure_future(connection.manager())
        asyncio.ensure_future(send_wifi_info(connection))
        asyncio.ensure_future(start_camera())
        # asyncio.ensure_future(start_standby(None, pressed_action))
        loop.run_forever()
    except KeyboardInterrupt:
        log()
        log("in except KeyboardInterrupt: User stopped program.")
    finally:
        log("in finally Disconnecting...")
        finally_process()

if __name__ == "__main__":
    connect_and_shot()