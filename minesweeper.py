import random
import pygame
import tkinter as tk
from PIL import Image, ImageTk

def play_sound():
    pygame.mixer.init()
    sound = pygame.mixer.Sound("burst.wav")
    sound.play()

def open_gif():
    root = tk.Tk()
    root.geometry("800x600")

    gif_path = "animation.gif"
    gif = Image.open(gif_path)
    frames = gif.n_frames

    canvas = tk.Canvas(root, width=gif.width, height=gif.height, bg="black")
    canvas.pack()

    delay = 6
    def show_next_frame(frame):
        gif.seek(frame)
        gif_frame = ImageTk.PhotoImage(gif)
        canvas.create_image(0, 0, image=gif_frame, anchor=tk.NW)
        root.update()
        canvas.delete("all")

        if frame < frames - 1:
            root.after(delay, show_next_frame, frame + 1)
        else:
            root.after(2000, root.destroy)

    show_next_frame(0)

    root.lift()
    root.attributes("-topmost", True)

    root.mainloop()


SIZE_BATTLE_FIELD = 8
LETTERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
L = '   A   B   C   D   E   F   G   H'
NUMS = ['1','2','3','4','5','6','7','8']
EMPTY = ' '
SQUARE = '■'
BOMB = '*'
BATTLE_FIELD_USER = []
BATTLE_FIELD_REAL = []

def createBattleField_U():
    for row in range(SIZE_BATTLE_FIELD):
        tmp = []
        for col in range(SIZE_BATTLE_FIELD):
            tmp.append(EMPTY)
        BATTLE_FIELD_USER.append(tmp)

def createBattleField_R():
    for row in range(SIZE_BATTLE_FIELD):
        tmp = []
        for col in range(SIZE_BATTLE_FIELD):
            tmp.append(EMPTY)
        BATTLE_FIELD_REAL.append(tmp)

def printBattleFieldU():
    print(L)
    for i, row in enumerate(BATTLE_FIELD_USER):
        print(NUMS[i], end=' ')
        for j in row:
            if j == SQUARE:
                print(f'\x1b[32m {j} \033[0m', end=' ')
            elif j == BOMB:
                print(f'\x1b[31m {j} \033[0m', end=' ')
            else:
                print(f'\x1b[33m '" "' \033[0m', end=' ')
        print(NUMS[i])
    print(L)


def printBattleFieldR():
    with open('small_hint.txt', 'w') as file:
        file.write(L+'\n')
        for i, row in enumerate(BATTLE_FIELD_REAL):
            line = ' '.join(f' {j} ' for j in row)
            file.write(f'{NUMS[i]} {line} {NUMS[i]}\n')
        file.write(L)

def bombsSet(AMOUNT):
    for i in range(AMOUNT):
        while True:
            pos_h = random.randint(1, SIZE_BATTLE_FIELD-1)
            pos_v = random.randint(1, SIZE_BATTLE_FIELD-1)
            if BATTLE_FIELD_REAL[pos_h][pos_v] == EMPTY:
                BATTLE_FIELD_REAL[pos_h][pos_v] = BOMB
                break

def goTo():
    while True:
        your_pos_h = input("Enter horizontal position (from A to H) \n-> ")
        your_pos_v = input("Enter vertical position (from 1 to 8) \n-> ")

        if your_pos_h not in LETTERS or your_pos_v not in NUMS:
            print("Invalid inputs! Try again!")
            continue

        pos_h = LETTERS.index(your_pos_h)
        pos_v = int(your_pos_v) - 1

        if BATTLE_FIELD_USER[pos_v][pos_h] == SQUARE:
            print("Position already selected. Please try again.")
            continue

        if BATTLE_FIELD_REAL[pos_v][pos_h] == BOMB :
            BATTLE_FIELD_USER[pos_v][pos_h] = BOMB
            print("Game Over! You hit a bomb.")
            pygame.init()
            play_sound()

            open_gif()
            printBattleFieldU()
            pygame.quit()
            return

        if BATTLE_FIELD_USER[pos_v][pos_h] == EMPTY and BATTLE_FIELD_REAL[pos_v][pos_h] == EMPTY:
            BATTLE_FIELD_USER[pos_v][pos_h] = SQUARE
            BATTLE_FIELD_REAL[pos_v][pos_h] = SQUARE
            printBattleFieldU()

def startGame():
    createBattleField_U()
    createBattleField_R()
    printBattleFieldU()
    bombsSet(8)
    printBattleFieldR()
    goTo()

