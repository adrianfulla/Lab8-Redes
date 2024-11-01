from PIL import Image
import numpy as np
from Crypto.Cipher import AES
import os

# a. Cargar imagen y convertir a Bytes
def carga_imagen():
    img = Image.open('tux.bmp').convert('RGBA')
    img_array = np.array(img)

    reshaped_img_array = np.reshape(img_array, (405, 480, 4))

    return reshaped_img_array.tobytes()


# b. Cifrar utilizando AES 128 en ECB
def cifrado_ecb(img_bytes):
    key = os.urandom(16)  

    cipher = AES.new(key, AES.MODE_ECB)

    pad_len = 16 - (len(img_bytes) % 16)
    padded_img_bytes = img_bytes + b'\x00' * pad_len 

    return cipher.encrypt(padded_img_bytes)

# c. Convertir bytes cifrados a imagen PNG
def bytes_a_png(bytes, filename):
    
    img_array = np.frombuffer(bytes, dtype=np.uint8)
    img_array = np.reshape(img_array[:405*480*4], (405, 480, 4))

    Image.fromarray(img_array, 'RGBA').save(filename)
    
    print(f"Imagen {filename} guardada")


# d. Cifrar utilizando AES 128 en CBC con vector de inicializacion
def cifrado_cbc(img_bytes):
    key = os.urandom(16) 
    iv = os.urandom(16)

    cipher = AES.new(key, AES.MODE_CBC, iv)

    pad_len = 16 - (len(img_bytes) % 16)
    padded_img_bytes = img_bytes + b'\x00' * pad_len

    return cipher.encrypt(padded_img_bytes)



if __name__ == "__main__":
    img_bytes = carga_imagen()
    
    bytes_cifrados = cifrado_ecb(img_bytes=img_bytes)
    
    bytes_a_png(bytes_cifrados, "lab8-2.2.2.a.png")
    
    bytes_cifrados = cifrado_cbc(img_bytes=img_bytes)
    
    bytes_a_png(bytes_cifrados, "lab8-2.2.2.b.png")