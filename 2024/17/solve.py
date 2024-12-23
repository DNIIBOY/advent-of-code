import pyperclip
from time import perf_counter
from enum import IntEnum


class OpCode(IntEnum):
    ADV = 0
    BXL = 1
    BST = 2
    JNZ = 3
    BXC = 4
    OUT = 5
    BDV = 6
    CDV = 7


def display_output(func) -> None:
    with open("input.txt", "r", encoding="utf-8") as f:
        values = f.read().splitlines()

    # values = [
    #     "Register A: 729",
    #     "Register B: 0",
    #     "Register C: 0",
    #     "",
    #     "Program: 0,1,5,4,3,0",
    # ]

    start = perf_counter()
    result = func(values)
    end = perf_counter()
    print(f"--- Got result in {end-start:.2f}s---")
    print(result)
    try:
        pyperclip.copy(result)
        print("--- Copied to clipboard ---")
    except FileNotFoundError:
        pass


class Computer:
    def __init__(self, a: int, b: int, c: int, instructions: list[int]) -> None:
        self.a = a
        self.b = b
        self.c = c
        self.ip = 0
        self.instructions = instructions
        self.output = []

    def run(self) -> None:
        while self.ip < len(self.instructions):
            opcode = OpCode(self.instructions[self.ip])
            arg = self.instructions[self.ip+1]
            self.run_operation(opcode, arg)
            self.ip += 2

    @classmethod
    def from_input(cls, values: list[int]) -> "Computer":
        a = int(values[0].split(": ")[1])
        b = int(values[1].split(": ")[1])
        c = int(values[2].split(": ")[1])
        instructions = list(map(int, values[-1].split(": ")[1].split(",")))
        return cls(a, b, c, instructions)

    def _combo_arg(self, arg: int) -> int:
        if arg < 4:
            return arg
        match arg:
            case 4:
                return self.a
            case 5:
                return self.b
            case 6:
                return self.c
        raise ValueError(f"Invalid argument: {arg}")

    def run_operation(self, opcode: OpCode, arg: int) -> None:
        match opcode:
            case OpCode.ADV:
                self.a = self.a // (2**self._combo_arg(arg))
            case OpCode.BXL:
                self.b = self.b ^ arg
            case OpCode.BST:
                self.b = self._combo_arg(arg) % 8
            case OpCode.JNZ:
                if self.a != 0:
                    self.ip = arg-2
            case OpCode.BXC:
                self.b = self.b ^ self.c
            case OpCode.OUT:
                self.output.append(self._combo_arg(arg) % 8)
            case OpCode.BDV:
                self.b = self.a // (2**self._combo_arg(arg))
            case OpCode.CDV:
                self.c = self.a // (2**self._combo_arg(arg))

    def __repr__(self) -> str:
        return f"Computer(a={self.a}, b={self.b}, c={self.c}, ip={self.ip})"

    def __str__(self) -> str:
        return f"{','.join(map(str, self.output))}"


def main(values: list) -> None:
    computer = Computer.from_input(values)
    computer.run()
    return str(computer)


if __name__ == "__main__":
    display_output(main)
