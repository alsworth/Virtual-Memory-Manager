import sys
import os
from struct import unpack
import random

PAGE_SIZE = 256
TLB_SIZE = 16
NUM_FRAMES = 128  # changed from 256 to 128
NUM_PAGES = 256
ADDRESS_MASK = 0xFFFF
OFFSET_MASK = 0xFF
NUM_ADDRESSES = 1000
ADDRESS_RANGE = 65536  # 2^16
BACKING_STORE_SIZE = 65536  # 2^16

class TLB:
    def __init__(self):
        self.entries = []
        self.hits = 0  # TLB hits

    def update(self, page_number, frame_number):
        if len(self.entries) >= TLB_SIZE:
            self.entries.pop(0)
        self.entries.append((page_number, frame_number))

    def lookup(self, page_number):
        for entry in self.entries:
            if entry[0] == page_number:
                self.hits += 1  # increment TLB hits
                return entry[1]
        return None

class PageTable:
    def __init__(self):
        self.entries = [None] * NUM_PAGES

    def __getitem__(self, index):
        return self.entries[index]

    def __setitem__(self, index, value):
        self.entries[index] = value

class PhysicalMemory:
    def __init__(self):
        self.memory = bytearray(NUM_FRAMES * PAGE_SIZE)
        self.free_frames = list(range(NUM_FRAMES))
        self.lru_list = []

    def __getitem__(self, index):
        return self.memory[index]

    def __setitem__(self, index, value):
        self.memory[index] = value

    def load_page(self, page_number, page_data):
        if self.free_frames:
            frame_number = self.free_frames.pop(0)
        else:
            frame_number = self.lru_list.pop(0)
        self.lru_list.append(frame_number)

        self[frame_number * PAGE_SIZE:(frame_number + 1) * PAGE_SIZE] = page_data
        return frame_number

    def unload_page(self, frame_number):
        self.free_frames.append(frame_number)
        self.lru_list.remove(frame_number)

def read_page_from_backing_store(page_number, backing_store):
    backing_store.seek(page_number * PAGE_SIZE)
    return bytearray(backing_store.read(PAGE_SIZE))

def create_addresses_file(filename):
    with open(filename, "w") as f:
        for _ in range(NUM_ADDRESSES):
            address = random.randint(0, ADDRESS_RANGE - 1)
            f.write(f"{address}\n")

def create_backing_store(filename):
    with open(filename, "wb") as f:
        for _ in range(BACKING_STORE_SIZE):
            f.write(bytes([random.randint(0, 255)]))
def main():
    addresses_file = "addresses.txt"
    backing_store_file = "BACKING_STORE.bin"

    create_addresses_file(addresses_file)
    create_backing_store(backing_store_file)

    page_table = PageTable()
    tlb = TLB()
    physical_memory = bytearray(NUM_FRAMES * PAGE_SIZE)
    free_frames = FreeFrames()

    total_addresses = 0  # total number of addresses processed
    page_faults = 0  # number of page faults