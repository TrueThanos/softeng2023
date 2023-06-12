import tkinter as tk
import json

class RoomDialog:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Room Visualization")
        self.canvas = None
        self.room_width = 0
        self.room_length = 0

        self.create_widgets()

    def create_widgets(self):
        # Label and Entry for room width
        self.width_label = tk.Label(self.window, text="Width:")
        self.width_label.pack()
        self.width_entry = tk.Entry(self.window)
        self.width_entry.pack()

        # Label and Entry for room length
        self.length_label = tk.Label(self.window, text="Length:")
        self.length_label.pack()
        self.length_entry = tk.Entry(self.window)
        self.length_entry.pack()

        # Submit button
        self.submit_button = tk.Button(self.window, text="Submit", command=self.submit_form)
        self.submit_button.pack()

        self.room_space = RoomSpace(self.window)

    def submit_form(self):
        # Get room dimensions from user input
        self.room_width = int(self.width_entry.get())
        self.room_length = int(self.length_entry.get())

        self.length_entry.destroy()
        self.length_label.destroy()
        self.width_entry.destroy()
        self.width_label.destroy()
        self.submit_button.destroy()

        l = tk.Label(self.window, text = "Click left to reserve space, click right to add speakers")
        l.config(font =("Courier", 14))
        l.pack(side='left')

        # Draw the grid
        self.room_space.initialize(self.room_width, self.room_length)

    def run(self):
        self.window.mainloop()

class RoomSpace:
    def __init__(self, window):
        self.window = window
        
        self.width = None
        self.length = None

        self.reserved_positions = []
        self.speaker_overlay = SpeakerOverlay()

        # Canvas for grid visualization
        self.canvas = tk.Canvas(self.window, width=1200, height=400)
        self.canvas.pack(expand=True, fill=tk.BOTH)

    def initialize(self, room_width, room_length):
        # Bind mouse click event - left click
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        # Bind mouse click event - right click
        self.canvas.bind("<Button-3>", self.on_canvas_click)

        self.width = room_width
        self.length = room_length

        self.draw_room()

    def draw_room(self):
        self.canvas.delete("all")

        # Calculate the size of each grid square based on canvas dimensions and room size
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        grid_size = min(canvas_width / self.width, canvas_height / self.length)

        for i in range(self.length):
            for j in range(self.width):
                x1 = j * grid_size
                y1 = i * grid_size
                x2 = x1 + grid_size
                y2 = y1 + grid_size

                if (i, j) in self.reserved_positions:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill="blue", outline="black")
                elif (i, j) in self.speaker_overlay.speaker_positions:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill="red", outline="black")
                else:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill="white", outline="black")

    def on_canvas_click(self, event):
        # Calculate the grid indices based on the mouse click coordinates
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        grid_size = min(canvas_width / self.width, canvas_height / self.length)

        grid_x = int(event.x // grid_size)
        grid_y = int(event.y // grid_size)

        # Toggle the color of the clicked grid square
        if event.num == 1 and (grid_y, grid_x) not in self.reserved_positions:
            self.reserved_positions.append(tuple((grid_y, grid_x)))
        elif event.num == 1:
            self.reserved_positions.remove((grid_y, grid_x))
        elif event.num == 3 and (grid_y, grid_x) not in self.speaker_overlay.speaker_positions:
            self.speaker_overlay.add_speaker(grid_y, grid_x)
        elif event.num == 3:
            self.speaker_overlay.remove_speaker(grid_y, grid_x)

        # Redraw the grid
        self.draw_room()

class SpeakerOverlay:
    def __init__(self):
        self.speaker_positions = []

    def add_speaker(self, y, x):
        self.speaker_positions.append(tuple((y, x)))

    def remove_speaker(self, y, x):
        self.speaker_positions.remove((y, x))

# Create and run the application
app = RoomDialog()
app.run()