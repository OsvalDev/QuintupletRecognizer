import os
import random
import shutil

def duplicate_images_to_target(dir_path, target_count):
    images = [f for f in os.listdir(dir_path) if f.lower().endswith(('.jpeg'))]
    current_count = len(images)
    
    if current_count >= target_count:
        print(f"La carpeta ya tiene {current_count} imágenes, que es igual o mayor que {target_count}.")
        return
    
    while current_count < target_count:
        image_to_duplicate = random.choice(images)
        new_image_name = f"copy_{current_count}_{image_to_duplicate}"
        original_path = os.path.join(dir_path, image_to_duplicate)
        new_image_path = os.path.join(dir_path, new_image_name)
        shutil.copy(original_path, new_image_path)
        images.append(new_image_name)
        current_count += 1
    
    print(f"Se duplicaron imágenes hasta alcanzar {target_count}. Total actual: {current_count}.")

ruta_directorio = "../dataset/zerotwo" 
objetivo = 800
duplicate_images_to_target(ruta_directorio, objetivo)
