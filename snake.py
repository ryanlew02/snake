import tkinter as tk
import math, random


# I want it to be 17x17 with 25 pixel each for the squares


#This is to set the rows, columns, and cell size

rows = 17
cols = 17
cell_size = 25


# Margins around the grid


margin_top = 0
margin_side = 80
margin_bottom = 0


canvas_width = margin_side + cols * cell_size + margin_side
canvas_height = margin_top + rows * cell_size + margin_bottom


#Starting game state


snake = [(8, 8), (8, 7), (8, 6)]  #Initial snake position
direction = (0, 1)  #Initial direction (moving right)
score = 0  #Initial score
running = False  #Game running state
after_id = None  #ID for the after method
speed_ms = 120  #Game speed in milliseconds



#Function to convert cell coordinates to pixel coordinates


def cell_to_px(row, col):
    x0 = margin_side + col * cell_size
    y0 = margin_top + row * cell_size
    x1 = x0 + cell_size
    y1 = y0 + cell_size
    return x0, y0, x1, y1


#Function to draw the grid


def draw_grid(cv):
    for r in range(rows):
        for c in range(cols):
            x0, y0, x1, y1 = cell_to_px(r, c)
            cv.create_rectangle(x0, y0, x1, y1, outline="#9aa0a6")
    
    x0, y0, x1, y1 = cell_to_px(0, 0)
    X0, Y0, X1, Y1 = cell_to_px(rows-1, cols-1)
    cv.create_rectangle(x0, y0, X1, Y1, outline="#5f6368", width=2)


#Function to draw the snake


def draw_snake(cv, snake_cells):
    cv.delete("snake")
    for i, (r, c) in enumerate(snake_cells):
        x0, y0, x1, y1 = cell_to_px(r, c)
        pad = 3 if i == 0 else 5
        cv.create_rectangle(x0+pad, y0+pad, x1-pad, y1-pad, fill="#34a853" if i else "#0b8043", width=0, tags="snake")


#Advance one tick of the game

def step():
    global snake, direction, score, running, after_id, next_food

    if not running:
        return

    head_r, head_c = snake[0]
    dr, dc = direction
    new_head = (head_r + dr, head_c + dc)

    if (new_head[0] < 0 or new_head[0] >= rows or
        new_head[1] < 0 or new_head[1] >= cols or
        new_head in snake):
        running = False
        start_button.config(state="normal")
        return

    snake = [new_head] + snake[:-1]
    if new_head == next_food:
        score += 1
        score_label.config(text=f"Score: {score}")
        snake.append(snake[-1])  # Grow the snake
        canvas.delete("food")
        next_food = create_food(snake)

    draw_snake(canvas, snake)
    after_id = root.after(speed_ms, step)


#Funciton to create food


def create_food(snake_cells):
    while True:
        r = random.randint(0, rows - 1)
        c = random.randint(0, cols - 1)
        if (r, c) not in snake_cells:
            x0, y0, x1, y1 = cell_to_px(r, c)
            #canvas.create_oval(x0+5, y0+5, x1-5, y1-5, fill="#ea4335", width=0, tags="food")
            canvas.create_text((x0+x1)//2, (y0+y1)//2, text="🍎", font=("Arial", 16), tags="food", fill="red")
            return (r, c)


#Function to start the game


def start_game():
    global snake, direction, score, running, after_id, next_food

    if running:
        return

    snake = [(8, 8), (8, 7), (8, 6)]
    direction = (0, 1)
    score = 0
    score_label.config(text=f"Score: {score}")
    running = True
    start_button.config(state="disabled")
    canvas.delete("food")
    next_food = create_food(snake)

    draw_snake(canvas, snake)
    after_id = root.after(speed_ms, step)


#Function to stop the game


def stop_game():
    global running, after_id
    if running:
        running = False
        if after_id:
            root.after_cancel(after_id)
            after_id = None
        start_button.config(state="normal")


#Function to change the snake's direction


def on_key(event):
    global direction
    key = event.keysym
    if key == "Up" and direction != (1, 0):
        direction = (-1, 0)
    elif key == "Down" and direction != (-1, 0):
        direction = (1, 0)
    elif key == "Left" and direction != (0, 1):
        direction = (0, -1)
    elif key == "Right" and direction != (0, -1):
        direction = (0, 1)



#Set up the game


root = tk.Tk()
root.title("Snake Game")
root.resizable(False, False)
root.bind("<Key>", on_key)

top_bar = tk.Frame(root, bg="#202124")
top_bar.pack(fill="x", side="top")

bottom_bar = tk.Frame(root, bg="#202124")
bottom_bar.pack(fill="x", side="bottom")


#Create the canvas for the grid


canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bg="#202124", highlightthickness=0)
canvas.pack()


#Score label


score_label = tk.Label(top_bar, text="Score: 0", font=("Arial", 16), bg="#202124", fg="white")
score_label.pack(pady=10)


#Start and Quit buttons


bottom_bar.columnconfigure(0, weight=1)
bottom_bar.columnconfigure(1, weight=1)

start_button = tk.Button(bottom_bar, text="New game", font=("Arial", 16), command=start_game)
start_button.grid(row=0, column=0, sticky="ew", padx=40, pady=20, ipady=0, ipadx=10)

quit_button = tk.Button(bottom_bar, text="Quit", font=("Arial", 16),command=root.destroy)
quit_button.grid(row=0, column=1, sticky="ew", padx=40, pady=0, ipady=0)




#Initial drawing


draw_grid(canvas)
draw_snake(canvas, snake)
root.mainloop()