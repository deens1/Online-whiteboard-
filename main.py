import threading
import tkinter as tk
import socket
import pickle


class Whiteboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Whiteboard")

        self.canvas = tk.Canvas(self.root, bg="#f0f0f0", width=1000, height=700)  # Light grey background
        self.canvas.pack()
        self.canvas.

        self.canvas.bind("<Button-1>", self.start_drawing)
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.stop_drawing)

        self.old_x = None
        self.old_y = None

    def start_drawing(self, event):
        # x, y = event.x, event.y
        x, y = float(event[1]), float(event[2])
        self.canvas.create_line(x - 0.1, y - 0.1, x + 0.1, y + 0.1, fill="Black", width=width_Scale.get(),
                                capstyle=tk.ROUND, smooth=True)

    def stop_drawing(self, event=None):
        self.old_x = None

    def draw(self, event):
        # x, y = event.x, event.y
        x, y = event[1], event[2]

        if self.old_x is None:
            self.old_x = x
            self.old_y = y

        try:
            self.canvas.create_line(self.old_x, self.old_y, x, y, fill="Black", width=width_Scale.get(),
                                    capstyle=tk.ROUND, smooth=True)
        except:
            print(f"{x}  {y}")

        self.old_x = x
        self.old_y = y

    def send_canvas_to_client(self, conn):
        pickled_canvas = pickle.dumps(self.canvas)
        conn.send(pickled_canvas)

    def clear(self):
        self.canvas.delete("all")


def on_slider_move(value):
    width_label.config(text=f"Width: {value}")


def listen_for_clients():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    host = socket.gethostname()
    port = 9000

    server.bind((host, port))
    server.listen(5)

    print("Server listening on {}:{}".format(host, port))

    while True:
        conn, addr = server.accept()
        print(f"Connection from {addr} has been established.")
        threading.Thread(target=client_connection, args=(conn,)).start()


def client_connection(conn):
    while True:
        # Receive data from the client
        data = str(conn.recv(1024).decode())

        if not data:
            break

        if data.startswith("draw"):
            whiteboard.draw(data.split())

        elif data.startswith("start"):
            whiteboard.start_drawing(data.split())

        elif data.startswith("stop"):
            whiteboard.stop_drawing()

        whiteboard.send_canvas_to_client(conn)


threading.Thread(target=listen_for_clients).start()
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
