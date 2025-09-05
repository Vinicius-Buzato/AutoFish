import time
import pyautogui
import pygetwindow as gw

# ------- CONFIGURAÇÕES -------
CAST_DELAY = 0.005  # segundos entre 1º e 2º clique (ajuste fino)
LOOP_DELAY = 1.50   # pausa entre ciclos
SEARCH_EVERY = 0.35 # intervalo de varredura de telas6
CONFIDENCE = 0.85   # 0.7-0.9; ajuste se não reconhecer
CLICK_POINT_REL = (810, 540)  # ponto para clicar (relativo à janela) para iniciar/lançar

IMG_CONTINUE  = "continue.png"
CONTINUE_ITEM = "continue_alt.png"
IMG_FLEE      = "flee.png"
IMG_EXIT      = "flee_yes.png"
LINE_BROKE    = "line_broke.png"
ITEMS         = "items.png"
NEW_LINE      = "fish_line.png"    # se houver um segundo botão pós-fuga
# -----------------------------

pyautogui.FAILSAFE = True  # mover mouse para canto superior-esquerdo aborta o script

def get_bluestacks_window():
    # Procura por qualquer janela com "BlueStacks" no título
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
    pyautogui.moveTo(x, y, duration=0.15)  # move suavemente
    time.sleep(0.25)         # espera antes do clique
    pyautogui.click(x, y)


def locate_in_window(image_path, win, confidence=CONFIDENCE):
    region = (win.left, win.top, win.width, win.height)
    try:
        return pyautogui.locateCenterOnScreen(image_path, region=region, confidence=confidence)
    except pyautogui.ImageNotFoundException:
        return None


def main():
    print("Iniciando... Ctrl+C para parar.")
    win = get_bluestacks_window()

    while True:
        # 1) Clique para iniciar a barra
        click_relative(win, CLICK_POINT_REL)
        time.sleep(CAST_DELAY)

        # 2) Clique para lançar
        click_relative(win, CLICK_POINT_REL)

        # 3) Espera resultado (loot ou batalha)
        started = time.time()
        while True:
            # 1) Tela de loot normal
            cont = locate_in_window(IMG_CONTINUE, win)
            if not cont:
                cont = locate_in_window(CONTINUE_ITEM, win)
            if cont:
                pyautogui.click(cont)
                time.sleep(0.3)
                break

            # 2) Tela de batalha
            flee = locate_in_window(IMG_FLEE, win)
            if flee:
                print("[LOG] Fugindo da luta")
                pyautogui.click(flee)
                time.sleep(0.8)
                exit_btn = locate_in_window(IMG_EXIT, win)
                if exit_btn:
                    pyautogui.click(exit_btn)
                    time.sleep(0.5)
                break

            # 3) Linha quebrada
            line_broken = locate_in_window(LINE_BROKE, win)
            if line_broken:
                print("[LOG] Linha quebrou! Equipando nova")
                pyautogui.click(line_broken)
                time.sleep(0.8)

                # Passo 1: abrir menu de itens
                items_btn = locate_in_window(ITEMS, win)
                if items_btn:
                    pyautogui.click(items_btn)
                    time.sleep(0.4)

                    # Passo 2: clicar na linha de pescaqq
                    fishing_line_btn = locate_in_window(NEW_LINE, win)
                    if fishing_line_btn:
                        pyautogui.click(fishing_line_btn)
                        time.sleep(0.3)
                break


            time.sleep(SEARCH_EVERY)

            # (Opcional) time-out de segurança para não travar caso nada apareça
            if time.time() - started > 30:
                print("Timeout: reiniciando ciclo.")
                break

        time.sleep(LOOP_DELAY)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nParado pelo usuário.")
