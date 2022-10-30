# https://stackoverflow.com/a/9941024/1360476

import random
import struct

floatlist = [random.random() for _ in range(10**5)]
buf = struct.pack('%sf' % len(floatlist), *floatlist)

print(buf)