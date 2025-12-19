#!/usr/bin/env python3
import curses
import configparser
import os
import subprocess
import textwrap
import sys
import platform

# =========================
# CONFIG
# =========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INI_FILE = os.path.join(BASE_DIR, "setup.ini")
RUN_SCRIPT = os.path.join(BASE_DIR, "run.sh")
KEY_CONFIRM = (10, 13, 32)
KEY_ESCAPE = 27
IGNORE_SECTIONS = ["reserved", "setup"]

# Default configuration
DEFAULT_CONFIG = {
    "update": {"main_mister": "0", "mame_rom": "0", "gnw_rom": "0", "additional_res": "0", "console_core": "0", "dualsdram": "0"},
    "console": {"psx": "0","s32x":"0","saturn":"0","sgb":"0","neogeo":"0","n64":"0","jaguar":"0","cdi":"0","pce":"0","nes":"0","snes":"0"},
    "clean": {"console_mgl": "0", "obsolete_core": "1", "remove_other": "0"},
    "folder": {"essential": "1","rootfolder":"0","show_system":"1","show_genre":"1","manufacturer_subfolder":"0",
               "action":"1","beat":"1","horizontal":"1","newest":"1","puzzle":"1","sport":"1","stg_h":"1","stg_v":"1",
               "vertical":"1","vsf":"1","rng_h":"1","rng_v":"1"}
}

DUALSDRAM_DESC = {"0": "single SDRAM core", "1": "Dual SDRAM core", "2": "Both Single and Dual SDRAM cores"}

# =========================
# INITIALIZATION
# =========================
if not os.path.exists(INI_FILE):
    parser = configparser.ConfigParser()
    for sec, opts in DEFAULT_CONFIG.items():
        parser[sec] = opts
    with open(INI_FILE, "w", encoding="utf-8") as f:
        parser.write(f)

parser = configparser.ConfigParser()
parser.optionxform = str
parser.read(INI_FILE, encoding="utf-8")
sections = [s for s in parser.sections() if s not in IGNORE_SECTIONS]
config = {sec: dict(parser[sec]) for sec in parser.sections() if sec not in IGNORE_SECTIONS}

# =========================
# CONFIG FUNCTIONS
# =========================
def toggle_value(sec, key):
    val = config[sec][key].strip()
    if key == "dualsdram":
        cycle_dualsdram(sec, key)
    else:
        config[sec][key] = "1" if val == "0" else "0"

def cycle_dualsdram(sec, key):
    val = config[sec][key].strip()
    next_val = {"0":"1","1":"2","2":"0"}.get(val,"0")
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

def draw_tooltip(stdscr,text):
    if not text: return
    h, w = stdscr.getmaxyx()
    lines = textwrap.wrap(text, w-2)
    y = h - len(lines) - 2
    stdscr.hline(y,0,curses.ACS_HLINE,w)
    for i,line in enumerate(lines):
        stdscr.addstr(y+1+i,1,line,curses.color_pair(1))

# =========================
# SETUP MODE
# =========================
def run_setup(stdscr):
    curses.curs_set(0)
    stdscr.keypad(True)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)

    main_menu = sections + ["Save", "Reset", "Exit"]
    current_section = 0
    current_key = 0
    mode = "section"

    while True:
        stdscr.clear()
        stdscr.addstr(0,0,"↑/↓ navigate | Enter/Space toggle | ESC quit",curses.color_pair(1))

        if mode=="section":
            stdscr.addstr(2,0,"Select :",curses.color_pair(1))
            for i,sec in enumerate(main_menu):
                attr = curses.color_pair(1)|curses.A_REVERSE if i==current_section else curses.color_pair(2)
                stdscr.addstr(3+i,0,("> "+sec) if i==current_section else ("  "+sec),attr)
        else:
            sec = main_menu[current_section]
            if sec in config:
                keys = list(config[sec].keys())
                stdscr.addstr(2,0,f"Select option in [{sec}] :",curses.color_pair(1))
                for i,k in enumerate(keys):
                    val = config[sec][k]
                    line = f"{k} = {val} ({DUALSDRAM_DESC[val]})" if k=="dualsdram" else f"{k} = {val}"
                    attr = curses.color_pair(1)|curses.A_REVERSE if i==current_key else curses.color_pair(2)
                    stdscr.addstr(3+i,0,("> "+line) if i==current_key else ("  "+line),attr)
                exit_index = len(keys)
                attr = curses.color_pair(1)|curses.A_REVERSE if current_key==exit_index else curses.color_pair(2)
                stdscr.addstr(3+exit_index,0,("> Exit") if current_key==exit_index else "  Exit",attr)

        draw_tooltip(stdscr,"")
        stdscr.refresh()
        key = stdscr.getch()

        if key==KEY_ESCAPE:
            if mode=="key":
                mode="section"
                current_key=0
            else:
                break
        elif key==curses.KEY_UP:
            if mode=="section":
                current_section=(current_section-1)%len(main_menu)
            else:
                sec=main_menu[current_section]
                keys=list(config[sec].keys())
                current_key=(current_key-1)%(len(keys)+1)
        elif key==curses.KEY_DOWN:
            if mode=="section":
                current_section=(current_section+1)%len(main_menu)
            else:
                sec=main_menu[current_section]
                keys=list(config[sec].keys())
                current_key=(current_key+1)%(len(keys)+1)
        elif key in KEY_CONFIRM:
            if mode=="section":
                sel = main_menu[current_section]
                if sel=="Exit":
                    break
                elif sel=="Save":
                    save_config()
                elif sel=="Reset":
                    reset_config()
                else:
                    mode="key"
                    current_key=0
            else:
                sec = main_menu[current_section]
                keys=list(config[sec].keys())
                if current_key==len(keys):
                    mode="section"
                    current_key=0
                else:
                    toggle_value(sec,keys[current_key])

# =========================
# RUN MODE
# =========================
def run_script(stdscr):
    curses.endwin()  # restore terminal
    print("Launching run.sh...")
    # Check if on Windows
    if platform.system() == "Windows":
        print("Run.sh cannot be executed on Windows. Use WSL or Git Bash.")
    else:
        if os.path.exists(RUN_SCRIPT):
            try:
                subprocess.run(["bash", RUN_SCRIPT], check=True)
            except subprocess.CalledProcessError as e:
                print("Error running run.sh:", e)
        else:
            print("run.sh not found.")
    input("Press Enter to return...")
    # When done, the wrapper will continue and menu is displayed again

# =========================
# MAIN MENU
# =========================
def main(stdscr):
    curses.curs_set(0)
    stdscr.keypad(True)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)

    menu = ["Setup","Run","Exit"]
    current=0
    while True:
        stdscr.clear()
        stdscr.addstr(0,0,"Insert-Coin",curses.color_pair(1) | curses.A_BOLD)
        stdscr.addstr(1,0,"↑/↓ navigate | Enter/Space select | ESC quit", curses.color_pair(1))
        for i,item in enumerate(menu):
            attr = curses.color_pair(1)|curses.A_REVERSE if i==current else curses.color_pair(2)
            stdscr.addstr(3+i,2,item,attr)
        key = stdscr.getch()
        if key==curses.KEY_UP:
            current=(current-1)%len(menu)
        elif key==curses.KEY_DOWN:
            current=(current+1)%len(menu)
        elif key in KEY_CONFIRM:
            if menu[current]=="Exit":
                break
            elif menu[current]=="Setup":
                run_setup(stdscr)
            elif menu[current]=="Run":
                run_script(stdscr)
        elif key==KEY_ESCAPE:
            break

# =========================
# ENTRY POINT
# =========================
if __name__=="__main__":
    curses.wrapper(main)
