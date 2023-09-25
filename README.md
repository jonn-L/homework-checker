# Homework Checker

Homework Checker is a script made using Python to assess student submmisons for a C/C++ program based on these criteria: 
- Passing of input test cases (if there is any)
- Reaching character limit per line (80 characters by default)
- Presence of a header comment (comment that contains student information)

## How to use the script

In 'settings.txt', parameters are set by typing them under each of the settings.

- Problem name: name of the folder that contains all the student folders with their solution to the problem inside of them.
- Source file(s): the file or list of files to be compiled.
- Test cases: input test cases seperated by newlines.
- Expected outputs: expected output to those test cases also seperated by newlines.

Here is an example:
```
===============================================================================
PROBLEM NAME:
folder_name
===============================================================================
SOURCE FILE(S):
file1.c
file2.c
file3.h
===============================================================================
TEST CASES:
input1
input1

input2
input2
===============================================================================
EXPECTED OUTPUTS:
output1
output1

output2
output2
===============================================================================

```

After setting this up, running the main.py file will write a 'results.txt' listing the students that did not meet the criteria mentioned before.

## Features to be added in the future

- Detect the presence of code comments
- Run the C/C++ code in a seperate virtual environment