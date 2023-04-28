import random

NUM_ADDRESSES = 1000
ADDRESS_RANGE = 65536  # 2^16

def create_addresses_file(filename):
    with open(filename, "w") as f:
        for _ in range(NUM_ADDRESSES):
            address = random.randint(0, ADDRESS_RANGE - 1)
            f.write(f"{address}\n")

if __name__ == "__main__":
    create_addresses_file("addresses.txt")
