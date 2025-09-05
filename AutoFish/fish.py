import time
import pyautogui
import pygetwindow as gw
import pytesseract
from PIL import Image
import os

# ------- CONFIGURAÇÕES -------
CAST_DELAY = 0.005
LOOP_DELAY = 1.50
SEARCH_EVERY = 0.35
CONFIDENCE = 0.65
CLICK_POINT_REL = (810, 540)

IMG_CONTINUE = "continue.png"
IMG_FLEE     = "flee.png"
IMG_EXIT     = "flee_yes.png"
LINE_BROKE   = "line_broke.png"
ITEMS_BTN    = "items.png"
LINE_BTN     = "fish_line.png"
CONTINUE_ALT = "continue_alt.png"

# caminho do tesseract OCR
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# região do contador (x, y, largura, altura)
COUNTER_REGION = (1172, 47, 43, 20)

# variáveis globais
total_peixes = 0
total_sessao = 0

# configurar se o script deve fechar BlueStacks ao atingir 500 peixes
FECHAR_BLUESTACKS = True
BLUESTACKS_PROCESS = "HD-Player.exe"  # confirme no Gerenciador de Tarefas!
# -----------------------------

pyautogui.FAILSAFE = True

def get_bluestacks_window():
    titles = [t for t in gw.getAllTitles() if "BlueStacks" in t]
    if not titles:
        raise RuntimeError("Janela do BlueStacks não encontrada.")
    win = gw.getWindowsWithTitle(titles[0])[0]
    if win.isMinimized:
        win.restore()
    win.activate()
    time.sleep(0.5)
    return win

def click_relative(win, rel_xy, delay_before_click=0.2):
    x = win.left + rel_xy[0]
    y = win.top + rel_xy[1]
    pyautogui.moveTo(x, y, duration=0.15)
    time.sleep(delay_before_click)
    pyautogui.click(x, y)

def locate_in_window(image_path, win, confidence=CONFIDENCE):
    region = (win.left, win.top, win.width, win.height)
    try:
        return pyautogui.locateCenterOnScreen(image_path, region=region, confidence=confidence)
    except pyautogui.ImageNotFoundException:
        return None

def ler_contador(win):
    global total_sessao, total_peixes
    region = (
        win.left + COUNTER_REGION[0],
        win.top + COUNTER_REGION[1],
        COUNTER_REGION[2],
        COUNTER_REGION[3]
    )
    screenshot = pyautogui.screenshot(region=region)
    texto = pytesseract.image_to_string(screenshot, config="--psm 7 digits")
    try:
        valor = int(texto.strip())
        total_sessao = valor
        return valor
    except:
        return None

def fechar_bluestacks():
    if FECHAR_BLUESTACKS:
        print("[END] Fechando BlueStacks...")
        os.system(f"taskkill /IM {BLUESTACKS_PROCESS} /F")

def main():
    global total_peixes, total_sessao
    print("Iniciando... Ctrl+C para parar.")
    win = get_bluestacks_window()

    while True:
        # Verificação do limite diário
        if total_peixes + total_sessao >= 500:
            print(f"[END] Limite diário de 500 peixes atingido. Encerrando script.")
            fechar_bluestacks()
            break

        # 1) Clique para iniciar
        click_relative(win, CLICK_POINT_REL)
        time.sleep(CAST_DELAY)

        # 2) Clique para lançar
        click_relative(win, CLICK_POINT_REL)

        # 3) Espera resultado
        started = time.time()
        contador_atual = None  # inicializado para evitar erro
        while True:
            cont = locate_in_window(IMG_CONTINUE, win)
            if not cont:
                cont = locate_in_window(CONTINUE_ALT, win)
            if cont:
                pyautogui.click(cont)
                time.sleep(0.3)

                # após capturar peixe/item, atualiza contador
                contador_atual = ler_contador(win)
                if contador_atual is not None:
                    print(f"Sessão: {total_sessao} | Total do dia: {total_peixes + total_sessao}")
                break

            flee = locate_in_window(IMG_FLEE, win)
            if flee:
                print("[LOG] Fugindo do combate")
                pyautogui.click(flee)
                time.sleep(0.8)
                exit_btn = locate_in_window(IMG_EXIT, win)
                if exit_btn:
                    pyautogui.click(exit_btn)
                    time.sleep(0.5)
                break

            line_broken = locate_in_window(LINE_BTN, win)
            if line_broken:
                print("[LOG] Linha quebrou! Reequipando")
                # soma sessão ao total
                total_peixes += total_sessao
                total_sessao = 0
                print(f"[UPDATE] Sessão: {total_sessao} | Total do dia: {total_peixes + total_sessao}")

                # Checagem do limite também aqui
                if total_peixes + total_sessao >= 500:
                    print(f"[END] Limite diário de 500 peixes atingido. Encerrando script.")
                    fechar_bluestacks()
                    return

                pyautogui.click(line_broken)
                time.sleep(0.8)
                break

            time.sleep(SEARCH_EVERY)
            if time.time() - started > 30:
                print("[LOG] Timeout: voltando ao ciclo.")
                break

        time.sleep(LOOP_DELAY)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nParado pelo usuário.")
