from tkinter import *
import random

GAME_WIDTH = 800
GAME_HEIGHT = 600
SPEED = 100
SPACE_SIZE = 30
BODY_PARTS = 3
SNAKE_COLOR = "#008000"
FOOD_COLOR = "#FF0000"
FOOD_COLOR2 = "#0000FF"
FOOD_COLOR3 = "#FFFF00"
BACKGROUND_COLOR = "#000000"


class Snake:
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        for i in range(0, BODY_PARTS):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")
            self.squares.append(square)


class Food:
    def __init__(self, color):
        self.color = color
        self.spawn_food()

    def spawn_food(self):
        x = random.randint(0, int(GAME_WIDTH / SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, int(GAME_HEIGHT / SPACE_SIZE) - 1) * SPACE_SIZE
        self.coordinates = [x, y]
        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=self.color, tag="food")


class Food2(Food):
    def __init__(self):
        super().__init__(FOOD_COLOR2)

    def spawn_food(self):
        x = random.randint(0, int(GAME_WIDTH / SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, int(GAME_HEIGHT / SPACE_SIZE) - 1) * SPACE_SIZE
        self.coordinates = [x, y]
        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=self.color, tag="food2")


class Food3(Food):
    def __init__(self):
        super().__init__(FOOD_COLOR3)

    def spawn_food(self):
        x = random.randint(0, int(GAME_WIDTH / SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, int(GAME_HEIGHT / SPACE_SIZE) - 1) * SPACE_SIZE
        self.coordinates = [x, y]
        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=self.color, tag="food3")


class Obstacle:
    def __init__(self):
        self.color = "#808080"
        self.coordinates = []
        self.squares = []
        self.spawn_obstacle()

    def spawn_obstacle(self):
        x = random.randint(0, int(GAME_WIDTH / SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, int(GAME_HEIGHT / SPACE_SIZE) - 1) * SPACE_SIZE
        self.coordinates = [x, y]
        square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=self.color, tag="obstacle")
        self.squares.append(square) 

def create_obstacle():
    if random.random() < obstacle_chance:
        obstacle = Obstacle()
        obstacles.append(obstacle)

def next_turn(snake, food, food2, food3):  
    global direction, score, SPEED, obstacles

    x, y = snake.coordinates[0]

    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    snake.coordinates.insert(0, (x, y))

    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)

    snake.squares.insert(0, square)

    del snake.coordinates[-1]

    if x == food.coordinates[0] and y == food.coordinates[1]:
        score += 1
        label.config(text="Score:{}".format(score))
        canvas.delete("food")
        food.spawn_food()
    elif x == food2.coordinates[0] and y == food2.coordinates[1]:
        score += 2
        label.config(text="Score:{}".format(score))
        canvas.delete("food2")
        food2.spawn_food()
    elif x == food3.coordinates[0] and y == food3.coordinates[1]:
        score += 3
        label.config(text="Score:{}".format(score))
        SPEED -= 5  # Increase speed
        canvas.delete("food3")
        food3.spawn_food()
    else:
        del snake.squares[-1]
        canvas.delete(snake.squares[-1])

    if score % 5 == 0:
        create_obstacle()

    if check_collisions(snake):
        game_over()
    else:
        window.after(SPEED, next_turn, snake, food, food2, food3)


    

def change_direction(new_direction):
    global direction

    if new_direction == 'left':
        if direction != 'right':
            direction = new_direction
    elif new_direction == 'right':
        if direction != 'left':
            direction = new_direction
    elif new_direction == 'up':
        if direction != 'down':
            direction = new_direction
    elif new_direction == 'down':
        if direction != 'up':
            direction = new_direction


def check_collisions(snake):
    x, y = snake.coordinates[0]

    if x < 0 or x >= GAME_WIDTH:
        return True
    elif y < 0 or y >= GAME_HEIGHT:
        return True


    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True

  
    for obstacle in obstacles:
        if x == obstacle.coordinates[0] and y == obstacle.coordinates[1]:
            return True

    return False



def game_over():
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width() / 2, canvas.winfo_height() / 2,
                       font=('consolas', 70), text="Game Over", fill="Red", tag="gameover")


window = Tk()
window.title("Snake Game")
window.resizable(False, False)

score = 0
direction = 'down'

label = Label(window, text="Score: {}.".format(score), font=('consolas', 40))
label.pack()

canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

window.update()

window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))

snake = Snake()
food = Food(FOOD_COLOR)
food2 = Food2()
food3 = Food3()

obstacle_chance = 0.05
obstacles = []

def create_obstacle():
    if random.random() < obstacle_chance:
        obstacle = Obstacle()
        obstacles.append(obstacle)

create_obstacle()
next_turn(snake, food, food2, food3)

window.mainloop()
