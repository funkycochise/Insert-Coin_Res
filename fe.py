import os
import tkinter as tk
import subprocess
import cv2
from PIL import Image, ImageTk

# ---------------- Liste des jeux en dur ----------------
games = [
    {"name": "Game 1", "cmd": "echo Lancement Game 1", "preview": "preview1.mp4"},
    {"name": "Game 2", "cmd": "echo Lancement Game 2", "preview": "preview2.mp4"},
    {"name": "Game 3", "cmd": "echo Lancement Game 3", "preview": "preview3.mp4"},
]

# ---------------- Variables globales ----------------
cap = None  # pour la vidéo

# ---------------- Lancer le jeu ----------------
def launch_game():
    index = game_listbox.curselection()
    if not index:
        return
    game = games[index[0]]
    subprocess.Popen(game["cmd"], shell=True)

# ---------------- Lecture vidéo preview ----------------
def play_preview():
    global cap
    index = game_listbox.curselection()
    if not index:
        return
    game = games[index[0]]
    preview_path = game.get("preview")
    if not preview_path or not os.path.exists(preview_path):
        label_preview.config(image='', text="Pas de preview")
        cap = None
        return
    if cap is not None:
        cap.release()
    cap = cv2.VideoCapture(preview_path)
    update_frame()

def update_frame():
    global cap
    if cap is None:
        return
    ret, frame = cap.read()
    if ret:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = ImageTk.PhotoImage(Image.fromarray(frame).resize((frame_right.winfo_width(), frame_right.winfo_height())))
        label_preview.config(image=img, text='')
        label_preview.image = img
        root.after(30, update_frame)
    else:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # boucle

# ---------------- Navigation clavier ----------------
def on_key(event):
    index = game_listbox.curselection()
    index = index[0] if index else 0

    if event.keysym == 'Up':
        index = max(0, index - 1)
    elif event.keysym == 'Down':
        index = min(game_listbox.size() - 1, index + 1)
    elif event.keysym == 'Return':
        launch_game()
        return

    game_listbox.selection_clear(0, tk.END)
    game_listbox.selection_set(index)
    game_listbox.activate(index)
    play_preview()

# ---------------- Quitter avec Esc ----------------
def quit_launcher(event=None):
    global cap
    if cap is not None:
        cap.release()
    root.destroy()

# ---------------- GUI ----------------
root = tk.Tk()
root.title("Launcher TeknoParrot Prototype")

# Plein écran
root.attributes('-fullscreen', True)
root.configure(bg='black')

# Bind clavier
root.bind('<Key>', on_key)
root.bind('<Escape>', quit_launcher)

# Frames
frame_left = tk.Frame(root, bg='black')
frame_left.pack(side=tk.LEFT, fill=tk.Y, padx=20, pady=20)

frame_right = tk.Frame(root, bg='black')
frame_right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=20, pady=20)

# Liste des jeux
game_listbox = tk.Listbox(frame_left, width=40, font=("Arial", 24), bg='black', fg='white', selectbackground='blue', selectforeground='white')
game_listbox.pack(fill=tk.Y, expand=True)

# Label preview
label_preview = tk.Label(frame_right, text="Sélectionnez un jeu", font=("Arial", 24), bg='black', fg='white')
label_preview.pack(fill=tk.BOTH, expand=True)

# Remplir la liste
for game in games:
    game_listbox.insert(tk.END, game["name"])

# Sélection par défaut
game_listbox.selection_set(0)
play_preview()

root.mainloop()
