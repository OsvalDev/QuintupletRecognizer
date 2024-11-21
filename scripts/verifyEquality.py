import os

folder_paths = ["asuna", "chizuru", "ichika", "itsuki", "kaede", "mai", "mami", "miku", "nino", "rei", "ruka", "serena", "sumi", "yotsuba", "zerotwo"]
targetNumber = 800
notSuccess = []
base_path = "../dataset/"

for folder in folder_paths:
    files = os.listdir(base_path + folder)

    if len(files) != targetNumber:
        notSuccess.append((folder, len(files) - targetNumber ))

if len(notSuccess)> 0: print(f"Folder without enogh imgs: {notSuccess}")
else: print("All success")