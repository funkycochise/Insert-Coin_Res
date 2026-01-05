import curses
import configparser
import textwrap
import os

INI_FILE = "setup.ini"
IGNORE_SECTIONS = ["reserved", "setup"]

# --- Valeurs par défaut ---
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
        "psx": "0",
        "s32x": "0",
        "saturn": "0",
        "sgb": "0",
        "neogeo": "0",
        "n64": "0",
        "jaguar": "0",
        "cdi": "0",
        "pce": "0",
        "nes": "0",
        "snes": "0"
    },
    "clean": {
        "console_mgl": "0",
        "obsolete_core": "1",
        "remove_other": "0"
    },
    "folder": {
        "essential": "1",
        "rootfolder": "0",
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

# --- Création du fichier INI si inexistant ---
if not os.path.exists(INI_FILE):
    parser = configparser.ConfigParser()
    for sec, opts in DEFAULT_CONFIG.items():
        parser[sec] = opts
    with open(INI_FILE, "w", encoding="utf-8") as f:
        parser.write(f)

# --- Lecture INI et copie en mémoire ---
parser = configparser.ConfigParser()
parser.optionxform = str
parser.read(INI_FILE, encoding="utf-8")
sections = [s for s in parser.sections() if s not in IGNORE_SECTIONS]

# Copie des valeurs dans un dictionnaire modifiable
config = {sec: dict(parser[sec]) for sec in parser.sections() if sec not in IGNORE_SECTIONS}

# --- Tooltips ---
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
        "main_mister": "Installs custom main mister to remove progress bar",
        "mame_rom": "Installs missing mame roms",
        "gnw_rom": "Installs missing Game & Watch roms",
        "additional_res": "Installs additional resources",
        "console_core": "Updates console cores",
        "dualsdram": "Selects single, dual or both SDRAM cores",
        "Exit": "Back to main menu"
    },
    "console": {
        "psx": "Installs Sony PlayStation core ",
        "s32x": "Installs Sega 32X core",
        "saturn": "Installs Sega Saturn core",
        "sgb": "Installs Nintendo Super Game Boy core",
        "neogeo": "Installs SNK Neo Geo core ",
        "n64": "Installs Nintendo 64 core",
        "jaguar": "Installs Atari Jaguar core",
        "cdi": "Installs Philips CD-i core",
        "pce": "Installs PC Engine/TurboGrafx-16 core ",
        "nes": "Installs Nintendo NES core",
        "snes": "Installs Super Nintendo core",
        "Exit": "Back to main menu "
    },
    "clean": {
        "console_mgl": "Removes additional console mgl",
        "obsolete_core": "Removes deprecated cores",
        "remove_other": "Removes other folder",
        "Exit": "Back to main menu"
    },    
    "folder": {
        "console_mgl": "Removes additional console mgl",
        "essential": "Creates menu for essential Titles",
        "rootfolder": "Creates Insert-Coin folder at root",
        "show_system": "Creates System menus",
        "show_genre": "Creates genre menus",
        "manufacturer_subfolder": "Creates manufacturer subfolder",
        "action": "Creates Action Games menu",
        "beat": "Creates Beat'em up Games menu",
        "horizontal": "Creates Horizontal Games menu",
        "newest": "Creates menu for newest Titles",
        "puzzle": "Creates Puzzle Games menu",
        "sport": "Creates Sport Games menu",
        "stg_h": "Creates Horizontal Shooting Games menu ",
        "stg_v": "Creates Vertical Shooting Games menu",
        "vertical": "Creates Vertical Games menu",
        "vsf": "Creates versus Fighting Games menu",
        "rng_h": "Creates Horizontal Run'n'Gun Games menu ",
        "rng_v": "Creates Vertical Run'n'Gun Games menu",        
        "Exit": "Back to main menu"
    }
}

# --- Fonctions pour manipuler les valeurs en mémoire ---
def toggle_value(sec, key):
    val = config[sec][key].strip()
    if key == "dualsdram":
        cycle_dualsdram(sec, key)
    else:
        config[sec][key] = "1" if val == "0" else "0"

def cycle_dualsdram(sec, key):
    val = config[sec][key].strip()
    next_val = {"0": "1", "1": "2", "2": "0"}.get(val, "0")
    config[sec][key] = next_val

def save_config():
    parser = configparser.ConfigParser()
    for sec, opts in config.items():
        parser[sec] = opts
    with open(INI_FILE, "w", encoding="utf-8") as f:
        parser.write(f)

def reset_config():
    global config
    config = {sec: dict(opts) for sec, opts in DEFAULT_CONFIG.items() if sec in sections}

# --- Tooltips ---
def get_section_tooltip(sec):
    return SECTION_TOOLTIPS.get(sec, "")

def get_key_tooltip(sec, key):
    if key == "Exit":
        return "Retour au menu principal"
    return KEY_TOOLTIPS.get(sec, {}).get(key, "")

def draw_tooltip(stdscr, text):
    if not text:
        return
    h, w = stdscr.getmaxyx()
    lines = textwrap.wrap(text, w - 2)
    y = h - len(lines) - 2
    stdscr.hline(y, 0, curses.ACS_HLINE, w)
    for i, line in enumerate(lines):
        stdscr.addstr(y + 1 + i, 1, line, curses.color_pair(1))

# --- Programme principal ---
def main(stdscr):
    curses.curs_set(0)
    stdscr.keypad(True)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)

    # Menu principal : ajout de Save et Reset
    main_menu = sections + ["Save", "Reset", "Exit"]

    current_section = 0
    current_key = 0
    mode = "section"

    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, "↑/↓ to browse, Enter/Space to toggle, Escape to exit", curses.color_pair(1))
        #stdscr.addstr(1, 0,"ligne 2", curses.color_pair(1))

        # --- Affichage menu ---
        if mode == "section":
            stdscr.addstr(2, 0, "Select :", curses.color_pair(1))
            for i, sec in enumerate(main_menu):
                if i == current_section:
                    stdscr.addstr(3 + i, 0, "> " + sec, curses.color_pair(1) | curses.A_REVERSE)
                else:
                    stdscr.addstr(3 + i, 0, "  " + sec, curses.color_pair(2))
        else:
            sec = main_menu[current_section]
            if sec in config:
                keys = list(config[sec].keys())
                stdscr.addstr(2, 0, f"Select option in [{sec}] :", curses.color_pair(1))
                for i, k in enumerate(keys):
                    val = config[sec][k]
                    if k == "dualsdram":
                        desc = DUALSDRAM_DESC.get(val, "")
                        line = f"{k} = {val} ({desc})"
                    else:
                        line = f"{k} = {val}"
                    if i == current_key:
                        stdscr.addstr(3 + i, 0, "> " + line, curses.color_pair(1) | curses.A_REVERSE)
                    else:
                        stdscr.addstr(3 + i, 0, "  " + line, curses.color_pair(2))
                # Ajouter Exit pour revenir au menu principal
                exit_index = len(keys)
                if current_key == exit_index:
                    stdscr.addstr(3 + exit_index, 0, "> Exit", curses.color_pair(1) | curses.A_REVERSE)
                else:
                    stdscr.addstr(3 + exit_index, 0, "  Exit", curses.color_pair(2))

        # --- Affichage tooltip ---
        tooltip = ""
        if mode == "section":
            sec_name = main_menu[current_section]
            tooltip = get_section_tooltip(sec_name) if sec_name in SECTION_TOOLTIPS else ""
        else:
            sec = main_menu[current_section]
            keys = list(config[sec].keys())
            if current_key < len(keys):
                tooltip = get_key_tooltip(sec, keys[current_key])
            else:
                tooltip = "Back to main menu"
        draw_tooltip(stdscr, tooltip)

        stdscr.refresh()
        key = stdscr.getch()

        # --- Gestion des touches ---
        if key == 27:  # Échap
            if mode == "key":
                mode = "section"
                current_key = 0
            else:
                break
        elif key == curses.KEY_UP:
            if mode == "section":
                current_section = (current_section - 1) % len(main_menu)
            elif mode == "key":
                sec = main_menu[current_section]
                keys = list(config[sec].keys())
                current_key = (current_key - 1) % (len(keys) + 1)
        elif key == curses.KEY_DOWN:
            if mode == "section":
                current_section = (current_section + 1) % len(main_menu)
            elif mode == "key":
                sec = main_menu[current_section]
                keys = list(config[sec].keys())
                current_key = (current_key + 1) % (len(keys) + 1)
        elif key in [10, 13, 32]:  # Entrée ou Espace
            if mode == "section":
                sel = main_menu[current_section]
                if sel == "Exit":
                    break
                elif sel == "Save":
                    save_config()
                elif sel == "Reset":
                    reset_config()
                else:
                    mode = "key"
                    current_key = 0
            else:
                sec = main_menu[current_section]
                keys = list(config[sec].keys())
                if current_key == len(keys):
                    mode = "section"
                    current_key = 0
                else:
                    k = keys[current_key]
                    toggle_value(sec, k)

curses.wrapper(main)
