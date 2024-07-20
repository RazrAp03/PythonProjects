import subprocess

if __name__ == '__main__':
    print("Welcome to RoboTalk 1.0")
    print("Press 'Q' to exit.")
    while True:
        text = input("Enter whatever you want me to say: ")

        # Create the PowerShell command
        command = f'Add-Type -AssemblyName System.Speech; (New-Object System.Speech.Synthesis.SpeechSynthesizer).Speak("{text}")'
        
        # Execute the PowerShell command using subprocess
        subprocess.call(["powershell", "-Command", command])
        
        if text == 'Q':
            break
