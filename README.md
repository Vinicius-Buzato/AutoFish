# 🎣 AutoFish Bot for BlueStacks

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)  
[![PyAutoGUI](https://img.shields.io/badge/PyAutoGUI-Automation-green)](https://pyautogui.readthedocs.io/)  
[![License](https://img.shields.io/badge/license-MIT-lightgrey.svg)](LICENSE)  

Automated fishing bot for a mobile game running on **BlueStacks**.  
This script simulates clicks and uses **OCR (Tesseract)** to track the number of fishes caught, stopping automatically when the daily limit is reached.

---

## ✨ Features
- 🎯 Automatic casting and re-casting of fishing line  
- 🐟 Detects when a fish/item is caught and continues fishing  
- 👹 Detects combat (monsters) and automatically flees  
- 💥 Detects when fishing line breaks and equips a new one  
- 🔢 OCR counter to track daily fish limit (500)  
- 🔒 Automatic stop (and optional BlueStacks shutdown) when limit is reached  

---

## ⚙️ Requirements
- **Python 3.9+**
- [Tesseract OCR](https://github.com/UB-Mannheim/tesseract/wiki) (Windows build recommended)

### Python Libraries
Install all dependencies with:
```bash
pip install pyautogui pygetwindow pytesseract pillow
```

---

## ▶️ Usage

1. Install **BlueStacks** and open the target game.  
2. Position the game window clearly on the screen.  
3. Adjust configuration in `fish.py`:  
   - `CLICK_POINT_REL`: where the fishing bar is triggered  
   - `COUNTER_REGION`: (x, y, width, height) of the on-screen fish counter  
   - `FECHAR_BLUESTACKS`: `True`/`False` to close emulator at 500 fishes  
   - `BLUESTACKS_PROCESS`: process name (`HD-Player.exe` or `Bluestacks.exe`)  

4. Run the bot:
```bash
python fish.py
```

---

## 🎮 Calibration

For OCR calibration:
- Run the helper script `ocr_debug.py` (included in repo).  
- It will save cropped screenshots from the counter area.  
- Adjust `COUNTER_REGION` until the numbers are recognized correctly.  

You can also enable **debug printouts** to track session vs. total fishes.

---

## 📁 Project Structure
```
AutoFish/
 ├── fish.py          # main bot script
 ├── ocr_debug.py     # helper for OCR calibration
 ├── /images/         # reference screenshots (continue, flee, etc.)
 ├── README.md        # project documentation
```

---

## ⚠️ Notes
- This script was made for educational purposes.  
- Ensure your system has focus on the BlueStacks window.  
- Dual monitor setups may require adjusting relative coordinates.  
- Use at your own risk in the game.

---

## 📜 License
This project is licensed under the [MIT License](LICENSE).
