import curses
import configparser
import textwrap
import os

INI_FILE = "setup.ini"
IGNORE_SECTIONS = ["reserved", "setup"]  # Ne pas afficher ces sections

# --- Création du fichier INI par défaut si inexistant ---
if not os.path.exists(INI_FILE):
    parser = configparser.ConfigParser()

    # Section update
    parser["update"] = {
        "main_mister": "0",
        "mame_rom": "1",
        "gnw_rom": "1",
        "additional_res": "0",
        "console_core": "0",
        "dualsdram": "0"
    }

    # Section console
    parser["console"] = {
        "psx": "1",
        "s32x": "0",
        "saturn": "1",
        "sgb": "0",
        "neogeo": "1",
        "n64": "1",
        "jaguar": "1",
        "cdi": "1",
        "pce": "1",
        "nes": "1",
        "snes": "1"
    }

    # Section clean
    parser["clean"] = {
        "console_mgl": "0",
        "obsolete_core": "1",
        "remove_other": "0"
    }

    # Section folder
    parser["folder"] = {
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

    # Écriture du fichier
    with open(INI_FILE, "w", encoding="utf-8") as f:
        parser.write(f)

# --- Lecture du fichier INI ---
parser = configparser.ConfigParser()
parser.optionxform = str
parser.read(INI_FILE, encoding="utf-8")
sections = [s for s in parser.sections() if s not in IGNORE_SECTIONS]

# --- Constantes ---
DUALSDRAM_DESC = {
    "0": "single SDRAM core",
    "1": "Dual SDRAM core",
    "2": "Both Single and Dual SDRAM cores"
}

SECTION_TOOLTIPS = {
    "update": "Options de mise à jour et configuration des cores",
    "console": "Paramètres liés aux cores consoles",
    "clean": "Supprime ou nettoie des fichiers temporaires ou inutiles",
    "folder": "Configuration des dossiers à afficher",
    "Exit": "Quitter le menu"
}

KEY_TOOLTIPS = {
    "update": {
        "main_mister": "Installs custom main mister to remove progress bar",
        "mame_rom": "Installs missing mame roms",
        "gnw_rom": "Installs missing Game & Watch roms",
        "additional_res": "Installs additional resources",
        "console_core": "Updates console cores",
        "dualsdram": "Selects single, dual or both SDRAM cores"
    },
    "console": {
        "psx": "PlayStation",
        "s32x": "Sega 32X",
        "saturn": "Sega Saturn",
        "sgb": "Super Game Boy",
        "neogeo": "Neo Geo",
        "n64": "Nintendo 64",
        "jaguar": "Atari Jaguar",
        "cdi": "Philips CD-i",
        "pce": "PC Engine / TurboGrafx-16",
        "nes": "Nintendo Entertainment System",
        "snes": "Super Nintendo"
    },
    "clean": {
        "console_mgl": "Supprime les fichiers MGL obsolètes",
        "obsolete_core": "Supprime les cores obsolètes",
        "remove_other": "Supprime les autres fichiers inutiles"
    },
    "folder": {
        "essential": "Dossier essentiel à afficher",
        "rootfolder": "Afficher le dossier racine",
        "show_system": "Afficher le système",
        "show_genre": "Afficher par genre",
        "manufacturer_subfolder": "Sous-dossier fabricant",
        "action": "Afficher les jeux action",
        "beat": "Afficher les jeux beat 'em up",
        "horizontal": "Afficher les jeux horizontal",
        "newest": "Afficher les derniers jeux",
        "puzzle": "Afficher les jeux puzzle",
        "sport": "Afficher les jeux sport",
        "stg_h": "Jeux shoot horizontal",
        "stg_v": "Jeux shoot vertical",
        "vertical": "Jeux vertical",
        "vsf": "Jeux VS Fighting",
        "rng_h": "Jeux racing horizontal",
        "rng_v": "Jeux racing vertical"
    }
}

# --- Fonctions ---
def toggle_value(section, key):
    val = parser[section][key].strip()
    parser[section][key] = "1" if val == "0" else "0"
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

def get_section_tooltip(section):
    return SECTION_TOOLTIPS.get(section, "")

def get_key_tooltip(section, key):
    if key == "Exit":
        return "Retour au menu principal"
    return KEY_TOOLTIPS.get(section, {}).get(key, "")

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

    current_section = 0
    current_key = 0
    mode = "section"

    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, "↑/↓ naviguer, Entrée toggle/cycle dualsdram, Échap pour quitter", curses.color_pair(1))

        # --- Affichage menu ---
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
        else:  # mode == "key"
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

        # --- Affichage tooltip ---
        tooltip = ""
        if mode == "section":
            sec_name = sections[current_section] if current_section < len(sections) else "Exit"
            tooltip = get_section_tooltip(sec_name)
        elif mode == "key":
            sec = sections[current_section]
            keys = list(parser[sec].keys())
            if current_key < len(keys):
                tooltip = get_key_tooltip(sec, keys[current_key])
            else:  # Exit
                tooltip = get_key_tooltip(sec, "Exit")
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
        elif key in [10, 13, 32]:  # Entrée ou Espace (32 = code ASCII espace)
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
