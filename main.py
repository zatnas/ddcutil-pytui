import subprocess

def get_displays():
    displays_command = subprocess.run(["ddcutil", "detect"], capture_output=True)
    displays_output = displays_command.stdout.decode()
    displays = []
    display = {}
    for line in displays_output.splitlines():
        if not line:
            continue
        if "Display" in line:
            if display:
                displays.append({**display})
                display = {}
            display["index"] = int(line[8:])
        elif "I2C bus" in line:
            display["path"] = line.split()[2]
        elif "Model" in line:
            display["model"] = ' '.join(line.split()[1:])
        elif "VCP version" in line:
            display["vcp_version"] = line.split()[2]
    displays.append({**display})
    return displays

displays = get_displays()
