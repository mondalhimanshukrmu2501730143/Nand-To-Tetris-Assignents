
import os
import re

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

INPUT_FILE = os.path.join(
    BASE_DIR, "..", "Part_C", "Box.asm"
)

OUTPUT_FILE = os.path.join(
    BASE_DIR, "..", "Part_C", "Box.hack"
)

class AssemblerError(Exception):
    def __init__(self, line_number, message):
        self.line_number = line_number
        self.message = message
        super().__init__(message)


def read_assembly_file(filename):
    instructions = []

    with open(filename, "r") as file:
        for line_number, line in enumerate(file, start=1):
            line = line.split("//")[0].strip()

            if line:
                instructions.append((line_number, line))

    return instructions


def valid_symbol(symbol):
    return re.fullmatch(r"[A-Za-z_.$:][A-Za-z0-9_.$:]*", symbol) is not None


COMP_TABLE = {
    "0": "0101010",
    "1": "0111111",
    "-1": "0111010",
    "D": "0001100",
    "A": "0110000",
    "M": "1110000",
    "!D": "0001101",
    "!A": "0110001",
    "!M": "1110001",
    "-D": "0001111",
    "-A": "0110011",
    "-M": "1110011",
    "D+1": "0011111",
    "A+1": "0110111",
    "M+1": "1110111",
    "D-1": "0001110",
    "A-1": "0110010",
    "M-1": "1110010",
    "D+A": "0000010",
    "D+M": "1000010",
    "D-A": "0010011",
    "D-M": "1010011",
    "A-D": "0000111",
    "M-D": "1000111",
    "D&A": "0000000",
    "D&M": "1000000",
    "D|A": "0010101",
    "D|M": "1010101"
}

DEST_TABLE = {
    "": "000",
    "M": "001",
    "D": "010",
    "MD": "011",
    "A": "100",
    "AM": "101",
    "AD": "110",
    "AMD": "111"
}

JUMP_TABLE = {
    "": "000",
    "JGT": "001",
    "JEQ": "010",
    "JGE": "011",
    "JLT": "100",
    "JNE": "101",
    "JLE": "110",
    "JMP": "111"
}


def create_symbol_table():
    symbols = {
        "SP": 0,
        "LCL": 1,
        "ARG": 2,
        "THIS": 3,
        "THAT": 4,
        "SCREEN": 16384,
        "KBD": 24576
    }

    for i in range(16):
        symbols["R" + str(i)] = i

    return symbols


def first_pass(instructions, symbol_table):
    rom_address = 0

    for line_number, instruction in instructions:

        if instruction.startswith("(") or instruction.endswith(")"):

            if not (
                instruction.startswith("(")
                and instruction.endswith(")")
                and instruction.count("(") == 1
                and instruction.count(")") == 1
            ):
                raise AssemblerError(
                    line_number, "Malformed label declaration"
                )

            label = instruction[1:-1]

            if not valid_symbol(label):
                raise AssemblerError(
                    line_number, "Invalid label name"
                )

            if label in symbol_table:
                raise AssemblerError(
                    line_number, "Duplicate label: " + label
                )

            symbol_table[label] = rom_address

        else:
            rom_address += 1

            if rom_address > 32768:
                raise AssemblerError(
                    line_number, "Program exceeds ROM capacity"
                )


def allocate_variables(instructions, symbol_table):
    next_address = 16

    for line_number, instruction in instructions:

        if instruction.startswith("@"):
            symbol = instruction[1:]

            if symbol.isdigit():
                continue

            if not valid_symbol(symbol):
                raise AssemblerError(
                    line_number, "Invalid symbol: " + symbol
                )

            if symbol not in symbol_table:
                if next_address >= 16384:
                    raise AssemblerError(
                        line_number, "No available RAM for new variables"
                    )

                symbol_table[symbol] = next_address
                print(
                    f"Variable allocated: {symbol} = {next_address}"
                )
                next_address += 1


def translate_a_instruction(instruction, symbol_table, line_number):
    if not instruction.startswith("@") or len(instruction) == 1:
        raise AssemblerError(
            line_number, "Invalid A-instruction"
        )

    symbol = instruction[1:]

    if symbol.isdigit():
        address = int(symbol)

    elif valid_symbol(symbol) and symbol in symbol_table:
        address = symbol_table[symbol]

    else:
        raise AssemblerError(
            line_number, "Invalid or unknown symbol: " + symbol
        )

    if address < 0 or address > 32767:
        raise AssemblerError(
            line_number,
            "A-instruction address must be between 0 and 32767"
        )

    return format(address, "016b")


def translate_c_instruction(instruction, line_number):
    dest = ""
    jump = ""

    if instruction.count("=") > 1:
        raise AssemblerError(
            line_number, "Invalid destination syntax"
        )

    if instruction.count(";") > 1:
        raise AssemblerError(
            line_number, "Invalid jump syntax"
        )

    if "=" in instruction:
        parts = instruction.split("=")
        dest = parts[0]
        instruction = parts[1]

    if ";" in instruction:
        parts = instruction.split(";")
        instruction = parts[0]
        jump = parts[1]

    if dest not in DEST_TABLE:
        raise AssemblerError(
            line_number, "Invalid destination: " + dest
        )

    if instruction not in COMP_TABLE:
        raise AssemblerError(
            line_number, "Invalid computation: " + instruction
        )

    if jump not in JUMP_TABLE:
        raise AssemblerError(
            line_number, "Invalid jump: " + jump
        )

    return (
        "111"
        + COMP_TABLE[instruction]
        + DEST_TABLE[dest]
        + JUMP_TABLE[jump]
    )


def assemble():
    # Remove an old output file before starting a new assembly.
    if os.path.exists(OUTPUT_FILE):
        os.remove(OUTPUT_FILE)

    instructions = read_assembly_file(INPUT_FILE)

    print("Assembly Instructions:")

    for line_number, instruction in instructions:
        print(f"Line {line_number} : {instruction}")

    symbol_table = create_symbol_table()

    # First pass: process labels.
    first_pass(instructions, symbol_table)

    # Allocate RAM addresses to variables.
    allocate_variables(instructions, symbol_table)

    machine_code = []

    # Second pass: translate instructions.
    for line_number, instruction in instructions:

        if instruction.startswith("(") and instruction.endswith(")"):
            continue

        if instruction.startswith("@"):
            code = translate_a_instruction(
                instruction, symbol_table, line_number
            )
        else:
            code = translate_c_instruction(
                instruction, line_number
            )

        machine_code.append(code)

    # Save machine code only if all instructions are valid.
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

    with open(OUTPUT_FILE, "w") as file:
        for code in machine_code:
            file.write(code + "\n")

    print("\nTranslated Machine Code:")

    for code in machine_code:
        print(code)

    print("\nStage 7 completed successfully!")
    print("Machine code saved at:", OUTPUT_FILE)


if __name__ == "__main__":
    try:
        assemble()

    except AssemblerError as error:
        print(
            f"\nAssembler Error: Line {error.line_number}: "
            f"{error.message}"
        )

    except FileNotFoundError:
        print("\nAssembler Error: Input assembly file not found.")

    except Exception as error:
        print("\nAssembler Error:", error)
  