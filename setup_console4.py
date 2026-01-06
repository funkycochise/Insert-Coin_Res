import curses
import configparser
import textwrap
import os
import subprocess

# ----------------------
# BANNIÈRE
# ----------------------
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
    "                                               ░                             "
]

# ----------------------
# CONSTANTES
# ----------------------
INI_FILE = "setup.ini"
NAMES_INI_FILE = "names.ini"
IGNORE_SECTIONS = ["reserved", "setup"]
RESERVED_VERSION = "1.0"

# ----------------------
# CONFIG PAR DÉFAUT
# ----------------------
DEFAULT_CONFIG = {
    "update": {
        "main_mister": "0",
        "mame_rom": "0",
        "gnw_rom": "0",
        "additional_res": "0",
        "console_core": "0",
        "dualsdram": "0"
    },
    "console": {
        "psx": "0", "s32x": "0", "saturn": "0", "sgb": "0", "neogeo": "0",
        "n64": "0", "jaguar": "0", "cdi": "0", "pce": "0", "nes": "0", "snes": "0"
    },
    "clean": {
        "console_mgl": "0", "obsolete_core": "1", "remove_other": "0"
    },
    "folder": {
        "essential": "1", "rootfolder": "0", "show_system": "1", "show_genre": "1",
        "manufacturer_subfolder": "0", "action": "1", "beat": "1", "horizontal": "1",
        "newest": "1", "puzzle": "1", "sport": "1", "stg_h": "1", "stg_v": "1",
        "vertical": "1", "vsf": "1", "rng_h": "1", "rng_v": "1"
    }
}

NAMES_DEFAULT_CONFIG = {
    "folder": {
        "essential": "_#Essentials", "newest": "_#Newest", "genre_horizontal": "__Horizontal",
        "genre_vertical": "__Vertical", "insertcoin": "_#Insert-Coin",
        "genre_action": "__Action", "genre_beat": "__Beat'em up", "genre_puzzle": "__Puzzle",
        "genre_sport": "__Sport", "genre_vsf": "__Vs Fighting",
        "genre_stg_h": "__STG_H", "genre_stg_v": "__STG_V", "genre_rng_h": "__Run'n'Gun_H",
        "genre_rng_v": "__Run'n'Gun_V"
    }
}

# ----------------------
# FONCTIONS DE GESTION DES INI
# ----------------------
def ensure_ini_file(file_path, default_config):
    """Crée ou complète un fichier INI avec les valeurs par défaut."""
    parser = configparser.ConfigParser()
    parser.optionxform = str
    updated = False

    if os.path.exists(file_path):
        parser.read(file_path, encoding="utf-8")

    for sec, opts in default_config.items():
        if not parser.has_section(sec):
            parser.add_section(sec)
            updated = True
        for key, val in opts.items():
            if not parser.has_option(sec, key):
                parser.set(sec, key, val)
                updated = True

    if updated or not os.path.exists(file_path):
        with open(file_path, "w", encoding="utf-8") as f:
            parser.write(f)


def read_ini(file_path, ignore_sections=None):
    """Lit un INI dans un dictionnaire."""
    parser = configparser.ConfigParser()
    parser.optionxform = str
    parser.read(file_path, encoding="utf-8")
    ignore_sections = ignore_sections or []
    return {sec: dict(parser[sec]) for sec in parser.sections() if sec not in ignore_sections}

# ----------------------
# INITIALISATION DES FICHIERS
# ----------------------
ensure_ini_file(INI_FILE, DEFAULT_CONFIG)
ensure_ini_file(NAMES_INI_FILE, NAMES_DEFAULT_CONFIG)

config = read_ini(INI_FILE, IGNORE_SECTIONS)
sections = list(config.keys())

# ----------------------
# TOOLTIP & DESCRIPTION
# ----------------------
DUALSDRAM_DESC = {"0": "single SDRAM core", "1": "Dual SDRAM core", "2": "Both Single and Dual SDRAM cores"}

SECTION_TOOLTIPS = {
    "update": "Settings for Update",
    "console": "Settings for Console Cores",
    "clean": "Settings for Cleaning for obsolete cores and useless files",
    "folder": "Settings for Folders to display",
    "Save": "Save modifications",
    "Reset": "Reset to default values",
    "Exit": "Exit"
}

KEY_TOOLTIPS = {
    "update": {
        "main_mister": "Installs custom main mister",
        "mame_rom": "Installs missing mame roms",
        "gnw_rom": "Installs missing Game & Watch roms",
        "additional_res": "Installs additional resources",
        "console_core": "Updates console cores",
        "dualsdram": "Selects single, dual or both SDRAM cores",
        "Exit": "Back to main menu"
    },
    # autres sections similaires...
}

# ----------------------
# FONCTIONS DE CONFIG
# ----------------------
def toggle_value(sec, key):
    val = config[sec][key].strip()
    if key == "dualsdram":
        config[sec][key] = {"0":"1","1":"2","2":"0"}.get(val,"0")
    else:
        config[sec][key] = "0" if val == "1" else "1"

def save_config():
    parser = configparser.ConfigParser()
    parser.optionxform = str
    parser["reserved"] = {"version": RESERVED_VERSION}
    for sec, opts in config.items():
        parser[sec] = opts
    with open(INI_FILE, "w", encoding="utf-8") as f:
        parser.write(f)

def reset_config():
    global config
    config = {sec: dict(opts) for sec, opts in DEFAULT_CONFIG.items() if sec in sections}

# ----------------------
# FONCTIONS D’AFFICHAGE
# ----------------------
def draw_tooltip(stdscr, text):
    if not text:
        return
    h, w = stdscr.getmaxyx()
    lines = textwrap.wrap(text, w - 2)
    y = h - len(lines) - 2
    stdscr.hline(y, 0, curses.ACS_HLINE, w)
    for i, line in enumerate(lines):
        stdscr.addstr(y + 1 + i, 1, line, curses.color_pair(1))

# ----------------------
# MENU SETUP
# ----------------------
def run_setup_menu(stdscr):
    current_section = 0
    current_key = 0
    mode = "section"
    main_menu = sections + ["Exit"]  # <-- Exit ajouté ici

    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, "↑/↓ to browse, Enter/Space to toggle, Escape to go back", curses.color_pair(1))

        if mode == "section":
            stdscr.addstr(2, 0, "Select section:", curses.color_pair(1))
            for i, sec in enumerate(main_menu):
                attr = curses.color_pair(1) | curses.A_REVERSE if i == current_section else curses.color_pair(2)
                stdscr.addstr(3 + i, 0, "> " + sec if i == current_section else "  " + sec, attr)
        else:
            sec = main_menu[current_section]
            if sec == "Exit":
                mode = "section"
                current_key = 0
                continue

            keys = list(config[sec].keys()) + ["Exit"]
            stdscr.addstr(2, 0, f"Options in [{sec}]:", curses.color_pair(1))
            for i, k in enumerate(keys):
                if k == "dualsdram":
                    val = config[sec][k]
                    line = f"{k} = {val} ({DUALSDRAM_DESC.get(val,'')})"
                else:
                    line = f"{k} = {config[sec].get(k,k)}"
                attr = curses.color_pair(1) | curses.A_REVERSE if i == current_key else curses.color_pair(2)
                stdscr.addstr(3 + i, 0, "> " + line if i == current_key else "  " + line, attr)

        tooltip = get_section_tooltip(main_menu[current_section]) if mode == "section" else "Back to main menu" if keys[current_key]=="Exit" else get_key_tooltip(sec, keys[current_key])
        draw_tooltip(stdscr, tooltip)

        stdscr.refresh()
        key = stdscr.getch()

        if key == 27:
            if mode == "key":
                mode = "section"
                current_key = 0
            else:
                break
        elif key == curses.KEY_UP:
            if mode == "section":
                current_section = (current_section - 1) % len(main_menu)
            else:
                current_key = (current_key - 1) % len(keys)
        elif key == curses.KEY_DOWN:
            if mode == "section":
                current_section = (current_section + 1) % len(main_menu)
            else:
                current_key = (current_key + 1) % len(keys)
        elif key in [10,13,32]:
            if mode == "section":
                if main_menu[current_section] == "Exit":
                    break
                mode = "key"
                current_key = 0
            else:
                if keys[current_key] == "Exit":
                    mode = "section"
                    current_key = 0
                else:
                    toggle_value(sec, keys[current_key])

# ----------------------
# MENU PRINCIPAL
# ----------------------
def main(stdscr):
    curses.curs_set(0)
    stdscr.keypad(True)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)

    main_menu = ["Run", "Setup", "Save", "Reset", "Exit"]
    current_selection = 0

    while True:
        stdscr.clear()
        # Bannière
        for i, line in enumerate(BANNER):
            stdscr.addstr(i, 0, line, curses.color_pair(3))

        banner_height = len(BANNER)
        stdscr.addstr(banner_height, 0, "↑/↓ to browse, Enter/Space to select, Escape to exit", curses.color_pair(1))

        # Menu
        for i, item in enumerate(main_menu):
            attr = curses.color_pair(1) | curses.A_REVERSE if i == current_selection else curses.color_pair(2)
            stdscr.addstr(banner_height + 1 + i, 0, "> " + item if i == current_selection else "  " + item, attr)

        tooltip = {
            "Run": "Run Insert-Coin",
            "Setup": "Modify configuration",
            "Save": "Save current configuration",
            "Reset": "Reset configuration to defaults",
            "Exit": "Quit program"
        }.get(main_menu[current_selection], "")
        draw_tooltip(stdscr, tooltip)

        stdscr.refresh()
        key = stdscr.getch()

        if key == 27:
            break
        elif key == curses.KEY_UP:
            current_selection = (current_selection - 1) % len(main_menu)
        elif key == curses.KEY_DOWN:
            current_selection = (current_selection + 1) % len(main_menu)
        elif key in [10,13,32]:
            sel = main_menu[current_selection]
            if sel == "Exit":
                break
            elif sel == "Run":
                curses.endwin()
                subprocess.run(["bash", "run.sh"])
                stdscr = curses.initscr()
                curses.curs_set(0)
                stdscr.keypad(True)
                curses.start_color()
                curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
                curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)
            elif sel == "Setup":
                run_setup_menu(stdscr)
            elif sel == "Save":
                save_config()
            elif sel == "Reset":
                reset_config()

curses.wrapper(main)
