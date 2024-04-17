import subprocess
from time import sleep

def start_anonsurf(password):
    try:
        # Start anonsurf with sudo password
        process = subprocess.Popen(['sudo', '-S', 'anonsurf', 'start'], stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        process.communicate(password.encode())
        if process.returncode != 0:
            raise subprocess.CalledProcessError(process.returncode, 'anonsurf start')
        print("Anonsurf started successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to start Anonsurf: {e}")

def stop_anonsurf(password):
    try:
        # Stop anonsurf with sudo password
        process = subprocess.Popen(['sudo', '-S', 'anonsurf', 'stop'], stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        process.communicate(password.encode())
        if process.returncode != 0:
            raise subprocess.CalledProcessError(process.returncode, 'anonsurf stop')
        print("Anonsurf stopped successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to stop Anonsurf: {e}")

# Example usage
password = "Jkl;Fdsa" #"your_sudo_password_here" # Replace with your actual sudo password
start_anonsurf(password)
sleep(2)
gettogo = input("go konim?")
# Do some tasks while anonsurf is running
stop_anonsurf(password)
