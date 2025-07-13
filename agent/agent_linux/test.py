import pyautogui
import time

# Дать время переключиться на окно LibreOffice
time.sleep(5)

# Ввод текста
pyautogui.typewrite('Привет, LibreOffice!')

# Нажать Enter
pyautogui.press('enter')

