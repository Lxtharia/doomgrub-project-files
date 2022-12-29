#import Pillow
from typing import List, Any

data = []




with open("Minecraft.pf2", "rb") as f:
    data = f.read()
    print(data[0:40])
    i: int = 0

    if not data[i:i+4] == b'FILE':
        exit(-1)

    i += 4
    length = int.from_bytes(data[i:i+4], "big")
    print(length)




