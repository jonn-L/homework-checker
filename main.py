import subprocess
import os
from collections import defaultdict

problem_name = 'temp'
source_files = []
inputs = []
expected_outputs = []
char_limit = 80

try:
    with open('settings.txt', 'r') as file:
        for line in file:
            if line == 'PROBLEM NAME:\n':
                problem_name = file.readline().strip()
            
            if line == 'SOURCE FILE(S):\n':
                while True:
                    source_file = file.readline()
                    if (len(source_file) == 80):
                        break
                    elif (source_file == '\n'):
                        continue
                    else:
                        source_files.append(source_file.strip())

            if line == 'INPUTS:\n':
                input = ''
                while True:
                    reader = file.readline()
                    if (reader[0] == '='):
                        inputs.append(input)
                        break
                    elif (reader == '\n'):
                        inputs.append(input)
                        input = ''
                    else:
                        input += reader  
                    
            if line == 'EXPECTED OUTPUTS:\n':
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

            if line == 'CHAR LIMIT:\n':
                char_limit = int(file.readline())            

except FileNotFoundError:
    print(f"File '{file}' not found.")
except Exception as e:
    print(f"An error occurred: {e}")

print(problem_name)
print(source_files)
print(inputs)
print(expected_outputs)
print(char_limit)

students = os.listdir(problem_name)
print(len(students))

student_compilation_error = defaultdict()
student_header_comment_missing = set()
student_over_char_limit = set()
student_outputs = defaultdict(list)

for student in students:
    if student == 'azinovev':
        continue

    ### get paths for the source files
    path_to_student = f'{problem_name}/{student}'
    print(path_to_student)
    source_files_paths = [path_to_student + f'/{file}' for file in source_files]

    ### compile the code
    compile_command = ['gcc'] + source_files_paths + ['-o', f'{path_to_student}/run']
    result = subprocess.run(compile_command, stdout=subprocess.PIPE, 
                            stderr=subprocess.PIPE, text=True)
    
    ### check if code failed to compile compile
    if result.returncode != 0:
        full_path = os.path.join(path_to_student, source_files[0])
        student_compilation_error[full_path] = result.stderr
        continue
    
    for input in inputs:    
        ### run the code with the test case input
        run_command = [f'./{path_to_student}/run']
        output = subprocess.run(run_command,input=input, 
                                stdout=subprocess.PIPE, text=True).stdout
        full_path = os.path.join(path_to_student, source_files[0])
        student_outputs[full_path].append(output)

    header = False
    for path in source_files_paths:
        try:
            with open(path, "r") as file:

                ### check for header comment
                code = file.read()
                if 'CH-230-A' in code:
                    header = True
                else:
                    if student[1:] in code.lower():
                        header = True

                ### check for 80 characters per line limit
                if char_limit <= 0:
                    continue

                for line in file:
                    if len(line) > char_limit:
                        full_path = os.path.join(path_to_student, source_files[0])
                        student_over_char_limit.add(full_path)
                        break

        except FileNotFoundError:
            print(f"File '{path}' not found.")
        except Exception as e:
            print(path)
            print(f"An error occurred: {e}")

    if header == False:
        full_path = os.path.join(path_to_student, source_files[0])
        student_header_comment_missing.add(full_path)


try:
    with open('results.md', 'w') as file:
        file.write('### STUDENTS WITH COMPILATION ERRORS:\n')
        for path_to_student in student_compilation_error:
            parts = path_to_student.split('/')
            student = parts[1]
            file.write(f'- [{student}]({path_to_student})\n')

        file.write('\n---\n')

        file.write('### STUDENTS WITH MISSING COMMENT HEADER:\n')
        for path_to_student in student_header_comment_missing:
            parts = path_to_student.split('/')
            student = parts[1]
            file.write(f'- [{student}]({path_to_student})\n')

        file.write('\n---\n')
        
        if (char_limit):
            file.writelines(f'### STUDENTS OVER {char_limit} CHARACTERS PER LINE:\n')
            for path_to_student in student_over_char_limit:
                parts = path_to_student.split('/')
                student = parts[1]
                file.write(f'- [{student}]({path_to_student})\n')

        file.write('\n---\n')
        
        ### compare the student's outputs with the expected outputs
        file.write('### STUDENTS OUTPUTS:\n')
        for path_to_student, outputs in student_outputs.items():
            path_parts = path_to_student.split('/')
            student = path_parts[1]
            file.write(f'- [{student}]({path_to_student})\n')
            
            file.write('```\n')
            for expected_output, output in zip(expected_outputs, outputs):
                output_lines = output.split('\n')
                expected_output_lines = expected_output.split('\n')
                
                for output_line, expected_output_line in zip(output_lines, expected_output_lines):
                    file.write(f'{output_line:<25}')
                    file.write(f'\t{expected_output_line:<25}\n')
            file.write('```\n')

except FileNotFoundError:
    print(f"File '{file}' not found.")
except Exception as e:
    print(f"An error occurred: {e}")