import requests
import os
import re
import base64
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_service = Service('./chromedriver-win64/chromedriver.exe')
driver = webdriver.Chrome(service=chrome_service, options=chrome_options)



urls_and_folders = [
    {
        "url": "https://www.google.com/search?q=kaede+bunny+girl+senpai+anime&client=opera&hs=FNt&sca_esv=35a14008bdd29155&udm=2&biw=1482&bih=714&sxsrf=ADLYWIJBPbI5DrN0kIPenNNu8fl4ER0diA%3A1732204108945&ei=TFY_Z9K1Ob-dkPIPurK5-Ao&ved=0ahUKEwjSi96U4-2JAxW_DkQIHTpZDq8Q4dUDCBE&uact=5&oq=kaede+bunny+girl+senpai+anime&gs_lp=EgNpbWciHWthZWRlIGJ1bm55IGdpcmwgc2VucGFpIGFuaW1lSJQzUJwSWLIycAF4AJABAJgBnQGgAd8IqgEDOC4zuAEDyAEA-AEBmAIIoAKaBsICChAAGIAEGEMYigXCAgQQABgewgIGEAAYCBgewgIEECMYJ8ICCBAAGIAEGLEDwgIFEAAYgATCAg0QABiABBixAxhDGIoFwgILEAAYgAQYsQMYgwHCAgcQABiABBgTwgIGEAAYExgewgIIEAAYExgKGB7CAggQABgTGAgYHpgDAIgGAZIHAzIuNqAH6zE&sclient=img",
        "folder": "../dataset/kaede",
        "source": "google"
    },
    {
        "url": "https://www.google.com/search?q=mami+rent+a+girlfriend+anime&client=opera&sca_esv=35a14008bdd29155&udm=2&biw=1482&bih=714&sxsrf=ADLYWIIpee9GJ1KnXaC_N16O2iBx0vW8vg%3A1732205462256&ei=lls_Z-WpD67VkPIPgK6swAQ&ved=0ahUKEwjlzIWa6O2JAxWuKkQIHQAXC0gQ4dUDCBE&uact=5&oq=mami+rent+a+girlfriend+anime&gs_lp=EgNpbWciHG1hbWkgcmVudCBhIGdpcmxmcmllbmQgYW5pbWVIpoQBUL8LWJZ_cAN4AJABAJgBkgKgAe8YqgEGNy4xMy4zuAEDyAEA-AEBmAIEoAKBBMICBhAAGAcYHsICCBAAGAcYChgewgIFEAAYgATCAggQABgHGAgYHpgDAIgGAZIHAzEuM6AH0CA&sclient=img",
        "folder": "../dataset/mami",
        "source": "google"
    },
    {
        "url": "https://www.google.com/search?q=ruka+rent+a+girlfriend+anime&client=opera&sca_esv=35a14008bdd29155&udm=2&biw=1482&bih=714&sxsrf=ADLYWILavStyfwObsvfxN8RKDIsSLBEpkQ%3A1732205522218&ei=0ls_Z6_xDJ66kPIPmOeC0Q4&ved=0ahUKEwivotG26O2JAxUeHUQIHZizIOoQ4dUDCBE&uact=5&oq=ruka+rent+a+girlfriend+anime&gs_lp=EgNpbWciHHJ1a2EgcmVudCBhIGdpcmxmcmllbmQgYW5pbWVIxw1QkQdY5QtwAngAkAEAmAFioAHSA6oBATW4AQPIAQD4AQGYAgGgAmbCAggQABgHGAgYHpgDAIgGAZIHAzAuMaAHnQs&sclient=img",
        "folder": "../dataset/ruka",
        "source": "google"
    },
    {
        "url": "https://www.google.com/search?q=sumi+rent+a+girlfriend+anime&client=opera&sca_esv=35a14008bdd29155&udm=2&biw=1482&bih=714&sxsrf=ADLYWIIKfDbXS6po6BRZvBrgj7Xfa54qdw%3A1732205544678&ei=6Fs_Z_SOKe_HkPIPgKKewA8&ved=0ahUKEwj0oqzB6O2JAxXvI0QIHQCRB_gQ4dUDCBE&uact=5&oq=sumi+rent+a+girlfriend+anime&gs_lp=EgNpbWciHHN1bWkgcmVudCBhIGdpcmxmcmllbmQgYW5pbWUyCBAAGAcYCBgeMggQABgHGAgYHjIIEAAYBxgIGB4yCBAAGAcYCBgeMggQABgHGAgYHjIIEAAYBxgIGB5IqwxQowVYhAtwAngAkAEAmAHYAaABmgOqAQUyLjAuMbgBA8gBAPgBAZgCAqACyQGYAwCIBgGSBwMxLjGgB9sP&sclient=img",
        "folder": "../dataset/sumi",
        "source": "google"
    },
    {
        "url": "https://www.google.com/search?q=serena+pokemon+anime&client=opera&sca_esv=35a14008bdd29155&udm=2&biw=1482&bih=714&sxsrf=ADLYWIKVFhxnYQlsR3d66ARJKo1ei90Xhw%3A1732205569290&ei=AVw_Z9O2EZ3BkPIPvNKqgAk&ved=0ahUKEwiTu4rN6O2JAxWdIEQIHTypCpAQ4dUDCBE&uact=5&oq=serena+pokemon+anime&gs_lp=EgNpbWciFHNlcmVuYSBwb2tlbW9uIGFuaW1lMgYQABgHGB4yBhAAGAcYHjIGEAAYBxgeMgYQABgHGB4yBhAAGAcYHjIGEAAYBxgeMgYQABgHGB4yCBAAGAcYChgeMggQABgHGAoYHjIIEAAYBxgIGB5I1ClQ5RBYpCdwA3gAkAECmAHnBqABrReqAQ0wLjQuMS4xLjEuMS4xuAEDyAEA-AEBmAIEoAKTBMICBBAAGB6YAwCIBgGSBwMwLjSgB9Ey&sclient=img",
        "folder": "../dataset/serena",
        "source": "google"
    },
]

def scroll_to_bottom(driver):
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

def scrape_images(url, source):
    driver.get(url)
    scroll_to_bottom(driver)

    if source == "google":
        images = driver.execute_script("""
            return Array.from(document.querySelectorAll('.YQ4gaf:not(.zr758c)')).map(e => e.src);
        """)
    elif source == "pinterest":
        images = set()
        last_height = driver.execute_script("return document.body.scrollHeight")
        
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)

            new_images = driver.execute_script("""
                return Array.from(document.querySelectorAll('img')).map(e => e.src);
            """)
            images.update(new_images)

            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
        
        images = list(images)
    r = input(f"lon images: {len(images)}. Proced? (y/n)")
    if r == "y": return images
    else: exit(0)

def download_image(url, folder, file_name):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            content_type = response.headers['Content-Type']
            if 'image' in content_type:
                extension = content_type.split('/')[-1]
                if extension in ['jpeg', 'jpg', 'png']:
                    if not os.path.exists(folder):
                        os.makedirs(folder)
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
    match = re.match(r'data:image/(.*?);base64,(.*)', base64_string)
    if match:
        image_type = match.group(1)
        image_data = match.group(2)
        image_bytes = base64.b64decode(image_data)
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

for entry in urls_and_folders:
    url = entry["url"]
    folder = entry["folder"]
    source = entry["source"]
    
    images = scrape_images(url, source)
    
    i = get_initial_index(folder)
    for img_url in images:
        download_image_from_base64(img_url, folder, i)
        i += 1

driver.quit()
