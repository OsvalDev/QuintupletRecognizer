import os
from tqdm import tqdm

folder_paths = ["asuna", "chizuru", "ichika", "itsuki", "kaede", "mai", "mami", "miku", "nino", "rei", "ruka", "serena", "sumi", "yotsuba", "zerotwo"]
# folder_paths = ["rei"]
new_extension = ".jpeg"
temp_extension = ".temp" 

for element in folder_paths:
    folder_path = f"../dataset/{element}"
    files = os.listdir(folder_path)

    files = [f for f in files if f.endswith(new_extension)]

    files.sort()

    for i, file_name in enumerate(tqdm(files, desc=f"Renombrando archivos temporales en {element}"), start=0):
        old_file_path = os.path.join(folder_path, file_name)
        temp_file_name = f"temp_{i}{temp_extension}"
        temp_file_path = os.path.join(folder_path, temp_file_name)
        os.rename(old_file_path, temp_file_path)

    temp_files = os.listdir(folder_path)
    temp_files = [f for f in temp_files if f.startswith("temp_")]
    temp_files.sort()

    for i, temp_file_name in enumerate(tqdm(temp_files, desc=f"Renombrando archivos finales en {element}"), start=0):
        temp_file_path = os.path.join(folder_path, temp_file_name)
        new_file_name = f"{i}{new_extension}"
        new_file_path = os.path.join(folder_path, new_file_name)
        os.rename(temp_file_path, new_file_path)

    print(f"Renombrado {element} finalizado")

print("Renombrado completo.")
