import uasyncio as asyncio

TCP_CLIENT = 0
TCP_SERVER = 1
UDP_CLIENT = 2
UDP_SERVER = 3

class CH9121:

    def __init__(self, uart, cfg):
        self.uart = uart
        self.cfg = cfg
        self.w = asyncio.StreamWriter(uart, {})
        self.r = asyncio.StreamReader(uart)

    async def _config(self, cmd, n=1):
        self.cfg.value(0)
        await self.w.awrite(b'\x57\xab' + cmd)
        resp = b''
        while len(resp) < n:
            await asyncio.sleep(0.1)
            resp = await self.r.read(n)
        self.cfg.value(1)
        return resp

    async def get_mode(self):
        mode = await self._config(b'\x60')
        return ord(mode)

    async def get_local_ip(self):
        x = await self._config('\x61', 4)
        return (x[0], x[1], x[2], x[3])

    async def get_subnet_mask(self):
        x = await self._config('\x62', 4)
        return (x[0], x[1], x[2], x[3])

    async def get_gateway(self):
        x = await self._config('\x63', 4)
        return (x[0], x[1], x[2], x[3])

    async def get_local_port(self):
        x = await self._config('\x64', 2)
        return int.from_bytes(x, 'little')

    async def get_target_ip(self):
        x = await self._config('\x65', 4)
        return (x[0], x[1], x[2], x[3])

    async def get_target_port(self):
        x = await self._config('\x66', 2)
        return int.from_bytes(x, 'little')

    async def set_mode(self, mode):
        x = await self._config(b'\x10' + mode.to_bytes(1, 'little'))
        return x

    async def set_baud_rate(self, baud):
        x = await self._config(b'\x21' + baud.to_bytes(4, 'little'))
        return x

    async def set_local_ip(self, ip):
        x = await self._config(b'\x11' + bytes(bytearray(ip)))
        return x

    async def set_gateway(self, ip):
        x = await self._config(b'\x13' + bytes(bytearray(ip)))
        return x

    async def set_local_port(self, x):
        x = await self._config(b'\x14' + x.to_bytes(2, 'little'))
        return x

    async def set_target_ip(self, ip):
        x = await self._config(b'\x15' + bytes(bytearray(ip)))
        return x

    async def set_target_port(self, x):
        x = await self._config(b'\x16' + x.to_bytes(2, 'little'))
        return x

    async def write(self, x):
        return await self.w.awrite(x)

    async def read(self, n):
        return await self.r.read(n)

    async def readline(self):
        return await self.r.readline()

    async def reset(self):
        await self.w.awrite(b'\x57\xab\x02')
