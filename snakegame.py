import turtle
import random
import tkinter as tk
from tkinter import messagebox

w = 500
h = 500
food_size = 15
delay = 100
score = 0
 
offsets = {
    "up": (0, 20),
    "down": (0, -20),
    "left": (-20, 0),
    "right": (20, 0)
}
 
def reset():
    global snake, snake_dir, food_position, pen
    snake = [[0, 0], [20, 0], [40, 0], [60, 0], [80, 0]]
    snake_dir = "right"
    food_position = get_random_food_position()
    food.goto(food_position)
    move_snake() if(show_start()) else exit()

def show_start():
    response = messagebox.askquestion("Game Start!!", "Are you ready to feed..? :)")
    return (True if response == 'yes' else False)

def show_popup():
    global score, highScore
    points = "Your Score: {}".format(score)
    with open("highScore.txt","r") as f:
        highScore = f.read()
    if(score>int(highScore)):
        highScore = str(score)
        with open("highScore.txt", "w") as f:
            f.write(highScore)
    highPoints = "High Score: {}".format(highScore)
    text = "Did I EAT myself!!! :(\n***GAME OVER***\n\n" + points +"\n" + highPoints
    messagebox.showinfo("OOPS!!", text)
    response = messagebox.askquestion("Restart", "Do you want to continue..?")
    reset() if response == "yes" else exit()

def draw_score():
    pen.goto(-w / 2 + 10, h / 2 - 20)
    pen.clear()
    pen.write("Score: {}".format(score), align="left", font=("Arial", 12, "bold"))

def move_snake():
    global snake_dir
    new_head = snake[-1].copy()
    new_head[0] = snake[-1][0] + offsets[snake_dir][0]
    new_head[1] = snake[-1][1] + offsets[snake_dir][1]
 
    if new_head in snake[:-1]:
        show_popup()
    else:
        snake.append(new_head)
     
        if not food_collision():
            snake.pop(0)
        
        if snake[-1][0] > w / 2:
            snake[-1][0] -= w
        elif snake[-1][0] < - w / 2:
            snake[-1][0] += w
        elif snake[-1][1] > h / 2:
            snake[-1][1] -= h
        elif snake[-1][1] < -h / 2:
            snake[-1][1] += h

        pen.clearstamps()
         
        for segment in snake:
            pen.goto(segment[0], segment[1])
            pen.stamp()
         
        screen.update()
 
        turtle.ontimer(move_snake, delay)
 
def food_collision():
    global food_position, score
    if get_distance(snake[-1], food_position) < 15:
        food_position = get_random_food_position()
        food.goto(food_position)
        score += 10
        draw_score()
        return True
    return False
 
def get_random_food_position():
    x = random.randint(- w // 2 + food_size, w // 2 - food_size)
    y = random.randint(- h // 2 + food_size, h // 2 - food_size)
    return (x, y)
 
def get_distance(pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2
    distance = ((y2 - y1) ** 2 + (x2 - x1) ** 2) ** 0.5
    return distance

def go_up():
    global snake_dir
    if snake_dir != "down":
        snake_dir = "up"
 
def go_right():
    global snake_dir
    if snake_dir != "left":
        snake_dir = "right"
 
def go_down():
    global snake_dir
    if snake_dir!= "up":
        snake_dir = "down"
 
def go_left():
    global snake_dir
    if snake_dir != "right":
        snake_dir = "left"
 
screen = turtle.Screen()
screen.setup(w, h)
screen.title("Hit The Food Buddy")
screen.bgcolor("black")
screen.tracer(0)
 
pen = turtle.Turtle("square")
pen.color("white")
pen.penup()
 
food = turtle.Turtle()
food.shape("circle")
food.color("yellow")
food.shapesize(food_size / 15)
food.penup()
 
screen.listen()
screen.onkey(go_up, "Up")
screen.onkey(go_right, "Right")
screen.onkey(go_down, "Down")
screen.onkey(go_left, "Left")
 
root = tk.Tk()
root.withdraw()  

reset()
draw_score()
turtle.done()
