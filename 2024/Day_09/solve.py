#!/usr/bin/env python3.11

from copy import deepcopy

solution_a = 0
solution_b = 0


class Parser:
    def __init__(self, input_file: str):
        raw_input = open(input_file).readlines()[0].strip()
        self.disk, self.indexes = self._parse_disk_string(raw_input)

    def _parse_disk_string(self, disk_string: str) -> tuple[str, dict]:
        disk: list = []
        indexes: dict = {
            "void": [],
            "file": [],
            "file_blocks": [], # start: length
            "void_blocks": {}, # start: length
        }
        file_id = 0
        str_len = 0
        for i, size in enumerate(disk_string):
            if i % 2:
                block_type = '.'
                indexes["void"].extend([i for i in range(len(disk), len(disk) + int(size))])
                indexes["void_blocks"][int(str_len)] = int(size)
            else:
                block_type = str(file_id)
                file_id += 1
                indexes["file"].extend([i for i in range(len(disk), len(disk) + int(size))])
                indexes["file_blocks"].append([int(str_len), int(size)])
            str_len += int(size)

            disk.extend([block_type] * int(size))

        # Order file_blocks in reverse
        indexes["file_blocks"] = indexes["file_blocks"][::-1]

        return disk, indexes
    
    def _sort_disk_a(self) -> str:
        disk_copy = deepcopy(self.disk)
        while int(self.indexes["void"][0]) < int(self.indexes["file"][-1]):
            void_index = int(self.indexes["void"].pop(0))
            file_index = int(self.indexes["file"].pop(-1))
            assert disk_copy[void_index] == '.'
            disk_copy[void_index] = disk_copy[file_index]
            assert disk_copy[file_index] != '.'
            disk_copy[file_index] = '.'
        return disk_copy

    def _sort_disk_b(self) -> str:
        disk_copy = deepcopy(self.disk)

        # For each file block
        for file_index, file_size in self.indexes["file_blocks"]:
            # print(f"Considering file ID {disk_copy[file_index]} at {file_index} (size: {file_size})")

            # Find a valid void block
            void_blocks_sorted = sorted(self.indexes["void_blocks"].keys())
            for void_key in void_blocks_sorted:
                # Abort when our void is beyond our file
                if void_key >= file_index:
                    break

                # Parse our candidate void block
                void_size = self.indexes["void_blocks"][void_key]
                # print(f"Considering void at {void_key} (size: {void_size})")

                # Check if file will fit in this void
                if file_size <= void_size:
                    # print(f"Found a void: {void_key} (size: {void_size})")

                    # If it can, update disk_copy
                    for file_size_i in range(file_size):
                        assert disk_copy[void_key+file_size_i] == '.'
                        disk_copy[void_key+file_size_i] = disk_copy[file_index+file_size_i]
                        assert disk_copy[file_index+file_size_i] != '.'
                        disk_copy[file_index+file_size_i] = '.'
                    
                    # Upload void block now that a file occupies it
                    del self.indexes["void_blocks"][void_key]
                    if void_size - file_size:
                        # If void remains, update void size
                        self.indexes["void_blocks"][void_key+file_size] = void_size-file_size
                        # print(f">>>>>>>> UPDATED VOIDS: {self.indexes['void_blocks']}")
                    break
                else:
                    # print(f"Void not large enough: {void_key} (size: {void_size})")
                    continue

        # print(disk_copy)
        return disk_copy

    
    def calculate_checksum(self, sort_type: str) -> int:
        match sort_type:
            case 'A':
                disk = self._sort_disk_a()
            case 'B':
                disk = self._sort_disk_b()
            case _:
                raise ValueError(f"Invalid sort type {sort_type}")

        total = 0
        for i, id in enumerate(disk):
            if id != '.':
                total += (i * int(id))
        return total


test_parser = Parser("./test.txt")
assert test_parser.calculate_checksum('A') == 1928
assert test_parser.calculate_checksum('B') == 2858

assert Parser("./test2.txt").calculate_checksum('B') == 132

parser = Parser("./input.txt")
print(f"A: {parser.calculate_checksum('A')}")
print(f"B: {parser.calculate_checksum('B')}")
