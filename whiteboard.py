import tkinter as tk
from tkinter import filedialog
from tkinter.colorchooser import askcolor
from PIL import ImageGrab

class WhiteboardApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Whiteboard App")
        self.geometry("800x600")

        self.canvas = tk.Canvas(self, bg="white")
        self.canvas.pack(fill="both", expand=True)

        self.controls_frame = tk.Frame(self)
        self.controls_frame.pack(side="top", fill="x")

        self.drawing_color = "black"
        self.line_width = 2
        self.is_drawing = False
        self.prev_x, self.prev_y = None, None

        self.create_controls()
        self.bind_events()

    def create_controls(self):
        color_button = tk.Button(self.controls_frame, text="Change Color", command=self.change_pen_color)
        clear_button = tk.Button(self.controls_frame, text="Clear Canvas", command=self.canvas.delete("all"))
        save_button = tk.Button(self.controls_frame, text="Save Drawing", command=self.save_drawing)

        color_button.pack(side="left", padx=5, pady=5)
        clear_button.pack(side="left", padx=5, pady=5)
        save_button.pack(side="left", padx=5, pady=5)

        line_width_label = tk.Label(self.controls_frame, text="Line Width:")
        line_width_label.pack(side="left", padx=5, pady=5)

        line_width_slider = tk.Scale(self.controls_frame, from_=1, to=10, orient="horizontal", command=self.change_line_width)
        line_width_slider.set(self.line_width)
        line_width_slider.pack(side="left", padx=5, pady=5)

    def bind_events(self):
        self.canvas.bind("<Button-1>", self.start_drawing)
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.stop_drawing)

    def start_drawing(self, event):
        self.is_drawing = True
        self.prev_x, self.prev_y = event.x, event.y

    def draw(self, event):
        if self.is_drawing:
            current_x, current_y = event.x, event.y
            self.canvas.create_line(self.prev_x, self.prev_y, current_x, current_y, fill=self.drawing_color,
                                    width=self.line_width, capstyle=tk.ROUND, smooth=True)
            self.prev_x, self.prev_y = current_x, current_y

    def stop_drawing(self, event):
        self.is_drawing = False

    def change_pen_color(self):
        color = askcolor()[1]
        if color:
            self.drawing_color = color

    def change_line_width(self, value):
        self.line_width = int(value)

    def save_drawing(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".png")
        if file_path:
            x = self.canvas.winfo_rootx()
            y = self.canvas.winfo_rooty()
            x1 = x + self.canvas.winfo_width()
            y1 = y + self.canvas.winfo_height()
            ImageGrab.grab().crop((x, y, x1, y1)).save(file_path)

if __name__ == "__main__":
    app = WhiteboardApp()
    app.mainloop()
