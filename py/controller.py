# https://tutorialedge.net/python/concurrency/asyncio-event-loops-tutorial/
# sudo apt install bridge-utils bluez python-dbus python-gobject
# sudo service bluetooth restart
import os, sys
import asyncio
from datetime import datetime
from typing import Callable, Any

from aioconsole import ainput
from bleak import BleakClient, discover

from variables import ssid, ps
import json
import camera


com_start_server = '{"action":"start_server", "ssid": "%s", "pswd":"%s"}' % (ssid, ps)

device_name = "timerx"

received_data = ""
server_is_started = False
server_ip = ""
shot_started = False
shot_times = 100
shot_interval = 5


class Connection:
    
    client: BleakClient = None
    
    def __init__(
        self,
        loop: asyncio.AbstractEventLoop,
        read_characteristic: str,
        write_characteristic: str,
        data_dump_size: int = 256,
    ):
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

    def on_disconnect(self, client: BleakClient, future: asyncio.Future):
        self.connected = False
        # Put code here to handle what happens on disconnet.
        print(f"Disconnected from {self.connected_device.name}!")

    async def cleanup(self):
        if self.client:
            await self.client.stop_notify(read_characteristic)
            await self.client.disconnect()

    async def manager(self):
        print("Starting connection manager.")
        while True:
            if self.client:
                await self.connect()
            else:
                await self.select_device()
                await asyncio.sleep(10.0)

    async def connect(self):
        if self.connected:
            return
        try:
            await self.client.connect()
            self.connected = await self.client.is_connected()
            if self.connected:
                print(F"Connected to {self.connected_device.name}")
                self.client.set_disconnected_callback(self.on_disconnect)
                await self.client.start_notify(
                    self.read_characteristic, self.notification_handler,
                )
                while True:
                    if not self.connected:
                        break
                    await asyncio.sleep(1.0)
            else:
                print(f"Failed to connect to {self.connected_device.name}")
        except Exception as e:
            print(e)

    async def select_device(self):
        print("Bluetooh LE hardware warming up...")
        await asyncio.sleep(2.0) # Wait for BLE to initialize.
        devices = await discover()

        print("Please select device: ")
        target_index = -1
        for i, device in enumerate(devices):
            print(f"{i}: {device.name}")
            if device.name == device_name:
                target_index = i

        response = -1

        if target_index == -1:
            while True:
                response = await ainput("Select device: ")
                try:
                    response = int(response.strip())
                except:
                    print("Please make valid selection.")
                
                if response > -1 and response < len(devices):
                    break
                else:
                    print("Please make valid selection.")
        else:
            response = target_index

        print(f"Connecting to {devices[response].name}")
        self.connected_device = devices[response]
        self.client = BleakClient(devices[response].address, loop=self.loop)

    def record_time_info(self):
        present_time = datetime.now()
        self.rx_timestamps.append(present_time)
        self.rx_delays.append((present_time - self.last_packet_time).microseconds)
        self.last_packet_time = present_time

    def clear_lists(self):
        self.rx_data.clear()
        self.rx_delays.clear()
        self.rx_timestamps.clear()

    def notification_handler(self, sender: str, data: Any):
        self.rx_data.append(int.from_bytes(data, byteorder="big"))
        self.record_time_info()
        global server_is_started
        global server_ip

        print(f"Received From ESP 32 : {data}")
        received_data = data
        if hasattr(received_data, "decode"):
            str = received_data.decode()
            print(f"str {str}")
            j = json.loads(received_data)
            if("ip" in j):
                print(f"exitsts! IP: {j['ip']}")

                server_is_started = True
                server_ip = j["ip"]
        if len(self.rx_data) >= self.dump_size:
            self.clear_lists()


def startShots(ip):
    global shot_started
    if shot_started == False:
        shot_started = True
        res = camera.shots(shot_times, shot_interval, ip)
        if res == True:
            connection.cleanup()


#############
# Loops
#############
async def send_wifi_info(connection: Connection):
    loopable = True
    while loopable:
        if connection.client and connection.connected:
            bytes_to_send = bytearray(map(ord, com_start_server))
            await connection.client.write_gatt_char(write_characteristic, bytes_to_send)
            print(f"Sent: Wi-Fi info")
            loopable = False
        else:
            await asyncio.sleep(1.0)

async def receive_server_info():
    loopable = True
    while loopable:
        print(2)
        pattern = '^[0-9].*\.[0-9].*\.[0-9].*\.[0-9]'
        str = ""
        is_ip = False
        print("received_data")
        print(received_data)
        if hasattr(received_data, "decode"):
            str = received_data.decode()
            if hasattr(str, "match"):
               is_ip = str.match(pattern, received_data)
        if is_ip:
            print(f"IP: {received_data}")
            loopable = False
        else:
            print(3)
            await asyncio.sleep(2.0, loop=loop)

async def main():
    while True:
        # YOUR APP CODE WOULD GO HERE.
        if server_is_started:
            print(f"server is started ! ip: {server_ip}")
            startShots(server_ip)

        await asyncio.sleep(5)



#############
# App Main
#############
read_characteristic = "00001143-0000-1000-8000-00805f9b34fb"
write_characteristic = "00001142-0000-1000-8000-00805f9b34fb"

if __name__ == "__main__":

    # Create the event loop.
    loop = asyncio.get_event_loop()

    connection = Connection(
        loop, read_characteristic, write_characteristic
    )
    try:
        asyncio.ensure_future(connection.manager())
        asyncio.ensure_future(send_wifi_info(connection))
        asyncio.ensure_future(main())
        loop.run_forever()
    except KeyboardInterrupt:
        print()
        print("User stopped program.")
    finally:
        print("Disconnecting...")
        loop.run_until_complete(connection.cleanup())