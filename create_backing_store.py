import os
import random

BACKING_STORE_SIZE = 65536  # 2^16

def create_backing_store(filename):
    with open(filename, "wb") as f:
        for _ in range(BACKING_STORE_SIZE):
            f.write(bytes([random.randint(0, 255)]))

if __name__ == "__main__":
    create_backing_store("BACKING_STORE.bin")
