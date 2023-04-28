import sys
import os
from struct import unpack

PAGE_SIZE = 256
TLB_SIZE = 16
NUM_FRAMES = 256
NUM_PAGES = 256
ADDRESS_MASK = 0xFFFF
OFFSET_MASK = 0xFF

class TLB:
    def __init__(self):
        self.entries = []

    def update(self, page_number, frame_number):
        if len(self.entries) >= TLB_SIZE:
            self.entries.pop(0)
        self.entries.append((page_number, frame_number))

    def lookup(self, page_number):
        for entry in self.entries:
            if entry[0] == page_number:
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

def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} addresses.txt")
        sys.exit(1)

    addresses_file = sys.argv[1]

    page_table = PageTable()
    tlb = TLB()
    physical_memory = bytearray(NUM_FRAMES * PAGE_SIZE)

    with open("BACKING_STORE.bin", "rb") as backing_store, open(addresses_file, "r") as f:
        for line in f:
            logical_address = int(line.strip())
            page_number = (logical_address & ADDRESS_MASK) >> 8
            offset = logical_address & OFFSET_MASK

            frame_number = tlb.lookup(page_number)

            if frame_number is None:
                frame_number = page_table[page_number]

                if frame_number is None:
                    frame_number = len(page_table.entries) - page_table.entries.count(None) - 1
                    page_table[page_number] = frame_number

                    # Read the page from the backing store and store it in the physical memory
                    page_data = read_page_from_backing_store(page_number, backing_store)
                    physical_memory[frame_number * PAGE_SIZE:(frame_number + 1) * PAGE_SIZE] = page_data

                tlb.update(page_number, frame_number)

            physical_address = (frame_number << 8) | offset
            signed_byte_value = unpack("b", physical_memory[physical_address:physical_address + 1])[0]

            print(f"Logical address: {logical_address} -> Physical address: {physical_address} -> Signed byte value: {signed_byte_value}")

if __name__ == "__main__":
    main()
