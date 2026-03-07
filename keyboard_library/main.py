import keyboard
import time

keyboard.write("Hello")


# shift_check = keyboard.is_pressed("shift")  # Returns True if the Shift key is currently being pressed

# keyboard.press("a")  # Simulates pressing the "a" key down

# keyboard.release("a")  # Simulates releasing the "a" key

# print(shift_check)  # Output: True or False depending on whether Shift is pressed

"""
Helloa
Helloa

Hello
Helloaṁ


My name is 

"""


"""
keyboard.add_hotkey("alt+h+e", lambda: keyboard.write("Hello"))
keyboard.wait()
"""


keyboard.add_hotkey("ctrl+alt+m", lambda: keyboard.write("My name is "))






def write_name():
    time.sleep(0.05)
    keyboard.write("Rana Ji".upper())

keyboard.add_hotkey("alt+r", write_name)

keyboard.wait()


"""
Hello
ṁMy name is 

Hello
ṁMy name is 
NA JI
na Ji
Hello
RANA JI



"""




