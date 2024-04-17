import subprocess
from time import sleep

def start_anonsurf():
    try:
        # Start anonsurf
        subprocess.run(['sudo', 'anonsurf', 'start'], check=True)
        print("Anonsurf started successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to start Anonsurf: {e}")

def stop_anonsurf():
    try:
        # Stop anonsurf
        subprocess.run(['sudo', 'anonsurf', 'stop'], check=True)
        print("Anonsurf stopped successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to stop Anonsurf: {e}")

# Example usage
start_anonsurf()
sleep(20)
gettogo = input("go konim?")
# Do some tasks while anonsurf is running
stop_anonsurf()