
// =======================================
// PROJECT: MAKE THE COMPUTER DRAW A BOX
// Width  = 64 pixels
// Height = 20 pixels
// Start row = 43
// =======================================

// SCREEN START ADDRESS:
// 16384 + (32 * 43) = 17760

@17760
D=A
@addr
M=D

// Set row counter to 20

@20
D=A
@rows
M=D

// START DRAWING

(ROW_LOOP)

// Four words = 64 pixels

@4
D=A
@words
M=D

(WORD_LOOP)

// Fill current screen word with white pixels

@addr
A=M
M=-1

// Move to next screen word

@addr
M=M+1

// Decrease word counter

@words
M=M-1

// Continue until four words are filled

@words
D=M
@WORD_LOOP
D;JGT

// Move to the next screen row.
// Four words were already written.
// Remaining 28 words are skipped.

@28
D=A
@addr
M=D+M

// Decrease row counter

@rows
M=M-1

@rows
D=M
@ROW_LOOP
D;JGT

// STOP PROGRAM

(END)
@END
0;JMP
