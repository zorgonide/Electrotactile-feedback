import tkinter as tk
import time
from playsound import playsound
import threading


class YourApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sound Player")
        self.geometry("400x200")

        self.button_up = tk.Button(
            self, text='↑ Up', width=8, height=4, command=self.goUp)
        self.button_up.grid(row=1, column=3, pady=10)
        self.button_up_active = {"state": 0, "button": self.button_up}

        self.sound_thread = None
        self.is_sound_playing = False

    def check_button_active(self):
        if self.button_up_active["state"] == 1:
            self.toggle_button_color(self.button_up_active, self.button_up)

    def toggle_button_color(self, button_state, button):
        if button_state["state"] == 0:
            button.config(bg="red")
            button_state["state"] = 1
        else:
            button.config(bg="SystemButtonFace")
            button_state["state"] = 0

    def goUp(self):
        self.toggle_button_color(self.button_up_active, self.button_up)
        if self.button_up_active["state"] == 1:
            self.sound_thread = threading.Thread(
                target=self.play_sound_thread, args=('Forward.mp3',))
            self.is_sound_playing = True
            self.sound_thread.start()
        else:
            self.stop_sound()

    def play_sound_thread(self, sound_file):
        while self.is_sound_playing:
            playsound('Forward.mp3')
            time.sleep(4)

    def stop_sound(self):
        self.is_sound_playing = False

    def toggle_sound(self):
        if self.is_sound_playing:
            self.stop_sound()
        else:
            self.goUp()


if __name__ == "__main__":
    app = YourApp()
    app.mainloop()
