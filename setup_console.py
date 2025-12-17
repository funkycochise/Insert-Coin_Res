import curses
import configparser

INI_FILE = "setup.ini"
IGNORE_SECTIONS = ["reserved", "setup"]

parser = configparser.ConfigParser()
parser.optionxform = str
parser.read(INI_FILE, encoding="utf-8")

sections = [s for s in parser.sections() if s not in IGNORE_SECTIONS]

DUALSDRAM_DESC = {
    "0": "single SDRAM core",
    "1": "Dual SDRAM core",
    "2": "Both Single and Dual SDRAM cores"
}

def toggle_value(section, key):
    val = parser[section][key].strip()
    if val == "0":
        parser[section][key] = "1"
    elif val == "1":
        parser[section][key] = "0"
    with open(INI_FILE, "w", encoding="utf-8") as f:
        parser.write(f)

def cycle_dualsdram(section, key):
    val = parser[section][key].strip()
    if val not in ["0", "1", "2"]:
        val = "0"
    next_val = {"0": "1", "1": "2", "2": "0"}[val]
    parser[section][key] = next_val
    with open(INI_FILE, "w", encoding="utf-8") as f:
        parser.write(f)

def main(stdscr):
    curses.curs_set(0)
    stdscr.keypad(True)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)  # bleu sélection et non sélection
    curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)  # texte non sélectionné en bleu

    current_section = 0
    current_key = 0
    mode = "section"

    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, "↑/↓ naviguer, Entrée toggle/cycle dualsdram, Échap pour quitter", curses.color_pair(1))

        if mode == "section":
            stdscr.addstr(2, 0, "Sélectionne une section :", curses.color_pair(1))
            for i, sec in enumerate(sections):
                if i == current_section:
                    stdscr.addstr(3 + i, 0, "> " + sec, curses.color_pair(1) | curses.A_REVERSE)
                else:
                    stdscr.addstr(3 + i, 0, "  " + sec, curses.color_pair(2))
            exit_index = len(sections)
            if current_section == exit_index:
                stdscr.addstr(3 + exit_index, 0, "> Exit", curses.color_pair(1) | curses.A_REVERSE)
            else:
                stdscr.addstr(3 + exit_index, 0, "  Exit", curses.color_pair(2))
        else:
            sec = sections[current_section]
            keys = list(parser[sec].keys())
            stdscr.addstr(2, 0, f"Sélectionne une clé dans [{sec}] :", curses.color_pair(1))
            for i, k in enumerate(keys):
                val = parser[sec][k]
                if k == "dualsdram":
                    desc = DUALSDRAM_DESC.get(val, "")
                    line = f"{k} = {val} ({desc})"
                else:
                    line = f"{k} = {val}"
                if i == current_key:
                    stdscr.addstr(3 + i, 0, "> " + line, curses.color_pair(1) | curses.A_REVERSE)
                else:
                    stdscr.addstr(3 + i, 0, "  " + line, curses.color_pair(2))
            exit_index = len(keys)
            if current_key == exit_index:
                stdscr.addstr(3 + exit_index, 0, "> Exit", curses.color_pair(1) | curses.A_REVERSE)
            else:
                stdscr.addstr(3 + exit_index, 0, "  Exit", curses.color_pair(2))

        stdscr.refresh()
        key = stdscr.getch()

        if key == 27:  # Échap
            if mode == "key":
                mode = "section"
                current_key = 0
            else:
                break
        elif key == curses.KEY_UP:
            if mode == "section":
                current_section = current_section - 1 if current_section > 0 else len(sections)
            elif mode == "key":
                sec = sections[current_section]
                keys = list(parser[sec].keys())
                current_key = current_key - 1 if current_key > 0 else len(keys)
        elif key == curses.KEY_DOWN:
            if mode == "section":
                current_section = current_section + 1 if current_section < len(sections) else 0
            elif mode == "key":
                sec = sections[current_section]
                keys = list(parser[sec].keys())
                current_key = current_key + 1 if current_key < len(keys) else 0
        elif key in [10, 13]:  # Entrée
            if mode == "section":
                if current_section == len(sections):
                    break
                else:
                    mode = "key"
                    current_key = 0
            else:
                sec = sections[current_section]
                keys = list(parser[sec].keys())
                if current_key == len(keys):
                    mode = "section"
                    current_key = 0
                else:
                    k = keys[current_key]
                    if k == "dualsdram":
                        cycle_dualsdram(sec, k)
                    else:
                        toggle_value(sec, k)

curses.wrapper(main)
