# Nand-To-Tetris-Assignments

## Other Repository Contents

Apart from the Capstone Project, this repository also contains my Nand2Tetris Theory Assignments 1 to 4. These assignments are organised separately under the `1. Theory Assignments` folder.

The repository also includes the lab assignments 1 to 4 updated in zosima.ai as well, completed as part of the course.


#capstone project implementation details
# Make the Computer Draw a Box

## Nand2Tetris Capstone Project

**University:** K.R. Mangalam University  
**Student Name:** Himanshu Mondal  
**Roll Number:** 2501740143  
**Course Code:** ETCCNT301  

---

## About the Project

This project is based on the Nand2Tetris computer system. The main aim was to understand how a computer works internally and how hardware and software work together.

The project is divided into three parts. First, I worked on building the basic Hack computer components using HDL. Then, I developed a Python-based assembler to convert Hack assembly instructions into machine code. Finally, I wrote an assembly program that draws a rectangular box on the Hack screen.

## Project Structure

```text
3.Capstone Project/
│
├── Part_A/
│   ├── CPU.hdl
│   ├── Memory.hdl
│   └── Computer.hdl
│
├── Part_B/
│   ├── assembler.py
│   ├── prog.asm
│   └── output/
│       └── Prog.hack
│
├── Part_C/
│   ├── Box.asm
│   └── Box.hack
│
├── Report/
│   ├── Final Report.docx
│   └── Final Report.pdf
│
├── Screenshots/
│
└── README.md
```

## Part A – Hardware Implementation

In this part, I implemented three main components of the Hack computer using HDL.

- **CPU.hdl:** Handles instruction execution and processing.
- **Memory.hdl:** Provides access to RAM, screen memory and keyboard input.
- **Computer.hdl:** Connects the CPU, memory and instruction ROM to form the complete computer.

All three components were tested using the Hardware Simulator, and the simulations completed successfully.

## Part B – Python Assembler

For this part, I developed a Python program called `assembler.py`.

The assembler converts Hack assembly language instructions into 16-bit binary machine code.

The main features include:

- Translation of A-instructions and C-instructions.
- Handling of predefined symbols and labels.
- Allocation of RAM addresses for variables.
- Generation of `.hack` machine-code files.
- Error messages for invalid instructions, including their line numbers.

The assembler was tested using a sample assembly program and generated `Prog.hack` successfully. An invalid instruction was also tested to check the error-handling feature.

## Part C – Make the Computer Draw a Box

In the final part, I created `Box.asm` to draw a filled black rectangle on the Hack screen.

**Required dimensions:**

- Width: 64 pixels
- Height: 20 pixels
- Starting row: 43

The screen memory starts at address 16384. Each row contains 32 memory words, and each word represents 16 pixels.

The starting memory address was calculated as:

```text
16384 + (32 × 43) = 17760
```

The program uses loops to fill four consecutive screen words in each row and repeats the process for 20 rows.

The program was assembled into `Box.hack` and executed in the CPU Emulator. The rectangle appeared on the screen at the expected position.

## Technologies and Tools Used

- Hack Hardware Description Language (HDL)
- Python
- Hack Assembly Language
- Nand2Tetris Hardware Simulator
- Nand2Tetris CPU Emulator
- Visual Studio Code
- GitHub

## Testing and Results

The following tests were performed during the project:

1. CPU HDL simulation completed successfully.
2. Memory HDL simulation completed successfully.
3. Computer HDL simulation completed successfully.
4. Python assembler generated the expected machine-code output.
5. Invalid instruction testing displayed the correct line number.
6. Box drawing program executed successfully in the CPU Emulator.
7. Screen memory addresses were checked to verify the rectangle's dimensions.

Screenshots of the implementation and testing process are available in the `Screenshots` folder.

## Project Report

The detailed project report is available in the `Report` folder in both Word and PDF formats.

## Conclusion

Working on this project gave me practical experience with the internal working of the Hack computer. I learned how hardware components are connected, how assembly instructions are converted into machine code, and how memory can be used to control the screen.

It was a useful hands-on experience that helped me understand the connection between hardware, assembly language and computer architecture.

---

**Submitted by:** Himanshu Mondal  
**Roll Number:** 2501740143  
**K.R. Mangalam University**
