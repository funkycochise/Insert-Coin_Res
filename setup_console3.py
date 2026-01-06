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
NAMES_INI_FILE = "names.ini"
IGNORE_SECTIONS = ["reserved", "setup"]
RESERVED_VERSION = "1.0"

# --- Valeurs par défaut ---
DEFAULT_CONFIG = {
    "update": {"main_mister": "0","mame_rom": "0","gnw_rom": "0","additional_res": "0","console_core": "0","dualsdram": "0"},
    "console": {"psx": "0","s32x": "0","saturn": "0","sgb": "0","neogeo": "0","n64": "0","jaguar": "0","cdi": "0","pce": "0","nes": "0","snes": "0"},
    "clean": {"console_mgl": "0","obsolete_core": "1","remove_other": "0"},
    "folder": {"essential": "1","rootfolder": "0","show_system": "1","show_genre": "1","manufacturer_subfolder": "0","action": "1","beat": "1","horizontal": "1","newest": "1","puzzle": "1","sport": "1","stg_h": "1","stg_v": "1","vertical": "1","vsf": "1","rng_h": "1","rng_v": "1"}
}

DUALSDRAM_DESC = {"0": "single SDRAM core", "1": "Dual SDRAM core", "2": "Both Single and Dual SDRAM cores"}

SECTION_TOOLTIPS = {
    "update": "Settings for Update",
    "console": "Settings for Console Cores",
    "clean": "Settings for Cleaning for obsolete cores and useless files",
    "folder": "Settings for Folders to display"
}

KEY_TOOLTIPS = {
    "update": {"main_mister": "Installs custom main mister to remove progress bar",
               "mame_rom": "Installs missing mame roms",
               "gnw_rom": "Installs missing Game & Watch roms",
               "additional_res": "Installs additional resources",
               "console_core": "Updates console cores",
               "dualsdram": "Selects single, dual or both SDRAM cores"},
    "console": {"psx": "Installs Sony PlayStation core",
                "s32x": "Installs Sega 32X core",
                "saturn": "Installs Sega Saturn core",
                "sgb": "Installs Nintendo Super Game Boy core",
                "neogeo": "Installs SNK Neo Geo core",
                "n64": "Installs Nintendo 64 core",
                "jaguar": "Installs Atari Jaguar core",
                "cdi": "Installs Philips CD-i core",
                "pce": "Installs PC Engine/TurboGrafx-16 core",
                "nes": "Installs Nintendo NES core",
                "snes": "Installs Super Nintendo core"},
    "clean": {"console_mgl": "Removes additional console mgl",
              "obsolete_core": "Removes deprecated cores",
              "remove_other": "Removes other folder"},
    "folder": {}  # On peut ajouter plus tard
}

# --- Fonctions INI ---
def ensure_ini(filename, default_config):
    parser = configparser.ConfigParser()
    updated = False

    if os.path.exists(filename):
        parser.read(filename, encoding="utf-8")

    for sec, opts in default_config.items():
        if sec not in parser:
            parser[sec] = {}
            updated = True
        for key, val in opts.items():
            if key not in parser[sec]:
                parser[sec][key] = val
                updated = True

    if updated or not os.path.exists(filename):
        with open(filename, "w", encoding="utf-8") as f:
            parser.write(f)

# --- Initialisation des fichiers ---
ensure_ini(INI_FILE, DEFAULT_CONFIG)

# --- Lecture setup.ini ---
parser = configparser.ConfigParser()
parser.optionxform = str
parser.read(INI_FILE, encoding="utf-8")
sections = [s for s in parser.sections() if s not in IGNORE_SECTIONS]
config = {sec: dict(parser[sec]) for sec in sections}

# --- Fonctions ---
def toggle_value(sec, key):
    val = config[sec][key].strip()
    if key == "dualsdram":
        config[sec][key] = {"0":"1","1":"2","2":"0"}.get(val,"0")
    else:
        config[sec][key] = "1" if val == "0" else "0"

def save_config():
    parser = configparser.ConfigParser()
    parser["reserved"] = {"version": RESERVED_VERSION}
    for sec, opts in config.items():
        parser[sec] = opts
    with open(INI_FILE, "w", encoding="utf-8") as f:
        parser.write(f)

def reset_config():
    global config
    config = {sec: dict(opts) for sec, opts in DEFAULT_CONFIG.items() if sec in sections}

def get_section_tooltip(sec):
    return SECTION_TOOLTIPS.get(sec, "")

def get_key_tooltip(sec, key):
    if key == "Exit":
        return "Back to menu"
    return KEY_TOOLTIPS.get(sec, {}).get(key, "")

def draw_tooltip(stdscr, text):
    if not text:
        return
    h, w = stdscr.getmaxyx()
    lines = textwrap.wrap(text, w-2)
    y = h - len(lines) - 2
    stdscr.hline(y, 0, curses.ACS_HLINE, w)
    for i, line in enumerate(lines):
        stdscr.addstr(y+1+i, 1, line, curses.color_pair(1))

# --- Menu Setup ---
def run_setup_menu(stdscr):
    current_section = 0
    current_key = 0
    mode = "section"
    main_menu = sections + ["Exit"]  # <-- Exit ajouté ici

    while True:
        stdscr.clear()
        stdscr.addstr(0,0,"↑/↓ browse, Enter/Space toggle, Esc back", curses.color_pair(1))

        if mode == "section":
            stdscr.addstr(2,0,"Select section:", curses.color_pair(1))
            for i, sec in enumerate(main_menu):
                style = curses.A_REVERSE if i==current_section else 0
                stdscr.addstr(3+i, 0, "> "+sec if i==current_section else "  "+sec, curses.color_pair(1)|style if i==current_section else curses.color_pair(2))
            tooltip = get_section_tooltip(main_menu[current_section])
        else:
            sec = main_menu[current_section]
            keys = list(config.get(sec, {}).keys()) + ["Exit"]
            stdscr.addstr(2,0,f"Options in [{sec}]:", curses.color_pair(1))
            for i,k in enumerate(keys):
                if k=="Exit":
                    line="Exit"
                elif k=="dualsdram":
                    val=config[sec][k]
                    line=f"{k} = {val} ({DUALSDRAM_DESC.get(val,'')})"
                else:
                    line=f"{k} = {config[sec][k]}"
                style = curses.A_REVERSE if i==current_key else 0
                stdscr.addstr(3+i,0,"> "+line if i==current_key else "  "+line, curses.color_pair(1)|style if i==current_key else curses.color_pair(2))
            tooltip = "Back to menu" if keys[current_key]=="Exit" else get_key_tooltip(sec, keys[current_key])

        draw_tooltip(stdscr, tooltip)
        stdscr.refresh()
        key = stdscr.getch()

        if key==27:  # Esc
            if mode=="key":
                mode="section"; current_key=0
            else:
                break
        elif key==curses.KEY_UP:
            if mode=="section": current_section=(current_section-1)%len(main_menu)
            else: current_key=(current_key-1)%len(keys)
        elif key==curses.KEY_DOWN:
            if mode=="section": current_section=(current_section+1)%len(main_menu)
            else: current_key=(current_key+1)%len(keys)
        elif key in [10,13,32]:
            if mode=="section":
                mode="key"; current_key=0
            else:
                if keys[current_key]=="Exit":
                    mode="section"; current_key=0
                else:
                    toggle_value(sec, keys[current_key])

# --- Menu Principal ---
def main(stdscr):
    curses.curs_set(0)
    stdscr.keypad(True)
    curses.start_color()
    curses.init_pair(1,curses.COLOR_CYAN,curses.COLOR_BLACK)
    curses.init_pair(2,curses.COLOR_CYAN,curses.COLOR_BLACK)
    curses.init_pair(3,curses.COLOR_RED,curses.COLOR_BLACK)

    main_menu=["Run","Setup","Save","Reset","Exit"]
    current_selection=0

    while True:
        stdscr.clear()
        banner_height=len(BANNER)
        for i,line in enumerate(BANNER):
            stdscr.addstr(i,0,line,curses.color_pair(3))
        stdscr.addstr(banner_height,0,"↑/↓ browse, Enter/Space select, Esc exit",curses.color_pair(1))

        for i,item in enumerate(main_menu):
            style=curses.A_REVERSE if i==current_selection else 0
            stdscr.addstr(banner_height+1+i,0,"> "+item if i==current_selection else "  "+item,curses.color_pair(1)|style if i==current_selection else curses.color_pair(2))

        tooltip={"Run":"Run Insert-Coin","Setup":"Modify configuration","Save":"Save current config","Reset":"Reset config","Exit":"Quit program"}.get(main_menu[current_selection],"")
        draw_tooltip(stdscr,tooltip)
        stdscr.refresh()
        key=stdscr.getch()

        if key==27: break
        elif key==curses.KEY_UP: current_selection=(current_selection-1)%len(main_menu)
        elif key==curses.KEY_DOWN: current_selection=(current_selection+1)%len(main_menu)
        elif key in [10,13,32]:
            sel=main_menu[current_selection]
            if sel=="Exit": break
            elif sel=="Run":
                curses.endwin()
                subprocess.run(["bash","run.sh"])
                stdscr=curses.initscr()
                curses.curs_set(0)
                stdscr.keypad(True)
                curses.start_color()
                curses.init_pair(1,curses.COLOR_CYAN,curses.COLOR_BLACK)
                curses.init_pair(2,curses.COLOR_CYAN,curses.COLOR_BLACK)
            elif sel=="Setup":
                run_setup_menu(stdscr)
            elif sel=="Save":
                save_config()
            elif sel=="Reset":
                reset_config()

curses.wrapper(main)
