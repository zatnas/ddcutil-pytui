# import curses
# 
# def main(stdscr):
#     stdscr.clear()
# 
#     pos_x = 0
#     pos_y = 0
#     size_x = curses.COLS - 1
#     size_y = curses.LINES - 1
#     win = curses.newwin(size_y, size_x, pos_y, pos_x)
# 
#     win.addstr(0, 0, f'ddcutil tui')
# 
#     stdscr.refresh()
#     win.refresh()
# 
#     stdscr.getkey()
# 
# curses.wrapper(main)

import subprocess
import pprint

async def get_display_vcp(display_index:int=None, opcode:str=None):
    getvcp_command = subprocess.run(["ddcutil", "-b", str(index), "getvcp", opcode], capture_output=True)
    getvcp_output = getvcp_command.stdout.decode()
    print(getvcp_output)

def get_display_capabilities(index:int=None):
    capabilities_command = subprocess.run(["ddcutil", "-b", str(index), "capabilities"], capture_output=True)
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
    for feature in features:
        if feature["name"] == "Manufacturer specific feature":
            continue
        print(feature)
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
    for display in displays:
        get_display_capabilities(display["index"])
    return displays

displays = get_displays()
