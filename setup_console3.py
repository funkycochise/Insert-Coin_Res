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
IGNORE_SECTIONS = ["setup"]

#RUN_CMD = ["bash", "run.sh"]
RUN_CMD = None

# --- Valeurs par défaut ---
DEFAULT_CONFIG = {
    "update": {"main_mister": "0","mame_rom": "0","gnw_rom": "0","additional_res": "0","console_core": "0","dualsdram": "0"},
    "console": {"psx": "0","s32x": "0","saturn": "0","sgb": "0","neogeo": "0","n64": "0","jaguar": "0","cdi": "0","pce": "0","nes": "0","snes": "0"},
    "clean": {"console_mgl": "0","obsolete_core": "0","remove_other": "0"},
    "folder": {"essential": "1","rootfolder": "0","show_system": "1","show_genre": "1","manufacturer_subfolder": "0","action": "1","beat": "1","horizontal": "1","newest": "1","puzzle": "1","sport": "1","stg_h": "1","stg_v": "1","vertical": "1","vsf": "1","rng_h": "1","rng_v": "1"}
}

# --- Valeurs par défaut pour names.ini ---
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



DUALSDRAM_DESC = {"0": "single SDRAM core", "1": "Dual SDRAM core", "2": "Both Single and Dual SDRAM cores"}

SECTION_TOOLTIPS = {
    "update": "Settings for Update",
    "console": "Settings for Console Cores",
    "clean": "Settings for Cleaning obsolete cores and useless files",
    "folder": "Settings for folders to create"
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
    "folder": {
    "essential": "Generate essential games folder",
    "rootfolder": "Generate Insert-Coin folder at root intead of _Arcade",
    "show_system": "Generate separate folders for systems",
    "show_genre": "Generate folders by genre",
    "manufacturer_subfolder": "Generate subfolders by manufacturer",
    "action": "Generate action game folder",
    "beat": "Generate beat'em up game folder",
    "horizontal": "Generate horizontal game folder",
    "newest": "Generate newest game folder",
    "puzzle": "Generate puzzle game folder",
    "sport": "Generate sports game folder",
    "stg_h": "Generate horizontal STG game folder",
    "stg_v": "Generate vertical STG game folder",
    "vertical": "Generate vertical game folder",
    "vsf": "Generate VS fighting game folder",
    "rng_h": "Generate horizontal run'n'gun game folder",
    "rng_v": "Generate vertical run'n'gun game folder"
}
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
ensure_ini(NAMES_INI_FILE, NAMES_DEFAULT_CONFIG)  # <-- même traitement que setup.ini

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
        stdscr.addstr(0,0,"↑/↓ browse, Enter/Space toggle, Esc exit", curses.color_pair(1))

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
            if mode == "section":
                if main_menu[current_section] == "Exit":
                    return              # sortir du Setup
                    mode = "key"
                    current_key = 0
                else:
                    if keys[current_key] == "Exit":
                        mode = "section"    # retour aux sections
                        current_key = 0
                    else:
                        toggle_value(sec, keys[current_key])
                        
def do_run():
    curses.endwin()
    if RUN_CMD:
        subprocess.run(RUN_CMD)
    else:
        print("Run simulé !")
    return
    
# --- Menu Principal ---
def main(stdscr):
    curses.curs_set(0)
    stdscr.keypad(True)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)

    main_menu = ["Run", "Setup", "Save", "Reset", "Exit"]
    current_selection = 0  # Run par défaut

    countdown = 5  # secondes avant Run auto
    stdscr.timeout(1000)  # 1000 ms = 1 seconde par tick

    while True:
        stdscr.clear()
        banner_height = len(BANNER)
        for i, line in enumerate(BANNER):
            stdscr.addstr(i, 0, line, curses.color_pair(3))
        stdscr.addstr(banner_height, 0, "↑/↓ browse, Enter/Space select, Esc exit", curses.color_pair(1))

        # Affiche le menu
        for i, item in enumerate(main_menu):
            style = curses.A_REVERSE if i == current_selection else 0
            stdscr.addstr(banner_height + 1 + i, 0,
                          "> " + item if i == current_selection else "  " + item,
                          curses.color_pair(1) | style if i == current_selection else curses.color_pair(2))

        # Affiche le countdown en bas
        h, w = stdscr.getmaxyx()
        stdscr.addstr(h - 1, 0, f"AutoRun in {countdown} sec : Any arrow key to abort", curses.color_pair(1))
        stdscr.refresh()

        key = stdscr.getch()

        # Si aucune touche → countdown
        if key == -1:
            countdown -= 1
            if countdown <= 0:
                # Timeout atteint → exécution Run
                do_run()
                return
                
            continue  # prochaine seconde
        else:
            stdscr.timeout(-1)  # remettre mode bloquant après appui
            # Navigation classique
            if key == 27:  # ESC
                break
            elif key == curses.KEY_UP:
                current_selection = (current_selection - 1) % len(main_menu)
            elif key == curses.KEY_DOWN:
                current_selection = (current_selection + 1) % len(main_menu)
            elif key in [10, 13, 32]:  # Enter / Space
                sel = main_menu[current_selection]
                if sel == "Exit":
                    break
                elif sel == "Run":
                    curses.endwin()
                    do_run()
                    return                    
                elif sel == "Setup":
                    run_setup_menu(stdscr)
                elif sel == "Save":
                    save_config()
                elif sel == "Reset":
                    reset_config()
            # Reset countdown si utilisateur navigue
            countdown = 5
curses.wrapper(main)
