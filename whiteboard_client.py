import tkinter as tk
import socket
import pickle
import threading


class Whiteboard:
    def __init__(self, root):
        self.is_drawing = False
        self.root = root
        self.root.title("Whiteboard")

        self.canvas = tk.Canvas(self.root, bg="#f0f0f0", width=1000, height=700)  # Light grey background
        self.canvas.pack()

        self.setup()
        self.canvas.bind("<Button-1>", self.start_drawing)
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.stop_drawing)

    def setup(self):
        self.old_x = None
        self.old_y = None

    def start_drawing(self, event):
        x, y = event.x, event.y
        message = f"start {x} {y}"
        client.send(message.encode())

    def stop_drawing(self, event):
        message = f"stop"
        client.send(message.encode())

    def draw(self, event):
        x, y = event.x, event.y

        message = f"draw {x} {y}"
        client.send(message.encode())

    def clear(self):
        self.canvas.delete("all")
        self.setup()

    def set_canvas(self, new_canvas):
        self.canvas = new_canvas


def copy_canvas(client):
    while True:
        canvas = pickle.loads(client.recv(4096).decode())
        whiteboard.set_canvas(canvas)


def on_slider_move(value):
    width_label.config(text=f"Width: {value}")


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = socket.gethostname()
port = 9000

client.connect((host, port))

threading.Thread(target=copy_canvas, args=(client,)).start()

root = tk.Tk()
root.configure(bg="#f0f0f0")  # Set root background to match canvas
whiteboard = Whiteboard(root)

bottom_frame = tk.Frame(root, bg="#666666")  # Darker color for the bottom menu
bottom_frame.pack(side=tk.BOTTOM, fill=tk.X)

clear_button = tk.Button(bottom_frame, text="Clear", command=whiteboard.clear, bg="#333333", fg="white",
                         relief=tk.FLAT)  # Darker button with white text
clear_button.pack(side=tk.LEFT, padx=10, pady=5)

width_label = tk.Label(bottom_frame, text="Width: 0", bg="#666666", fg="white")  # Label matches the background
width_label.pack(side=tk.LEFT, padx=10, pady=5)

width_Scale = tk.Scale(bottom_frame, from_=0, to=30, showvalue=0, orient=tk.HORIZONTAL, command=on_slider_move,
                       bg="#666666", troughcolor="#999999", sliderlength=20, length=200)  # Adjusted slider appearance
width_Scale.pack(side=tk.LEFT, padx=10, pady=5)

root.mainloop()
