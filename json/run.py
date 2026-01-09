import json
from pathlib import Path
import configparser
import os

# Répertoires principaux
MAIN_DIR = Path("/media/fat/_Arcade")       # dossiers originaux des .mra
ALT_DIR = Path("/media/fat/_Arcade/_alternatives")   # dossiers des collections / liens symboliques

# Fichier menu.json
MENU_FILE = Path("menu.json")

# Lecture du menu
with open(MENU_FILE, "r") as f:
    menu = json.load(f)

# Lecture du names.ini
names_ini = configparser.ConfigParser()
names_ini.read("names.ini")  # assumes format [Collections] capcom=Capcom etc

# Parcours des collections
for coll in menu['collections']:
    if not coll.get("enabled", True):
        print(f"[SKIP] Collection désactivée : {coll['name']}")
        continue

    coll_name = coll['name']
    json_file = Path(coll['file'])

    if not json_file.exists():
        print(f"[ERROR] Fichier JSON de collection introuvable : {json_file}")
        continue

    # Nom du dossier depuis names.ini
    folder_name = names_ini.get("Collections", coll_name, fallback=coll_name)
    collection_folder = ALT_DIR / folder_name
    collection_folder.mkdir(parents=True, exist_ok=True)
    print(f"[INFO] Traitement de '{coll_name}' → dossier '{collection_folder}'")

    # Lecture des jeux
    with open(json_file, "r") as f:
        collection_data = json.load(f)

    for game, info in collection_data['games'].items():
        mra_file = MAIN_DIR / info['mra']
        alt_name = info.get('alt', game)
        orientation = info.get('orientation', 'H')
        type_ = info.get('type', None)

        symlink_path = collection_folder / alt_name

        if not mra_file.exists():
            print(f"  [WARNING] Fichier MRA introuvable pour {game}: {mra_file}")
            continue

        if symlink_path.exists():
            print(f"  [SKIP] Lien déjà existant : {symlink_path}")
        else:
            os.symlink(mra_file, symlink_path)
            print(f"  [CREATED] Lien créé : {symlink_path} (orientation={orientation}, type={type_})")
