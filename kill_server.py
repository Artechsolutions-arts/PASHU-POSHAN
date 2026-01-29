import os
import signal
import sys
import subprocess
import time

def kill_port(port):
    print(f"Finding process on port {port}...")
    try:
        # Windows specific
        cmd = f"netstat -ano | findstr :{port}"
        output = subprocess.check_output(cmd, shell=True).decode()
        lines = output.strip().split('\n')
        pids = set()
        for line in lines:
            parts = line.strip().split()
            if len(parts) > 4:
                pid = parts[-1]
                pids.add(pid)
        
        if not pids:
            print(f"No process found on port {port}.")
            return

        for pid in pids:
            print(f"Killing PID {pid}...")
            os.system(f"taskkill /F /PID {pid}")
            
    except subprocess.CalledProcessError:
        print(f"No process found on port {port}.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    kill_port(8000)
