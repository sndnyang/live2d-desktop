# from elevate import elevate
# import time
import pyautogui

def click_at(x=400, y=10):
    pyautogui.moveTo(400, 10, duration=0.1)
    pyautogui.click(clicks=2)
    # elevate()
    # time.sleep(1)
    # pyautogui.moveTo(400, 20, duration=0.25)
    # pyautogui.click(clicks=2)

if __name__ == "__main__":
    click_at()