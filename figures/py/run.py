import os
import subprocess
import sys

def run_all_py_files():
    current_file = os.path.basename(__file__)
    current_dir = os.path.dirname(os.path.abspath(__file__))

    for file in os.listdir(current_dir):
        if file.endswith('.py') and file != current_file:
            file_path = os.path.join(current_dir, file)
            print(f'Running: {file}')
            subprocess.run([sys.executable, file_path])

if __name__ == '__main__':
    run_all_py_files()
