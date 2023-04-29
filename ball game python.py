from itertools import cycle
from random import randrange
from tkinter import Canvas, Tk, messagebox, font

canvas_width = 800
canvas_height = 400

root = Tk()
root.title("Ball Catcher")
c = Canvas(root, width=canvas_width, height=canvas_height, background="deep sky blue")
c.create_rectangle(-5, canvas_height-100, canvas_width+5, canvas_height+5, fill="sea green", width=0)
c.create_oval(-100, -100, 100, 100, fill='orange', width=0)
c.pack()

color_cycle = cycle(["red", "light green", "pink", "yellow", "cyan"])
ball_width = 50
ball_height = 50
ball_score = 10
ball_speed = 400
ball_interval = 4000
difficulty = 0.90
catcher_color = "blue"
catcher_width = 100
catcher_height = 100
catcher_startx = canvas_width / 2 - catcher_width / 2
catcher_starty = canvas_height - catcher_height - 20
catcher_startx2 = catcher_startx + catcher_width
catcher_starty2 = catcher_starty + catcher_height

catcher = c.create_arc(catcher_startx, catcher_starty, catcher_startx2, catcher_starty2, start=200, extent=140, style="arc", outline=catcher_color, width=3)
game_font = font.nametofont("TkFixedFont")
game_font.config(size=18)


score = 0
score_text = c.create_text(10, 10, anchor="nw", font=game_font, fill="darkblue", text="Score: "+ str(score))

lives_remaining = 3
lives_text = c.create_text(canvas_width-10, 10, anchor="ne", font=game_font, fill="darkblue", text="Lives: "+ str(lives_remaining))

balls = []

def create_ball():
    x = randrange(10, 740)
    y = 40
    new_ball = c.create_oval(x, y, x+ball_width, y+ball_height, fill=next(color_cycle), width=0)
    balls.append(new_ball)
    root.after(ball_interval, create_ball)

def move_balls():
    for ball in balls:
        (ballx, bally, ballx2, bally2) = c.coords(ball)
        c.move(ball, 0, 10)
        if bally2 > canvas_height:
            ball_dropped(ball)
    root.after(ball_speed, move_balls)

def ball_dropped(ball):
    balls.remove(ball)
    c.delete(ball)
    lose_a_life()
    if lives_remaining == 0:
        messagebox.showinfo("Game Over!", "Final Score: "+ str(score))
        root.destroy()

def lose_a_life():
    global lives_remaining
    lives_remaining -= 1
    c.itemconfigure(lives_text, text="Lives: "+ str(lives_remaining))

def check_catch():
    (catcherx, catchery, catcherx2, catchery2) = c.coords(catcher)
    for ball in balls:
        (ballx, bally, ballx2, bally2) = c.coords(ball)
        if catcherx < ballx and ballx2 < catcherx2 and catchery2 - bally2 < 40:
            balls.remove(ball)
            c.delete(ball)
            increase_score(ball_score)
    root.after(100, check_catch)

def increase_score(points):
    global score, ball_speed, ball_interval
    score += points
    ball_speed = int(ball_speed * difficulty)
    ball_interval = int(ball_interval * difficulty)
    c.itemconfigure(score_text, text="Score: "+ str(score))

def move_left(event):
    (x1, y1, x2, y2) = c.coords(catcher)
    if x1 > 0:
        c.move(catcher, -20, 0)

def move_right(event):
    (x1, y1, x2, y2) = c.coords(catcher)
    if x2 < canvas_width:
        c.move(catcher, 20, 0)

c.bind("<Left>", move_left)
c.bind("<Right>", move_right)
c.focus_set()
root.after(1000, create_ball)
root.after(1000, move_balls)
root.after(1000, check_catch)
root.mainloop()
