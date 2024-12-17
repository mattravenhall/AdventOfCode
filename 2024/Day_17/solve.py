#!/usr/bin/env python3.11

import logging
import re
from typing import Optional

re_register = r"Register (A|B|C): (\d+)"

logger = logging.getLogger()
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')


class Handheld:
    def __init__(self, input_file: str, ):
        self.initial_registers, self.program = self._parse_input(input_file)

    def _parse_input(self, input_file: str) -> tuple[dict, list]:
        registers = {}
        for line in open(input_file).readlines():
            if line.startswith("Register"):
                register, value = re.match(re_register, line).groups()
                registers[register] = int(value)
            elif line.startswith("Program:"):
                program = line.strip().split()[1].split(',')
        return registers, program

    def run_program(self, registers: Optional[dict] = None, expected: Optional[list] = None) -> int:
        if registers is None:
            registers = self.initial_registers
        ipointer: int = 0
        output = []

        logger.debug(f"{self.program=}")
        logger.debug(f"{registers=}")

        while 0 <= ipointer <= (len(self.program)-2):
            opcode = int(self.program[ipointer])
            operand = int(self.program[ipointer+1])
            ijump: int = 2

            logger.debug(f"Processing {opcode=} with {operand=} [{ipointer=}]")

            # Combo operands
            combo = {
                0: 0,
                1: 1,
                2: 2,
                3: 3,
                4: registers["A"],
                5: registers["B"],
                6: registers["C"],
                7: None,
            }

            # Perform opcode
            match opcode:
                case 0:
                    # adv
                    logger.debug(f"Performing adv (A = A >> {combo[operand]})")
                    registers["A"] = registers["A"] >> combo[operand]
                case 1:
                    # bxl
                    logger.debug(f"Performing bxl (B ^= {operand})")
                    registers["B"] ^= operand
                case 2:
                    # bst
                    logger.debug(f"Performing bst (B = {combo[operand]} % 8)")
                    registers["B"] = combo[operand] % 8
                case 3:
                    # jnz
                    logger.debug("Performing jnz (loop if A != 0)")
                    if registers["A"] == 0:
                        pass
                    else:
                        ipointer = operand
                        ijump = 0
                case 4:
                    # bxc
                    logger.debug(f"Performing bxc (B ^= C)")
                    registers["B"] ^= registers["C"]
                case 5:
                    # out
                    logger.debug(f"Performing out ({combo[operand]} % 8 to output)")
                    output_raw = combo[operand] % 8
                    output.extend(list(str(output_raw)))
                case 6:
                    # bdv
                    logger.debug(f"Performing bdv (B = A >> {combo[operand]})")
                    registers["B"] = registers["A"] >> combo[operand]
                case 7:
                    # cdv
                    logger.debug(f"Performing cdv (C = A >> {combo[operand]})")
                    registers["C"] = registers["A"] >> combo[operand]
            
            if ijump > 0:
                ipointer += ijump
            
            logger.debug(f"Updated State: {registers=} {output=}")
            logger.debug(f"A: {bin(registers['A'])}")
            logger.debug(f"B: {bin(registers['B'])}")
            logger.debug(f"C: {bin(registers['C'])}")
        
        logger.debug(f"{output=}")
        return ','.join(map(str, output)), registers

    def find_lowest_a(self, candidate: int = 0) -> int:
        # Staring at the pattern of the iterations, it looks like we can step up matches in reverse?
        logger.debug(f"{candidate=}")
        for i in range(8):  # The pattern increments in blocks of 8
            logger.debug(f"Testing {i=}")
            scout = candidate * 8 + i
            output = self.run_program({'A': scout, 'B': 0, 'C': 0}, expected=self.program)[0].split(',')

            logger.debug(f"{output=}")

            # Solved
            if output == self.program:
                return scout

            # Matching ends make the candidate valid
            if (self.program[-len(output):] == output):
                logger.debug("Looks good")
                # Keep going if we're partly there
                result = self.find_lowest_a(candidate=scout)
                if result is not None:
                    return result
            
        return None

assert Handheld("./test.txt").run_program()[0] == "4,6,3,5,6,3,5,2,1,0"
assert Handheld("./test2.txt").run_program()[1]["B"] == 1
assert Handheld("./test3.txt").run_program()[0] == "0,1,2"
test4_program, test4_registers = Handheld("./test4.txt").run_program()
assert test4_program == "4,2,5,6,7,7,7,7,3,1,0"
assert test4_registers["A"] == 0
assert Handheld("./test5.txt").run_program()[1]["B"] == 26
assert Handheld("./test6.txt").run_program()[1]["B"] == 44354
assert Handheld("./test7.txt").run_program()[0] == "0,3,5,4,3,0"

solver = Handheld("./input.txt")
print(f"A: {solver.run_program()[0]}")  # 7,3,5,7,5,7,4,3,0
print(f"B: {solver.find_lowest_a()}")  # 105734774294938
