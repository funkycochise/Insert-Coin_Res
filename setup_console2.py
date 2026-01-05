import curses
import configparser
import textwrap
import os
import subprocess

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

NAMES_INI_FILE = "names.ini"

# Valeurs par défaut pour names.ini
NAMES_DEFAULT_CONFIG = {
    "folder": {
        "essential": "_#Essentials",
        "newest": "_#Newest",
        "genre_horizontal": "__Horizontal",
        "genre_vertical": "__Vertical",
        "insertcoin": "_#Insert-Coin",
        "genre_action": "__Action",
        "genre_beat": "__Beat'em up",
        "genre_puzzle": "__Puzzle",
        "genre_sport": "__Sport",
        "genre_vsf": "__Vs Fighting",
        "genre_stg_h": "__STG_H",
        "genre_stg_v": "__STG_V",
        "genre_rng_h": "__Run'n'Gun_H",
        "genre_rng_v": "__Run'n'Gun_V",
        "alpha": "_Alpha",
        "atari": "_Atari",
        "bagman": "_Bagman",
        "bally_midway": "_Bally-midway",
        "capcom": "_Capcom-Mitchell",
        "cps1": "_CPS1",
        "cps15": "_CPS15",
        "cps2": "_CPS2",
        "cave": "_Cave 68000",
        "crazykong": "_Crazy Kong",
        "deco": "_DataEast-Deco",
        "exidy": "_Exidy",
        "galaxian": "_Galaxian",
        "gottlieb": "_Gottlieb",
        "irem": "_Irem",
        "irem62": "_Irem M62",
        "irem72": "_Irem M72",
        "irem90": "_Irem M90",
        "irem92": "_Irem M92",
        "irem92t": "_Irem M92t",
        "irem107": "_Irem M107",
        "jaleco": "_Jaleco",
        "kiwako": "_Kiwako",
        "konami": "_Konami",
        "konamitwin16": "_Konami Twin16",
        "ladybug": "_Ladybug",
        "mcr1": "_MCR1",
        "mcr2": "_MCR2",
        "mcr3": "_MCR3",
        "mcr3mono": "_Midway_MCR3Mono",
        "mcr3scroll": "_Midway_MCR3Scroll",
        "midwayy": "_Midway_YUnit",
        "namco": "_Namco",
        "namco_sys1": "_Namco-System-1",
        "namco_sys86": "_Namco-System-86",
        "neogeo": "_Neo-geo",
        "nichibutsu": "_Nihon Bussan-Nichibutsu",
        "nintendo": "_Nintendo",
        "vs": "_Nintendo Vs.",
        "pacman": "_Pacman",
        "raizing": "_Raizing-8ing",
        "rare": "_Rare",
        "robotron": "_Robotron",
        "scramble": "_Scramble",
        "sega": "_Sega",
        "outrun": "_Sega-Outrun",
        "segasys1": "_Sega-System-1",
        "segasys2": "_Sega-System-2",
        "segasyse": "_Sega-System-E",
        "segasys16": "_Sega-System-16",
        "segasys18": "_Sega-System-18",
        "segastv": "_Sega-Titan Video",
        "snk": "_SNK",
        "si": "_Space Invaders",
        "stern": "_Stern",
        "tad": "_Tad Corp",
        "taito": "_Taito",
        "taitof2": "_Taito-F2",
        "taitosj": "_Taito-SJ",
        "technos": "_Technos",
        "technos16": "_Technos16",
        "tecmo": "_Tehkan-Tecmo",
        "toaplan": "_Toaplan",
        "toaplan_stg": "_Toaplan_STG",
        "universal": "_Universal",
        "upl": "_Upl",
        "williams": "_Williams"
    }
}

# --- Fonction pour créer / compléter setup.ini ---
def ensure_setup_ini():
    parser = configparser.ConfigParser()
    updated = False

    # Lire le fichier existant
    if os.path.exists(INI_FILE):
        parser.read(INI_FILE, encoding="utf-8")

    # Ajouter / compléter les sections et clés par défaut
    for sec, opts in DEFAULT_CONFIG.items():
        if sec not in parser:
            parser[sec] = {}
            updated = True
        for key, val in opts.items():
            if key not in parser[sec]:
                parser[sec][key] = val
                updated = True

    # Réécrire si nécessaire
    if updated or not os.path.exists(INI_FILE):
        with open(INI_FILE, "w", encoding="utf-8") as f:
            parser.write(f)
            
# --- Fonction pour créer / compléter names.ini ---
def ensure_names_ini():
    parser = configparser.ConfigParser()
    updated = False

    # Lire le fichier existant
    if os.path.exists(NAMES_INI_FILE):
        parser.read(NAMES_INI_FILE, encoding="utf-8")

    # Ajouter / compléter les clés par défaut
    for sec, opts in NAMES_DEFAULT_CONFIG.items():
        if sec not in parser:
            parser[sec] = {}
            updated = True
        for key, val in opts.items():
            if key not in parser[sec]:
                parser[sec][key] = val
                updated = True

    # Réécrire si nécessaire
    if updated or not os.path.exists(NAMES_INI_FILE):
        with open(NAMES_INI_FILE, "w", encoding="utf-8") as f:
            parser.write(f)

ensure_setup_ini()
ensure_names_ini()

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
        "psx": "Installs Sony PlayStation core",
        "s32x": "Installs Sega 32X core",
        "saturn": "Installs Sega Saturn core",
        "sgb": "Installs Nintendo Super Game Boy core",
        "neogeo": "Installs SNK Neo Geo core",
        "n64": "Installs Nintendo 64 core",
        "jaguar": "Installs Atari Jaguar core",
        "cdi": "Installs Philips CD-i core",
        "pce": "Installs PC Engine/TurboGrafx-16 core",
        "nes": "Installs Nintendo NES core",
        "snes": "Installs Super Nintendo core",
        "Exit": "Back to main menu"
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
        "stg_h": "Creates Horizontal Shooting Games menu",
        "stg_v": "Creates Vertical Shooting Games menu",
        "vertical": "Creates Vertical Games menu",
        "vsf": "Creates versus Fighting Games menu",
        "rng_h": "Creates Horizontal Run'n'Gun Games menu",
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

# --- Sauvegarde avec section reserved ---
def save_config():
    parser = configparser.ConfigParser()
    
    # Ajout de reserved en premier
    parser["reserved"] = {"version": RESERVED_VERSION}
    
    # Ajout des autres sections
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

# --- Menu Setup séparé ---
def run_setup_menu(stdscr):
    current_section = 0
    current_key = 0
    mode = "section"
    main_menu = sections

    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, "↑/↓ to browse, Enter/Space to toggle, Escape to go back", curses.color_pair(1))

        # Affichage menu
        if mode == "section":
            stdscr.addstr(2, 0, "Select :", curses.color_pair(1))
            for i, sec in enumerate(main_menu):
                if i == current_section:
                    stdscr.addstr(3 + i, 0, "> " + sec, curses.color_pair(1) | curses.A_REVERSE)
                else:
                    stdscr.addstr(3 + i, 0, "  " + sec, curses.color_pair(2))
        else:
            sec = main_menu[current_section]
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
            exit_index = len(keys)
            if current_key == exit_index:
                stdscr.addstr(3 + exit_index, 0, "> Exit", curses.color_pair(1) | curses.A_REVERSE)
            else:
                stdscr.addstr(3 + exit_index, 0, "  Exit", curses.color_pair(2))

        # Tooltip
        tooltip = ""
        if mode == "section":
            tooltip = get_section_tooltip(main_menu[current_section])
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

        # Gestion touches
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
                current_key = (current_key - 1) % (len(config[main_menu[current_section]]) + 1)
        elif key == curses.KEY_DOWN:
            if mode == "section":
                current_section = (current_section + 1) % len(main_menu)
            else:
                current_key = (current_key + 1) % (len(config[main_menu[current_section]]) + 1)
        elif key in [10, 13, 32]:
            if mode == "section":
                mode = "key"
                current_key = 0
            else:
                sec = main_menu[current_section]
                keys = list(config[sec].keys())
                if current_key == len(keys):
                    mode = "section"
                    current_key = 0
                else:
                    toggle_value(sec, keys[current_key])

# --- Menu principal ---
def main(stdscr):
    curses.curs_set(0)
    stdscr.keypad(True)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)

    main_menu = ["Run", "Setup", "Save", "Reset", "Exit"]
    current_selection = 0

    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, "↑/↓ to browse, Enter/Space to select, Escape to exit", curses.color_pair(1))

        for i, item in enumerate(main_menu):
            if i == current_selection:
                stdscr.addstr(2 + i, 0, "> " + item, curses.color_pair(1) | curses.A_REVERSE)
            else:
                stdscr.addstr(2 + i, 0, "  " + item, curses.color_pair(2))

        tooltip = {
            "Run": "Execute run.sh script",
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
        elif key in [10, 13, 32]:
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
