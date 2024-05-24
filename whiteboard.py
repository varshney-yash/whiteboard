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
        self.shape = "free_draw"
        self.prev_x, self.prev_y = None, None
        self.lines = []
        self.current_shape_id = None

        self.create_controls()
        self.bind_events()

    def create_controls(self):
        color_button = tk.Button(self.controls_frame, text="Change Color", command=self.change_pen_color)
        clear_button = tk.Button(self.controls_frame, text="Clear Canvas", command=self.clear_canvas)
        undo_button = tk.Button(self.controls_frame, text="Undo", command=self.undo)
        save_button = tk.Button(self.controls_frame, text="Save Drawing", command=self.save_drawing)

        color_button.pack(side="left", padx=5, pady=5)
        clear_button.pack(side="left", padx=5, pady=5)
        undo_button.pack(side="left", padx=5, pady=5)
        save_button.pack(side="left", padx=5, pady=5)

        line_width_label = tk.Label(self.controls_frame, text="Line Width:")
        line_width_label.pack(side="left", padx=5, pady=5)

        line_width_slider = tk.Scale(self.controls_frame, from_=1, to=10, orient="horizontal", command=self.change_line_width)
        line_width_slider.set(self.line_width)
        line_width_slider.pack(side="left", padx=5, pady=5)

        free_draw_button = tk.Button(self.controls_frame, text="Free Draw", command=lambda: self.set_shape("free_draw"))
        rect_button = tk.Button(self.controls_frame, text="Rectangle", command=lambda: self.set_shape("rectangle"))
        oval_button = tk.Button(self.controls_frame, text="Oval", command=lambda: self.set_shape("oval"))
        line_button = tk.Button(self.controls_frame, text="Line", command=lambda: self.set_shape("line"))

        free_draw_button.pack(side="left", padx=5, pady=5)
        rect_button.pack(side="left", padx=5, pady=5)
        oval_button.pack(side="left", padx=5, pady=5)
        line_button.pack(side="left", padx=5, pady=5)

    def bind_events(self):
        self.canvas.bind("<Button-1>", self.start_drawing)
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.stop_drawing)

    def start_drawing(self, event):
        self.is_drawing = True
        self.prev_x, self.prev_y = event.x, event.y
        self.current_line = []

        if self.shape in ["rectangle", "oval", "line"]:
            self.current_shape_id = None

    def draw(self, event):
        if self.is_drawing:
            current_x, current_y = event.x, event.y

            if self.shape == "free_draw":
                line_id = self.canvas.create_line(self.prev_x, self.prev_y, current_x, current_y, fill=self.drawing_color,
                                                  width=self.line_width, capstyle=tk.ROUND, smooth=True)
                self.current_line.append(line_id)
                self.prev_x, self.prev_y = current_x, current_y
            else:
                if self.current_shape_id:
                    self.canvas.delete(self.current_shape_id)
                if self.shape == "rectangle":
                    self.current_shape_id = self.canvas.create_rectangle(self.prev_x, self.prev_y, current_x, current_y,
                                                                         outline=self.drawing_color, width=self.line_width)
                elif self.shape == "oval":
                    self.current_shape_id = self.canvas.create_oval(self.prev_x, self.prev_y, current_x, current_y,
                                                                    outline=self.drawing_color, width=self.line_width)
                elif self.shape == "line":
                    self.current_shape_id = self.canvas.create_line(self.prev_x, self.prev_y, current_x, current_y,
                                                                    fill=self.drawing_color, width=self.line_width)

    def stop_drawing(self, event):
        self.is_drawing = False
        if self.shape == "free_draw" and self.current_line:
            self.lines.append(self.current_line)
        elif self.current_shape_id:
            self.lines.append([self.current_shape_id])

    def change_pen_color(self):
        color = askcolor()[1]
        if color:
            self.drawing_color = color

    def change_line_width(self, value):
        self.line_width = int(value)

    def clear_canvas(self):
        self.canvas.delete("all")
        self.lines = []

    def undo(self):
        if self.lines:
            last_line = self.lines.pop()
            for line_id in last_line:
                self.canvas.delete(line_id)

    def save_drawing(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".png")
        if file_path:
            x = self.canvas.winfo_rootx()
            y = self.canvas.winfo_rooty()
            x1 = x + self.canvas.winfo_width()
            y1 = y + self.canvas.winfo_height()
            ImageGrab.grab().crop((x, y, x1, y1)).save(file_path)

    def set_shape(self, shape):
        self.shape = shape

if __name__ == "__main__":
    app = WhiteboardApp()
    app.mainloop()
