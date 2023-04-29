import sys
import os
from struct import unpack
import random

PAGE_SIZE = 256
TLB_SIZE = 16
NUM_FRAMES = 256
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

    total_addresses = 0  # total number of addresses processed
    page_faults = 0  # number of page faults

    with open(backing_store_file, "rb") as backing_store, open(addresses_file, "r") as f:
        for line in f:
            total_addresses += 1  # increment total addresses
            logical_address = int(line.strip())
            page_number = (logical_address & ADDRESS_MASK) >> 8
            offset = logical_address & OFFSET_MASK

            frame_number = tlb.lookup(page_number)

            if frame_number is None:
                frame_number = page_table[page_number]

                if frame_number is None:
                    page_faults += 1  # increment page faults
                    frame_number = len(page_table.entries) - page_table.entries.count(None)
                    page_table[page_number] = frame_number

                    # Read the page from the backing store and store it in the physical memory
                    page_data = read_page_from_backing_store(page_number, backing_store)
                    physical_memory[frame_number * PAGE_SIZE:(frame_number + 1) * PAGE_SIZE] = page_data
                tlb.update(page_number, frame_number)

            physical_address = (frame_number << 8) | offset
            signed_byte_value = unpack("b", physical_memory[physical_address:physical_address + 1])[0]

            print(f"Logical address: {logical_address} -> Physical address: {physical_address} -> Signed byte value: {signed_byte_value}")

    # Calculate and print statistics
    page_fault_rate = (page_faults / total_addresses) * 100
    tlb_hit_rate = (tlb.hits / total_addresses) * 100

    print(f"Page fault rate: {page_fault_rate}%")
    print(f"TLB hit rate: {tlb_hit_rate}%")

if __name__ == "__main__":
    main()