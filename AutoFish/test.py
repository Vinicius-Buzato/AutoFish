# ########## Teste posição do mouse #########

# import pyautogui
# import time

# print("Posicione o mouse sobre o contador em 3 segundos...")
# time.sleep(3)
# print("Posição atual do mouse:", pyautogui.position())


######### Teste leitura de números #########

import time
import pyautogui
import pytesseract
from PIL import Image
import os

# Caminho do tesseract OCR (ajuste se for diferente!)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Região do contador (x, y, largura, altura) – AJUSTAR!
COUNTER_REGION = (1172, 47, 43, 20)

# Pasta onde vamos salvar as imagens
SAVE_PATH = "ocr_debug"
os.makedirs(SAVE_PATH, exist_ok=True)

def ler_contador():
    region = (
        COUNTER_REGION[0],
        COUNTER_REGION[1],
        COUNTER_REGION[2],
        COUNTER_REGION[3]
    )
    screenshot = pyautogui.screenshot(region=region)

    # salva cada captura com timestamp
    filename = os.path.join(SAVE_PATH, f"frame_{int(time.time())}.png")
    screenshot.save(filename)
    print(f"[DEBUG] Screenshot salva em {filename}")

    texto = pytesseract.image_to_string(screenshot, config="--psm 7 digits")
    try:
        return int(texto.strip())
    except:
        return None

print("Iniciando calibração... Ctrl+C para parar.")
while True:
    valor = ler_contador()
    if valor is not None:
        print("Contador detectado:", valor)
    else:
        print("⚠️ Não consegui ler nada, ajuste a região COUNTER_REGION")
    time.sleep(5.0)
