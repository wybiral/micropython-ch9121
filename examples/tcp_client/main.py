import uasyncio as asyncio
import ch9121
from machine import Pin, UART
import time

GATEWAY = (192, 168, 1, 254)
TARGET_IP = (192, 168, 1, 69)
TARGET_PORT = 8080

cfg = Pin(19, Pin.OUT)
uart = UART(2, 9600)
eth = ch9121.CH9121(uart, cfg)

async def main(eth):
    await asyncio.sleep(1)
    await eth.set_mode(ch9121.TCP_CLIENT)
    await eth.set_gateway(GATEWAY)
    await eth.set_target_ip(TARGET_IP)
    await eth.set_target_port(TARGET_PORT)
    await asyncio.sleep(1)
    while True:
        line = await eth.readline()
        print(line)
        await eth.write(line)

loop = asyncio.get_event_loop()
loop.create_task(main(eth))
loop.run_forever()
