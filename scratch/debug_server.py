
import subprocess
import os
import sys

def run():
    print("Starting server diagnostic...")
    cwd = os.getcwd()
    print(f"CWD: {cwd}")
    
    python_exe = os.path.join(cwd, "env", "Scripts", "python.exe")
    if not os.path.exists(python_exe):
        print(f"ERROR: python.exe not found at {python_exe}")
        return

    cmd = [python_exe, "-m", "uvicorn", "main:app", "--host", "127.0.0.1", "--port", "8000"]
    print(f"Running command: {' '.join(cmd)}")
    
    try:
        # Run with a timeout of 5 seconds to see if it starts or crashes immediately
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        try:
            stdout, stderr = process.communicate(timeout=5)
            print("Server process exited early.")
            print("STDOUT:")
            print(stdout)
            print("STDERR:")
            print(stderr)
        except subprocess.TimeoutExpired:
            print("Server seems to be running (didn't crash in 5 seconds).")
            process.terminate()
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    run()
