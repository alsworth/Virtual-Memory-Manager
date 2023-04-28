# Virtual Memory Simulator

This project is a virtual memory simulator that translates logical addresses to physical addresses using a TLB and a page table. The program reads a file containing logical addresses, translates them to corresponding physical addresses, and outputs the value of the signed byte stored at the translated physical address. This project helps users understand the steps involved in translating logical to physical addresses, including resolving page faults using demand paging, managing a TLB, and implementing a page-replacement algorithm.

## Getting Started

These instructions will help you set up and run the project on your local machine.

### Prerequisites

- Python (version 3.x is recommended)

### Installation

1. Clone the repository or download the source code.
2. Open a terminal or command prompt and navigate to the project directory.

### Usage

1. Run `python create_backing_store.py` to generate the `BACKING_STORE.bin` file.
2. Run `python create_addresses_file.py` to generate the `addresses.txt` file with 1,000 random logical addresses.
3. Run `python virtual_memory_simulator.py addresses.txt` to execute the virtual memory simulator using the generated `addresses.txt` file.

The virtual memory simulator will display the output showing the logical addresses, their corresponding physical addresses, and the signed byte values stored in the physical memory at the translated physical addresses.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
