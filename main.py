import subprocess
import os
from collections import defaultdict
# import re

###############################################################################

'''
    PROBLEM_NUMBER: name of the folder with student solutions
    SOURCE_FILE(S): name of the file(s) to be compiled seperated by spaces
    TEST_CASES: list of input test cases
    EXPECTED_OUTPUTS: list of expected outputs to those test cases
'''

problem_number = 'temp'
source_files = []
test_cases = []
expected_outputs = []

###############################################################################

try:
    with open('settings.txt', 'r') as file:
        for line in file:
            if line == 'PROBLEM NAME:\n':
                problem_number = file.readline().strip()
            
            if line == "SOURCE FILE(S):\n":
                while True:
                    source_file = file.readline()
                    if (len(source_file) == 80):
                        break
                    elif (source_file == '\n'):
                        continue
                    else:
                        source_files.append(source_file.strip())

            if line == "TEST CASES:\n":
                test_case = ''
                while True:
                    reader = file.readline()
                    if (len(source_file) == 80):
                        test_cases.append(test_case)
                        break
                    elif (reader == '\n'):
                        test_cases.append(test_case)
                        test_case = ''
                    else:
                        test_case += reader
                    
            
            if line == "EXPECTED OUTPUTS:\n":
                expected_output = ''
                while True:
                    reader = file.readline()
                    if (reader[0] == '='):
                        expected_outputs.append(expected_output)
                        break
                    elif (reader == '\n'):
                        expected_outputs.append(expected_output)
                        expected_output = ''
                    else:
                        expected_output += reader               

except FileNotFoundError:
    print(f"File '{file}' not found.")
except Exception as e:
    print(f"An error occurred: {e}")

print(expected_outputs)

students = os.listdir(problem_number)

student_compilation_error = set()
student_header_comment_missing = set()
student_over_char_limit = set()
student_output = defaultdict(list)

for student in students:
    if student == 'gmarcano01':
        continue
    ### get paths for the source files
    path_to_student = f'{problem_number}/{student}/'
    print(path_to_student)
    source_files_paths = [path_to_student + file for file in source_files]

    ### compile the code
    compile_command = ['gcc'] + source_files_paths + ['-o', f'{path_to_student}run']
    result = subprocess.run(compile_command, stdout=subprocess.PIPE, 
                            stderr=subprocess.PIPE, text=True)
    
    ### check if code failed to compile compile
    if result.returncode != 0:
        print(f"Compilation failed. Error output:\n{result.stderr}")
        student_compilation_error.add(
            f'Projects/Homework_Checker/{path_to_student}{source_files[0]}')
        continue
    
    for input in test_cases:    
        ### run the code with the test case input
        run_command = [f'./{path_to_student}run']
        output = subprocess.run(run_command,input=input, 
                                stdout=subprocess.PIPE, text=True).stdout
        student_output[path_to_student].append(output)

    header = False
    for path in source_files_paths:
        try:
            with open(path, "r") as file:

                ### check for header comment
                code = file.read()
                index = code.find('CH-230-A')
                if index != -1:
                    header = True

                ### check for 80 characters per line limit
                for line in file:
                    if len(line) > 80:
                        student_over_char_limit.add(path_to_student)
                        break
        except FileNotFoundError:
            print(f"File '{path}' not found.")
        except Exception as e:
            print(path)
            print(f"An error occurred: {e}")

    if header == False:
        student_header_comment_missing.add(path_to_student)


try:
    with open('results.txt', 'w') as file:
        for i in range(80):
            file.write('=')
        file.write('\n')

        file.write('STUDENTS WITH COMPILATION ERRORS:\n\n')
        for student in student_compilation_error:
            full_path = f'file://home/jlumi/Projects/Homework_Checker/{student}{source_files[0]}'
            file.write(f'{full_path}\n')

        file.write('\n')
        for i in range(80):
            file.write('=')
        file.write('\n')

        file.write('STUDENTS WITH MISSING COMMENT HEADER:\n\n')
        for student in student_header_comment_missing:
            full_path = f'file://home/jlumi/Projects/Homework_Checker/{student}{source_files[0]}'
            file.write(f'{full_path}\n')

        file.write('\n')
        for i in range(80):
            file.write('=')
        file.write('\n')
        
        file.writelines('STUDENTS OVER 80 CHARACTERS PER LINE:\n\n')
        for student in student_over_char_limit:
            full_path = f'file://home/jlumi/Projects/Homework_Checker/{student}{source_files[0]}'
            file.write(f'{full_path}\n')

        file.write('\n')
        for i in range(80):
            file.write('=')
        file.write('\n')    
        
        ### compare the student's outputs with the expected outputs
        file.write('STUDENTS WHO DID NOT PASS TEST CASES:\n\n')
        for student, output in student_output.items():
            print(output)
            comparisons_result = [i == j 
                                  for i, j in zip(expected_outputs, output)]

            for comparison_result in comparisons_result:
                if comparison_result == False:
                    full_path = f'file://home/jlumi/Projects/Homework_Checker/{student}{source_files[0]}'
                    file.write(f'{full_path}\n')
                    file.writelines(expected_outputs)
                    file.write('\n')
                    file.writelines(output)
                    file.write('\n')

        for i in range(80):
            file.write('=')
        file.write('\n')  

except FileNotFoundError:
    print(f"File '{file}' not found.")
except Exception as e:
    print(f"An error occurred: {e}")