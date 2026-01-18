import curses
import configparser
import textwrap
import os
import sys

# ------------------- Fichiers INI -------------------
INI_FILE = "setup.ini"
NAMES_FILE = "names.ini"

DEFAULT_CONFIG = {
    "update": {"main_mister": "0","mame_rom": "0","gnw_rom": "0","additional_res": "0","console_core": "0","dualsdram": "0"},
    "console": {"psx": "1","s32x": "1","saturn": "1","sgb": "1","neogeo": "1","n64": "1","jaguar": "1","cdi": "1","pce": "1","nes": "1","snes": "1"},
    "clean": {"console_mgl": "0","obsolete_core": "0","remove_other": "0"},
    "folder": {
        "essential": "1",
        "rootfolder": "1",
        "show_system": "1",
        "show_genre": "1",
        "manufacturer_subfolder": "0",
        "action": "1",
        "beat": "1",
        "horizontal": "1",
        "newest": "1",
        "puzzle": "1",
        "sport": "1",
        "stg_h": "1",
        "stg_v": "1",
        "vertical": "1",
        "vsf": "1",
        "rng_h": "1",
        "rng_v": "1"
    }
}

RAW_NAMES_CONTENT = """[folder]
essential="_#Essentials"
newest="_#Newest"

genre_horizontal="__Horizontal"
genre_vertical="__Vertical"
insertcoin="_#Insert-Coin"
genre_action="__Action"
genre_beat="__Beat'em up"
genre_puzzle="__Puzzle"
genre_sport="__Sport"
genre_vsf="__Vs Fighting"
genre_stg_h="__STG_H"
genre_stg_v="__STG_V"
genre_rng_h="__Run'n'Gun_H"
genre_rng_v="__Run'n'Gun_V"

alpha="_Alpha"
atari="_Atari"
bagman="_Bagman"
bally_midway="_Bally-midway"
capcom="_Capcom-Mitchell"
cps1="_CPS1"
cps15="_CPS15"
cps2="_CPS2"
cave="_Cave 68000"
crazykong="_Crazy Kong"
deco="_DataEast-Deco"
exidy="_Exidy"
galaxian="_Galaxian"
gottlieb="_Gottlieb"
irem="_Irem"
irem62="_Irem M62"
irem72="_Irem M72"
irem90="_Irem M90"
irem92="_Irem M92"
irem92t="_Irem M92t"
irem107="_Irem M107"
jaleco="_Jaleco"
kiwako="_Kiwako"
konami="_Konami"
konamitwin16="_Konami Twin16"
ladybug="_Ladybug"
mcr1="_MCR1"
mcr2="_MCR2"
mcr3="_MCR3"
mcr3mono="_Midway_MCR3Mono"
mcr3scroll="_Midway_MCR3Scroll"
midwayy="_Midway_YUnit"
namco="_Namco"
namco_sys1="_Namco-System-1"
namco_sys86="_Namco-System-86"
neogeo="_Neo-geo"
nichibutsu="_Nihon Bussan-Nichibutsu"
nintendo="_Nintendo"
vs="_Nintendo Vs."
pacman="_Pacman"
raizing="_Raizing-8ing"
rare="_Rare"
robotron="_Robotron"
scramble="_Scramble"
sega="_Sega"
outrun="_Sega-Outrun"
segasys1="_Sega-System-1"
segasys2="_Sega-System-2"
segasyse="_Sega-System-E"
segasys16="_Sega-System-16"
segasys18="_Sega-System-18"
segastv="_Sega-Titan Video"
snk="_SNK"
si="_Space Invaders"
stern="_Stern"
tad="_Tad Corp"
taito="_Taito"
taitof2="_Taito-F2"
taitosj="_Taito-SJ"
technos="_Technos"
technos16="_Technos16"
tecmo="_Tehkan-Tecmo"
toaplan="_Toaplan"
toaplan_stg="_Toaplan_STG"
universal="_Universal"
upl="_Upl"
williams="_Williams"
"""

def normalize_ini(filename):
    with open(filename, "r", encoding="utf-8") as f:
        lines = f.readlines()
    with open(filename, "w", encoding="utf-8") as f:
        for line in lines:
            if "=" in line and not line.lstrip().startswith("#"):
                k, v = line.split("=", 1)
                f.write(f"{k.strip()}={v.strip()}\n")
            else:
                f.write(line)

def ensure_ini(filename, default_config):
    if not os.path.exists(filename):
        parser = configparser.ConfigParser()
        for sec, opts in default_config.items():
            parser[sec] = opts
        with open(filename, "w", encoding="utf-8") as f:
            parser.write(f)
        normalize_ini(filename)

def ensure_names():
    if not os.path.exists(NAMES_FILE):
        with open(NAMES_FILE, "w", encoding="utf-8") as f:
            f.write(RAW_NAMES_CONTENT)

# --- Initialisation INI ---
ensure_ini(INI_FILE, DEFAULT_CONFIG)
ensure_names()

parser = configparser.ConfigParser()
parser.optionxform = str
parser.read(INI_FILE, encoding="utf-8")
sections = [s for s in parser.sections()]
config = {sec: dict(parser[sec]) for sec in sections}

# ------------------- Fonctions config -------------------
def toggle_value(sec, key):
    if key == "dualsdram":
        config[sec][key] = {"0":"1","1":"2","2":"0"}[config[sec][key]]
    else:
        config[sec][key] = "1" if config[sec][key] == "0" else "0"

def save_config():
    parser = configparser.ConfigParser()
    parser.optionxform = str
    for sec, opts in config.items():
        if not parser.has_section(sec):
            parser.add_section(sec)
        for k, v in opts.items():
            parser.set(sec, k, v)
    with open(INI_FILE, "w", encoding="utf-8") as f:
        parser.write(f)
    normalize_ini(INI_FILE)

def reset_config():
    global config
    config = {sec: dict(opts) for sec, opts in DEFAULT_CONFIG.items()}

SECTION_TOOLTIPS = {
    "update": "Settings for Update",
    "console": "Settings for Console Cores",
    "clean": "Settings for Cleaning obsolete cores and useless files",
    "folder": "Settings for folders to create",
    "Save": "Save configuration to setup.ini",
    "Reset": "Reset configuration to default values",
    "Exit": "Back to main menu"
}

def draw_tooltip(stdscr, text):
    if not text:
        return
    h, w = stdscr.getmaxyx()
    lines = textwrap.wrap(text, w-2)
    y = h - len(lines) - 2
    stdscr.hline(y, 0, curses.ACS_HLINE, w)
    for i, line in enumerate(lines):
        stdscr.addstr(y+1+i, 1, line, curses.color_pair(1))

# ------------------- Fonctions Bash -------------------
def do_Run():
    sys.exit(0)

def do_Exit():
    sys.exit(1)

# ------------------- Menu Setup -------------------
def run_setup_menu(stdscr):
    menu = sections + ["Save", "Reset", "Exit"]
    current = 0
    mode = "section"
    key_index = 0

    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, "↑/↓ browse  ←/→/Enter/Space toggle/select  Esc back", curses.color_pair(1))

        if mode == "section":
            for i, item in enumerate(menu):
                style = curses.A_REVERSE if i == current else 0
                stdscr.addstr(2+i, 0,
                    ("> " if i == current else "  ") + item,
                    curses.color_pair(1)|style if i == current else curses.color_pair(2))
            draw_tooltip(stdscr, SECTION_TOOLTIPS.get(menu[current], ""))
        else:
            sec = menu[current]
            keys = list(config[sec].keys()) + ["Exit"]
            for i, k in enumerate(keys):
                line = f"{k} = {config[sec][k]}" if k != "Exit" else "Exit"
                style = curses.A_REVERSE if i == key_index else 0
                stdscr.addstr(2+i, 0,
                    ("> " if i == key_index else "  ") + line,
                    curses.color_pair(1)|style if i == key_index else curses.color_pair(2))
            draw_tooltip(stdscr, "Toggle option value")

        stdscr.refresh()
        k = stdscr.getch()

        if k == 27:
            if mode == "key":
                mode = "section"
                key_index = 0
            else:
                return
        elif k == curses.KEY_UP:
            if mode == "section":
                current = (current - 1) % len(menu)
            else:
                key_index = (key_index - 1) % len(keys)
        elif k == curses.KEY_DOWN:
            if mode == "section":
                current = (current + 1) % len(menu)
            else:
                key_index = (key_index + 1) % len(keys)
        elif k in [10, 13, 32, curses.KEY_LEFT, curses.KEY_RIGHT]:
            if mode == "section":
                sel = menu[current]
                if sel == "Exit":
                    return
                elif sel == "Save":
                    save_config()
                elif sel == "Reset":
                    reset_config()
                else:
                    mode = "key"
                    key_index = 0
            else:
                if keys[key_index] == "Exit":
                    mode = "section"
                    key_index = 0
                else:
                    toggle_value(sec, keys[key_index])

# ------------------- Banner ASCII -------------------
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

# ------------------- Menu Principal -------------------
def main(stdscr):
    curses.curs_set(0)
    stdscr.keypad(True)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)

    main_menu = ["Run", "Setup", "Exit"]
    RUN_INDEX = main_menu.index("Run")
    current = 0
    last = 0
    countdown = 5
    autorun = True
    stdscr.timeout(1000)

    while True:
        stdscr.clear()
        for i, line in enumerate(BANNER):
            stdscr.addstr(i, 0, line, curses.color_pair(3))

        banner_height = len(BANNER)
        stdscr.addstr(banner_height, 0, "↑/↓ browse  ←/→/Enter/Space toggle/select  Esc exit", curses.color_pair(1))

        for i, item in enumerate(main_menu):
            style = curses.A_REVERSE if i == current else 0
            stdscr.addstr(banner_height+1+i, 0,
                ("> " if i == current else "  ") + item,
                curses.color_pair(1)|style if i == current else curses.color_pair(2))

        h, _ = stdscr.getmaxyx()
        if current == RUN_INDEX and autorun:
            stdscr.addstr(h-1, 0, f"AutoRun in {countdown} sec", curses.color_pair(1))

        draw_tooltip(stdscr, "")

        stdscr.refresh()
        k = stdscr.getch()

        if k == -1 and autorun:
            if current == RUN_INDEX:
                countdown -= 1
                if countdown <= 0:
                    do_Run()
            continue

        if k == 27:
            do_Exit()
        elif k == curses.KEY_UP:
            current = (current - 1) % len(main_menu)
        elif k == curses.KEY_DOWN:
            current = (current + 1) % len(main_menu)
        elif k in [10, 13, 32, curses.KEY_LEFT, curses.KEY_RIGHT]:
            if main_menu[current] == "Run":
                do_Run()
            elif main_menu[current] == "Setup":
                run_setup_menu(stdscr)
            elif main_menu[current] == "Exit":
                do_Exit()

        if last == RUN_INDEX and current != RUN_INDEX:
            countdown = 5
        if current != RUN_INDEX:
            countdown = 5
        last = current
        stdscr.timeout(1000)

curses.wrapper(main)
