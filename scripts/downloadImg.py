import requests
import os
import re
import base64

#let a = Array.from(document.querySelectorAll('.YQ4gaf:not(.zr758c)')).map(e => e.src)
#document.onclick = () => {navigator.clipboard.writeText(JSON.stringify(a))}

data = ["results of the previous commented lines"]

def download_image(url, folder, file_name):
    try:
        # Realiza la solicitud a la URL
        response = requests.get(url)
        if response.status_code == 200:
            # Obtener el tipo de archivo desde el encabezado 'Content-Type'
            content_type = response.headers['Content-Type']
            if 'image' in content_type:
                # Extraer la extensión del tipo de contenido
                extension = content_type.split('/')[-1]
                # Asegurarse de que la extensión sea válida
                if extension in ['jpeg', 'jpg', 'png']:
                    # Crear la carpeta si no existe
                    if not os.path.exists(folder):
                        os.makedirs(folder)

                    # Definir el nombre del archivo con la extensión correcta
                    filename = os.path.join(folder, f"{file_name}.{extension}")
                    with open(filename, "wb") as f:
                        f.write(response.content)
                    print(f"Imagen descargada: {filename}")
                else:
                    print(f"Tipo de imagen no soportado: {content_type}")
            else:
                print(f"No es una imagen válida: {url}")
        else:
            print(f"No se pudo descargar la imagen {url}")
    except Exception as e:
        print(f"Error al descargar la imagen {url}: {e}")

def download_image_from_base64(base64_string, folder, file_name):
    # Extraer el tipo de archivo
    match = re.match(r'data:image/(.*?);base64,(.*)', base64_string)
    if match:
        image_type = match.group(1)  # Tipo de imagen
        image_data = match.group(2)  # Parte codificada en base64
        
        # Decodificar la imagen
        image_bytes = base64.b64decode(image_data)
        
        # Crear la carpeta si no existe
        if not os.path.exists(folder):
            os.makedirs(folder)
        
        file_path = os.path.join(folder, f"{file_name}.{image_type}")
        
        with open(file_path, 'wb') as image_file:
            image_file.write(image_bytes)
        
        print(f"Imagen guardada en {file_path}")
    else:
        download_image(base64_string, folder, file_name)

def get_initial_index(folder):
    existing_files = os.listdir(folder)
    image_files = [f for f in existing_files if f.endswith(('.jpeg', '.jpg', '.png', '.gif'))]
    indices = [int(f.split('.')[0]) for f in image_files if f.split('.')[0].isdigit()]
    return max(indices, default=-1) + 1

folder = "../dataset/itsuki"

i = get_initial_index(folder)
for e in data:
    download_image_from_base64(e, folder, i)
    i += 1
