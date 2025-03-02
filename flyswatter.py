from tkinter import *
from random import *

def menu_toggle():
    global menu_mode, timer_running
    if menu_mode:
        menu_hide()
        timer_running = True
        update_timer()
    else:
        menu_show()
        timer_running = False

def key_handler(event):
    global menu_mode

    if event.keycode == KEY_ESC:
        menu_toggle()
        return

    if menu_mode:
        if event.keycode == KEY_UP:
            menu_up()
        elif event.keycode == KEY_DOWN:
            menu_down()
        elif event.keycode == KEY_ENTER:
            menu_enter()
        return

    if is_game_over:
        return

def menu_create(canvas):
    offset = 0
    for menu_option in menu_options:
        option_id = canvas.create_text(400, 200 + offset, anchor=CENTER, font=('Arial', '25'), text=menu_option,
                                       fill='black', state='hidden')
        menu_options_id.append(option_id)
        offset += 50

def menu_enter():
    if menu_current_index == 0:
        game_resume()
    elif menu_current_index == 1:
        new_game()
    elif menu_current_index == 2:
        game_exit()

def menu_show():
    global menu_mode
    menu_mode = True
    menu_update()

def menu_hide():
    global menu_mode
    menu_mode = False
    menu_update()

def menu_up():
    global menu_current_index
    if menu_current_index > 0:
        menu_current_index -= 1
    menu_update()

def menu_down():
    global menu_current_index
    if menu_current_index < len(menu_options) - 1:
        menu_current_index += 1
    menu_update()

def menu_update():
    global menu_options_id

    for element_id in menu_options_id:
        canvas.delete(element_id)
    menu_options_id.clear()

    if not menu_mode:
        return

    offset = 0
    for menu_index, menu_option in enumerate(menu_options):
        if menu_index == menu_current_index:
            option_id = canvas.create_text(360, 280 + offset, anchor=CENTER, font=('Arial', '30', 'bold'),
                                           text=menu_option, fill='black')
        else:
            option_id = canvas.create_text(360, 280 + offset, anchor=CENTER, font=('Arial', '25', 'bold'), text=menu_option,
                                           fill='black')
        menu_options_id.append(option_id)
        offset += 50

def game_resume():
    global menu_mode, timer_running
    if not is_game_over:
        menu_hide()
        timer_running = True
        update_timer()

def new_game():
    global score, is_game_over, gameover, time_left, timer_running, flies_killed

    score = 10
    is_game_over = False
    gameover = False

    time_left = 20
    flies_killed = 0
    time_left = 20

    timer_running = True

    update_points()
    update_timer_display()
    spawn()
    canvas.itemconfigure(text_id, text=f'Очки: {score}')
    canvas.itemconfigure(timer_id, text=f'Время: {time_left} секунд')
    menu_hide()

    update_timer()

def game_exit():
    exit()

def collision_detection(x, y):
    position = canvas.coords(npc_id)
    left = position[0]
    top = position[1]
    right = position[0] + npc_width
    bottom = position[1] + npc_height
    return left <= x <= right and top <= y <= bottom

def hit():
    global score, flies_killed
    score += 1
    flies_killed += 1
    update_points()
    spawn()

def missclick():
    global score
    score -= 1
    if score <= 0:
        game_over()
    else:
        update_points()

def spawn():
    for i in range(100):
        x = randint(1, 400)
        y = randint(1, 400)
        if abs(mouse_x - x) > 200 or abs(mouse_y - y) > 200:
            break
    canvas.moveto(npc_id, x, y)

def game_update():
    spawn()
    canvas.after(1000, game_update)

def update_points():
    canvas.itemconfigure(text_id, text=f'Очки: {score}')
    if score >= 100:
        canvas.itemconfigure(text_id, text=f'Молодец, ты выиграл! Тебе приз 🏆')

def game_over():
    global gameover, timer_running
    timer_running = False
    canvas.itemconfigure(text_id, text=f'Начни игру заново!')
    canvas.itemconfigure(timer_id, text=f'Убито {flies_killed} мух')
    gameover = True

def mouse_click(e):
    if gameover:
        return
    if collision_detection(e.x, e.y):
        animate_flyswatter()
        hit()
    else:
        animate_flyswatter()
        missclick()

def mouse_motion(event):
    global mouse_x, mouse_y
    mouse_x, mouse_y = event.x, event.y
    canvas.moveto(flyswatter_id, mouse_x - flyswatter_width // 2, mouse_y - flyswatter_height // 2)

def animate_flyswatter():
    def down():
        canvas.move(flyswatter_id, 0, 20)
        window.after(100, up)

    def up():
        canvas.move(flyswatter_id, 0, -20)

    down()

def load_background():
    global background_image
    file_path = "комната.png"
    background_image = PhotoImage(file=file_path)
    canvas.itemconfigure(background_id, image=background_image)


def update_timer():
    global time_left, timer_running
    if time_left > 0 and timer_running:
        time_left -= 1
        update_timer_display()
        canvas.after(1000, update_timer)
    elif time_left == 0:
        game_over()

def update_timer_display():
    canvas.itemconfigure(timer_id, text=f'Время: {time_left} секунд')

game_width = 720
game_height = 720

menu_mode = False
menu_options = ['Возврат в игру', 'Начать игру заново', 'Выход']
menu_current_index = 0
menu_options_id = []

KEY_UP = 87
KEY_DOWN = 83
KEY_ESC = 27
KEY_ENTER = 13

is_game_over = False
pause = False

npc_width = 120
npc_height = 95

score = 10
mouse_x = mouse_y = 0
gameover = False

time_left = 20
timer_running = True
flies_killed = 0

window = Tk()
window.title('Мухобойка')
window.resizable(width=False, height=False)

canvas = Canvas(window, width=game_width, height=game_height)

menu_create(canvas)

canvas.config(cursor="none")

background_image = PhotoImage(file="комната.png")
background_id = canvas.create_image(0, 0, image=background_image, anchor=NW)

npc_image = PhotoImage(file='муха1.png')
npc_id = canvas.create_image(0, 0, image=npc_image, anchor=NW)

flyswatter_image = PhotoImage(file='мухобойка.png')
flyswatter_width, flyswatter_height = 100, 100
flyswatter_id = canvas.create_image(0, 0, image=flyswatter_image, anchor=NW)

text_id = canvas.create_text(game_width - 10, 10, fill='black', font='Arial 20 bold', text=f'Очки: {score}', anchor=NE)
timer_id = canvas.create_text(10, 680, fill='black', font='Arial 20 bold', text=f'Время: {time_left} сек', anchor=NW)

window.bind('<KeyRelease>', key_handler)

canvas.bind('<Button>', mouse_click)
canvas.bind('<Motion>', mouse_motion)

canvas.pack()

game_update()
update_timer()

window.mainloop()
