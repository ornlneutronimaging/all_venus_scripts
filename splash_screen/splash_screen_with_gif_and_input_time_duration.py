import tkinter as tk
from PIL import Image, ImageTk
import argparse

FILE = "/SNS/VENUS/shared/software/logos/logo_with_message.gif"


class MyApp(tk.Frame):

    def __init__(self, root):

        super().__init__(
            root,
            bg='WHITE'
        )

        self.main_frame = self

        self.main_frame.pack(fill=tk.BOTH, expand=True)
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.rowconfigure(0, weight=1)

        self.create_widgets()

    def create_widgets(self):

        self.label_gif1 = tk.Label(
            self.main_frame,
            background='WHITE',
            border=0,
            highlightthickness=0
        )

        self.label_gif1.grid(column=0, row=0)
        self.gif1_frames = self._get_frames(FILE)
        # self._play_gif(self.label_gif1, self.gif1_frames)
        root.after(10, self._play_gif, self.label_gif1, self.gif1_frames)

    def _get_frames(self, img):

        with Image.open(img) as gif:
            index = 0
            frames = []
            while True:
                try:
                    gif.seek(index)
                    frame = ImageTk.PhotoImage(gif)
                    frames.append(frame)
                except EOFError:
                    break
                index += 1

            return frames

    def _play_gif(self, label, frames):

        total_delay = 50   # ms
        delay_frames = 100  # ms
        for frame in frames:
            root.after(total_delay, self._next_frame, frame, label, frames)
            total_delay += delay_frames
        root.after(total_delay, self._next_frame, frame, label, frames, True)

    def _next_frame(self, frame, label, frames, restart=False):
        if restart:
            root.after(1, self._play_gif, label, frames)
            return

        label.config(
            image=frame
        )


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('time_duration', help='How long should we keep the splash screen displayed!')
    args = parser.parse_args()

    root = tk.Tk()
    root.title("My app")
    root.overrideredirect(True) # hide the title bar

    splash_width = 550
    splash_height = 600

    root.resizable(width=False, height=False)

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    left_position = int(screen_width/2 - splash_width/2)
    top_position = int(screen_height/2 - splash_height/2)

    root.geometry(f'{splash_width}x{splash_height}+{left_position}+{top_position}')
    # root.iconbitmap('logo.png')

    my_app_instance = MyApp(root)

    time_duration = int(args.time_duration)    # s
    root.after(time_duration*1000, root.destroy)

    root.mainloop()
