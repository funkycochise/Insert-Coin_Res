import curses
import os

RES_INDEX_FILE = "res_index.txt"
RES_INDEX_URL = "https://raw.githubusercontent.com/funkycochise/Insert-Coin_Res/main/res_index.txt"

# --- Téléchargement automatique si absent ---
def ensure_res_index():
    if os.path.exists(RES_INDEX_FILE):
        return True
    print("Téléchargement de res_index.txt ...")
    os.system(
        f"wget -q -O {RES_INDEX_FILE} {RES_INDEX_URL} "
        f"|| curl -s -o {RES_INDEX_FILE} {RES_INDEX_URL}"
    )
    return os.path.exists(RES_INDEX_FILE)

# --- Viewer minimal avec scroll + PageUp/PageDown + Home/End ---
def view_file(stdscr, filename, page_size=10):
    if not os.path.exists(filename):
        stdscr.addstr(0, 0, f"File not found: {filename}")
        stdscr.getch()
        return

    with open(filename, "r", encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()

    pos = 0
    stdscr.keypad(True)

    while True:
        stdscr.clear()
        h, w = stdscr.getmaxyx()
        y = 0

        # Affichage des lignes visibles
        for i in range(pos, min(pos + h - 1, len(lines))):
            stdscr.addstr(y, 0, lines[i].rstrip()[:w-1])
            y += 1

        # Footer
        stdscr.addstr(h-1, 0, f"↑↓ scroll  PgUp/PgDn {page_size} lines  Home/End start/end  ESC back")
        stdscr.refresh()

        k = stdscr.getch()
        if k == 27:  # ESC
            break
        elif k == curses.KEY_UP:
            pos = max(0, pos - 1)
        elif k == curses.KEY_DOWN:
            pos = min(len(lines) - 1, pos + 1)
        elif k == curses.KEY_NPAGE:  # Page Down
            pos = min(len(lines) - 1, pos + page_size)
        elif k == curses.KEY_PPAGE:  # Page Up
            pos = max(0, pos - page_size)
        elif k == curses.KEY_HOME:  # Home
            pos = 0
        elif k == curses.KEY_END:   # End
            pos = max(0, len(lines) - 1)

# --- Main test ---
if ensure_res_index():
    curses.wrapper(lambda stdscr: view_file(stdscr, RES_INDEX_FILE, page_size=10))
