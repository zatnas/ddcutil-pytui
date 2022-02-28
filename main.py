import subprocess
def get_display_capabilities(index:int=None):
    capabilities_command = subprocess.run(["ddcutil", "-b", "1", "capabilities"], capture_output=True)
    capabilities_output = capabilities_command.stdout.decode()
    features = []
    feature = {}
    value_mode = False
    for line in capabilities_output.splitlines():
        if not line:
            continue
        if "Feature:" in line:
            if feature:
                features.append({**feature})
                feature = {}
            value_mode = False
            feature["opcode"] = line.split()[1]
            feature["name"] = ' '.join(line.split()[2:])[1:-1]
        elif line.replace(" ","") == "Values:":
            value_mode = True
            feature["values"] = []
        elif value_mode:
            value_value = line.split()[0][:-1]
            value_name = ' '.join(line.split()[1:])
            feature["values"].append({
                "name": value_name,
                "value": value_value,
            })
        elif "Values:" in line and "interpretation unavailable" in line:
            feature["values"] = [
                {
                    "name": "",
                    "value": value,
                }
                for value in line.split()[1:-2]
            ]
    return features

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
