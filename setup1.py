import curses
import configparser
import textwrap
import os
import subprocess

BANNER = [
" ██▓███▄    █  ██████▓█████ ██▀███ ▄▄▄█████▓    ▄████▄  ▒█████  ██▓███▄    █",
"▓██▒██ ▀█   █▒██    ▒▓█   ▀▓██ ▒ ██▓  ██▒ ▓▒   ▒██▀ ▀█ ▒██▒  ██▓██▒██ ▀█   █",
"▒██▓██  ▀█ ██░ ▓██▄  ▒███  ▓██ ░▄█ ▒ ▓██░ ▒░   ▒▓█    ▄▒██░  ██▒██▓██  ▀█ ██▒",
"░██▓██▒  ▐▌██▒ ▒   ██▒▓█  ▄▒██▀▀█▄ ░ ▓██▓ ░    ▒▓▓▄ ▄██▒██   ██░██▓██▒  ▐▌██▒",
"░██▒██░   ▓██▒██████▒░▒████░██▓ ▒██▒ ▒██▒ ░    ▒ ▓███▀ ░ ████▓▒░██▒██░   ▓██░",
"░▓ ░ ▒░   ▒ ▒▒ ▒▓▒ ▒ ░░ ▒░ ░ ▒▓ ░▒▓░ ▒ ░░      ░ ░▒ ▒  ░ ▒░▒░▒░░▓ ░ ▒░   ▒ ▒ ",
" ▒ ░ ░░   ░ ▒░ ░▒  ░ ░░ ░  ░ ░▒ ░ ▒░   ░         ░  ▒    ░ ▒ ▒░ ▒ ░ ░░   ░ ▒░",
" ▒ ░  ░   ░ ░░  ░  ░    ░    ░░   ░  ░         ░       ░ ░ ░ ▒  ▒ ░  ░   ░ ░ ",
" ░          ░      ░    ░  ░  ░                ░ ░         ░ ░  ░          ░ ",
"                                               ░                             ",
"    "
]

INI_FILE = "setup.ini"
IGNORE_SECTIONS = ["setup", "reserved"]

RUN_CMD = ["bash", "/media/fat/Scripts/#insertcoin/run.sh"]

DEFAULT_CONFIG = {
    "update": {"main_mister": "0","mame_rom": "0","gnw_rom": "0","additional_res": "0","console_core": "0","dualsdram": "0"},
    "console": {"psx": "0","s32x": "0","saturn": "0","sgb": "0","neogeo": "0","n64": "0","jaguar": "0","cdi": "0","pce": "0","nes": "0","snes": "0"},
    "clean": {"console_mgl": "0","obsolete_core": "0","remove_other": "0"},
    "folder": {"essential": "1","rootfolder": "0","show_system": "1","show_genre": "1","manufacturer_subfolder": "0"}
}

DUALSDRAM_DESC = {
    "0": "single SDRAM core",
    "1": "Dual SDRAM core",
    "2": "Both Single and Dual SDRAM cores"
}

SECTION_TOOLTIPS = {
    "update": "Settings for Update",
    "console": "Settings for Console Cores",
    "clean": "Settings for Cleaning obsolete cores and useless files",
    "folder": "Settings for folders to create"
}

MAIN_MENU_TOOLTIPS = {
    "Run": "Run Insert-Coin script with current configuration",
    "Setup": "Configure options before running the script",
    "Save": "Save current configuration to setup.ini",
    "Reset": "Reset configuration to default values",
    "Exit": "Exit Insert-Coin setup"
}

def ensure_ini(filename, default_config):
    if not os.path.exists(filename):
        parser = configparser.ConfigParser()
        for sec, opts in default_config.items():
            parser[sec] = opts
        with open(filename, "w", encoding="utf-8") as f:
            parser.write(f)

ensure_ini(INI_FILE, DEFAULT_CONFIG)

parser = configparser.ConfigParser()
parser.optionxform = str
parser.read(INI_FILE, encoding="utf-8")

sections = [s for s in parser.sections() if s.lower() not in (i.lower() for i in IGNORE_SECTIONS)]
config = {sec: dict(parser[sec]) for sec in sections}

def toggle_value(sec, key):
    val = config[sec][key]
    if key == "dualsdram":
        config[sec][key] = {"0":"1","1":"2","2":"0"}[val]
    else:
        config[sec][key] = "1" if val == "0" else "0"

def save_config():
    parser = configparser.ConfigParser()
    parser.optionxform = str
    parser.read(INI_FILE, encoding="utf-8")
    for sec, opts in config.items():
        if not parser.has_section(sec):
            parser.add_section(sec)
        for k, v in opts.items():
            parser.set(sec, k, v)
    with open(INI_FILE, "w", encoding="utf-8") as f:
        parser.write(f)

def reset_config():
    global config
    config = {sec: dict(opts) for sec, opts in DEFAULT_CONFIG.items()}

def draw_tooltip(stdscr, text):
    if not text:
        return
    h, w = stdscr.getmaxyx()
    lines = textwrap.wrap(text, w-2)
    y = h - len(lines) - 2
    stdscr.hline(y, 0, curses.ACS_HLINE, w)
    for i, line in enumerate(lines):
        stdscr.addstr(y+1+i, 1, line, curses.color_pair(1))

def do_run():
    curses.endwin()
    process = subprocess.Popen(
        ["stdbuf", "-o0", "-e0"] + RUN_CMD,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )
    for line in process.stdout:
        print(line, end='', flush=True)
    process.wait()
    input("Press Enter to continue")

def main(stdscr):
    curses.curs_set(0)
    stdscr.keypad(True)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)

    main_menu = ["Run", "Setup", "Save", "Reset", "Exit"]
    RUN_INDEX = main_menu.index("Run")

    current_selection = 0
    last_selection = current_selection
    countdown = 5

    stdscr.timeout(1000)

    while True:
        stdscr.clear()
        for i, line in enumerate(BANNER):
            stdscr.addstr(i, 0, line, curses.color_pair(3))

        for i, item in enumerate(main_menu):
            style = curses.A_REVERSE if i == current_selection else 0
            stdscr.addstr(len(BANNER)+1+i, 0,
                ("> " if i == current_selection else "  ") + item,
                curses.color_pair(1)|style if i == current_selection else curses.color_pair(2))

        h, _ = stdscr.getmaxyx()
        if current_selection == RUN_INDEX:
            stdscr.addstr(h-1, 0, f"AutoRun in {countdown} sec", curses.color_pair(1))

        draw_tooltip(stdscr, MAIN_MENU_TOOLTIPS.get(main_menu[current_selection], ""))
        stdscr.refresh()

        key = stdscr.getch()

        if key == -1:
            if current_selection == RUN_INDEX:
                countdown -= 1
                if countdown <= 0:
                    do_run()
                    return
            continue

        stdscr.timeout(-1)

        if key == 27:
            break
        elif key == curses.KEY_UP:
            current_selection = (current_selection - 1) % len(main_menu)
        elif key == curses.KEY_DOWN:
            current_selection = (current_selection + 1) % len(main_menu)
        elif key in [10, 13, 32]:
            sel = main_menu[current_selection]
            if sel == "Exit":
                break
            elif sel == "Run":
                do_run()
                return
            elif sel == "Save":
                save_config()
            elif sel == "Reset":
                reset_config()

        if last_selection == RUN_INDEX and current_selection != RUN_INDEX:
            countdown = 5

        if current_selection != RUN_INDEX:
            countdown = 5

        last_selection = current_selection
        stdscr.timeout(1000)

curses.wrapper(main)
