import pygame
from pygame import mixer 
pygame.init()

WIDTH = 1400
HEIGHT = 800
NEW_WIDTH = 1400
NEW_HEIGHT = 845

black = (0, 0, 0)
white = (255, 255, 255)
gray = (128, 128, 128)
hover_gray = (110, 110, 110)
light_gray = (211, 211, 211)
green = (0, 255, 0)
hover_green = (0, 200, 0)
red = (200, 0, 0)
gold = (212, 175, 55)
blue = (0, 255, 255)

screen = pygame.display.set_mode([NEW_WIDTH, NEW_HEIGHT])
pygame.display.set_caption('Beat Maker')
title_font = pygame.font.Font('freesansbold.ttf', 50)
label_font = pygame.font.Font('freesansbold.ttf', 32)
small_font = pygame.font.Font('freesansbold.ttf', 15)

for event in pygame.event.get():
    screen.fill(light_gray)

save_active = False
load_mode = False
beats = 8
fps = 60
bpm = 160
active_length = 0
active_beat = 1
beat_changed = True
timer = pygame.time.Clock()
instruments = 6
boxes = []
play_pause_val = -1
play_val = False

try:
    with open('data.txt', 'r+') as data:
        x = data.readlines()
except:
    with open('data.txt', 'w+') as data:
        pass
else:
    pass
finally:
    pass

play_pause_hover = 1
tempo_hover = 1
num_beats_hover = 1

#loading in sounds
hi_hat = mixer.Sound('basickit/hi hat.wav')
bass = mixer.Sound('basickit/bass.wav')
crash = mixer.Sound('basickit/cymbal.wav')
snare = mixer.Sound('basickit/snare.WAV')
tom = mixer.Sound(r'basickit/tom.WAV')
clap = mixer.Sound('basickit/clap.wav')
pygame.mixer.set_num_channels(instruments*3)

def hover_func(button, mouse_x, mouse_y):
    box_x = button[0]
    box_y = button[1] 
    box_width = button[2]
    box_height = button[3]
    if box_x <= mouse_x <= box_x + box_width and box_y <= mouse_y <= box_y + box_height:
        output = -1
    else:
        output = 1
    return(output)
#========================================================
def user_tempo_input():
    user_input = ""
    input_active = True
    while input_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    user_input = user_input[:-1]
                else:
                    user_input += event.unicode

        # Clear the screen

        # Display the input box
        input_box = pygame.Rect(415, 720+45, 200, 40)
        pygame.draw.rect(screen, (200, 200, 200), input_box, 0, 5)
        pygame.draw.rect(screen, white, input_box, 3)
        # Display the user input
        text_surface = label_font.render(user_input, True, white)
        screen.blit(text_surface, (input_box[0] + 5, input_box[1] + 5))

        pygame.display.flip()

    return user_input
#========================================================
def user_num_beats_input():
    user_input = ""
    input_active = True
    while input_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    user_input = user_input[:-1]
                else:
                    user_input += event.unicode

        # Clear the screen

        # Display the input box
        input_box = pygame.Rect(630, 720+45, 200, 40)
        pygame.draw.rect(screen, (200, 200, 200), input_box, 0, 5)
        pygame.draw.rect(screen, white, input_box, 2)

        # Display the user input
        text_surface = label_font.render(user_input, True, white)
        screen.blit(text_surface, (input_box[0] + 5, input_box[1] + 5))

        pygame.display.flip()
    return user_input
#========================================================
def save_menu(tempo, num_beats, clicked, cur_name = ""):
    screen.fill(black)
    user_input = cur_name
    samename_text = label_font.render("This save name already exists, would you like to replace ? (Y/N)", True, white)
    save_line = f'tempo: {tempo}, num_beats: {num_beats}, clicked: {clicked}, '
    # print(save_line)
    save_run = True
    with open('data.txt', 'r+') as data:
        data.seek(0)
        saves = data.readlines()
    # print(saves)
    while save_run:
        names = []
        for i in saves:
            name_data = (i.split(',')[0])
            # print(name_data)
            name = name_data.split(':')[1].strip()
            names.append(name)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    name = user_input
                    save_line = f'name: {user_input}, {save_line}\n'
                    if user_input not in names:
                        save_run = False
                        saves.append(save_line)
                        # with open('data.txt', 'a+') as data:
                        #     data.write(f'{save_line}\n')
                    else:
                        x = names.index(user_input)
                        minirun = True
                        while minirun:
                            screen.blit(samename_text, (200, HEIGHT-300))
                            pygame.display.flip()
                            for event in pygame.event.get():
                                if event.type == pygame.KEYDOWN:
                                    if event.key == pygame.K_y:
                                        minirun = False
                                        save_run = False
                                        saves[x] = save_line
                                    if event.key == pygame.K_n:
                                        minirun = False
                                        save_run = False
                elif event.key == pygame.K_ESCAPE:
                    save_run = False
                elif event.key == pygame.K_BACKSPACE:
                    user_input = user_input[:-1]
                else:
                    user_input += event.unicode
            if event.type == pygame.QUIT:
                pygame.quit()

        
        input_box = pygame.Rect(200, HEIGHT-450, 1000, 40)
        text_surface = label_font.render(user_input, True, white)
        pygame.draw.rect(screen, gray, input_box, 0, 5)
        screen.blit(text_surface, (input_box[0]+5, input_box[1]+5))
        pygame.display.flip()
    with open('data.txt', 'w+') as data:
        data.writelines(saves)
    
    return(name)
#========================================================
def load_menu():
    saves = []
    names = []
    with open("data.txt", "r+") as data:
        data.seek(0)
        saves = data.readlines()
    for i in saves:
        name_data = (i.split(',')[0])
        name = name_data.split(':')[1].strip()
        names.append(name)
    num_saves = len(saves)
    load_menu_hover = [1 for _ in range(num_saves)]
    del_hover = [1 for _ in range(num_saves)]
    run = True
    while run:
        names = []
        with open("data.txt", 'r+') as data:
            saves = data.readlines()
        for i in saves:
            name_data = (i.split(',')[0])
            name = name_data.split(':')[1].strip()
            names.append(name)
        num_saves = len(saves)
        save_rectangles = []
        delete_rectangles = []
        mouse_x, mouse_y = (pygame.mouse.get_pos())
        screen.fill(black)
        for i in range(num_saves):
            if load_menu_hover[i] == -1:
                color = hover_gray
                text_color = gold
            elif del_hover[i] == -1:
                del_color = hover_gray
                del_text_color = gold
            else:
                color = gray
                del_color = gray
                text_color = white
                del_text_color = white
            name_text = label_font.render(names[i], True, text_color)
            del_text = small_font.render('Delete', True, del_text_color)
            del_box = pygame.Rect(720, i*50 + 10, 100, 40)
            box = pygame.Rect(20, i*50 + 10, WIDTH/2 - 10, 40)
            rect = pygame.draw.rect(screen, color, box, 0, 5)
            del_rect = pygame.draw.rect(screen, del_color, del_box, 0, 5)
            screen.blit(name_text, (30, i*50 + 14))
            screen.blit(del_text, (745, i*50 + 22))
            save_rectangles.append((rect, i))
            delete_rectangles.append(del_rect)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i in range(len(save_rectangles)):
                    if save_rectangles[i][0].collidepoint(event.pos):
                        first_split = saves[i].split(',')
                        second_split = saves[i].split(':')
                        for i in first_split:
                            try:
                                name = first_split[0].split(':')[1].strip()
                                tempo = first_split[1].split(':')[1].strip()
                                num_beats = first_split[2].split(':')[1].strip()
                                clicked = second_split[4].strip()[0:-1]
                                clicked = eval(clicked)
                                # print(clicked)
                            except:
                                pass
                            else:
                                pass
                            finally:
                                pass
                            run = False
                for i in range(len(delete_rectangles)):
                    if delete_rectangles[i].collidepoint(event.pos):
                        del saves[i]
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
            for i in range(len(save_rectangles)):
                load_menu_hover[i] = hover_func(save_rectangles[i][0], mouse_x, mouse_y)
                del_hover[i] = hover_func(delete_rectangles[i], mouse_x, mouse_y)
        with open("data.txt", 'w+') as data:
            data.writelines(saves)
        pygame.display.flip()
    # print(save_rectangles)
    try:
        return(tempo, num_beats, clicked, name)
    except:
        pass
    else:
        pass
    finally:
        pass
#========================================================
def play_notes(beats, clicked):
    for i in range(len(clicked)):
        if clicked[i][active_beat-1] == 1:
            if i == 0:
                hi_hat.play()
            if i == 1:
                snare.play()
            if i == 2:
                bass.play()
            if i == 3:
                crash.play()
            if i == 4:
                clap.play()
            if i == 5:
                tom.play()
#========================================================
def update_clicked_hover(beats, instruments):
    clicked = [[-1 for _ in range(beats)] for _ in range(instruments)] #initialize clicked and hover matrices
    hover = [[1 for _ in range(beats)] for _ in range(instruments)]  
    return(clicked, hover)

clicked = [[-1 for _ in range(beats)] for _ in range(instruments)] #initialize clicked and hover matrices
hover = [[1 for _ in range(beats)] for _ in range(instruments)]

def draw_grid(beat, beats, clicked, hover, cur_save):
    B = 100
    D = 120
    left_box = pygame.draw.rect(screen, gray, [0, 0+D-25, 200, HEIGHT -200], 5)
    # bottom_box = pygame.draw.rect(screen, gray, [0, HEIGHT - 200, WIDTH, 200], 5)
    boxes = []
    colors = [gray, white, gray]
    hi_hat_text = label_font.render('Hi Hat', True, white)
    screen.blit(hi_hat_text, (30, 30+B))
    snare_text = label_font.render('Snare', True, white)
    screen.blit(snare_text, (30, 130+B))
    kick_text = label_font.render('Bass', True, white)
    screen.blit(kick_text, (30, 230+B))
    crash_text = label_font.render('Crash', True, white)
    screen.blit(crash_text, (30, 330+B))
    clap_text = label_font.render('Clap', True, white)
    screen.blit(clap_text, (30, 430+B))
    floor_text = label_font.render('Floor Tom', True, white)
    screen.blit(floor_text, (30, 530+B))

    title_text = title_font.render('Beat Maker', True, white)
    screen.blit(title_text, (25, 25))
    beat_count_text = f'Beat Count : {str(beat)}'

    beat_count = small_font.render(beat_count_text, True, white)
    screen.blit(beat_count, (20, HEIGHT-50))

    cur_save_text = small_font.render(f'current save: {cur_save}', True, white)
    screen.blit(cur_save_text, (1200, 70))

    for i in range(6):
        pygame.draw.line(screen, gray, (0, (i*100) + 100+D-25), (195, (i*100)-25 + 100+D), 5 )

    for i in range(beats):
        color = gray
        for j in range(instruments):
            if clicked[j][i] == -1:
                if hover[j][i] == -1:
                    color = hover_gray
                    ring_color = gold
                else:
                    color = gray
                    ring_color = red
            if clicked[j][i] == 1:
                if hover[j][i] == -1:
                    color = hover_green
                    ring_color = gold
                else:
                    color = green
                    ring_color = red
                
            D = 95

            rect = pygame.draw.rect(screen, color, [i * ((WIDTH-200)//beats) + 205, j*100 + 5+D , ((WIDTH - 200) // beats) -10, ((HEIGHT - 200)//instruments)-10], 0, 1)

            rect = pygame.draw.rect(screen, ring_color, [i * ((WIDTH-200)//beats) + 200, j*100+D, ((WIDTH - 200) // beats), ((HEIGHT - 200)//instruments)], 5, 5)

            rect = pygame.draw.rect(screen, black, [i * ((WIDTH-200)//beats) + 200, j*100+D, ((WIDTH - 200) // beats), ((HEIGHT - 200)//instruments)], 3, 5)
            
            boxes.append((rect, (i, j)))

        if beat != 0:
            active = pygame.draw.rect(screen, blue, [(beat-1) * ((WIDTH - 200)//beats) + 200, 0+D, ((WIDTH - 200)//beats), instruments*100], 2, 5) 
    return (boxes, clicked, hover)
#========================================================
def play_pause(button_val, playing, hover):
    if button_val == 1: 
        playing = True
        if hover == -1:
            color = hover_green
        else:
            color = green
        text = label_font.render('Playing', True, white)
    if button_val == -1:
        if hover == -1:
            color = hover_gray
        else:
            playing = False
            color = gray 
        text = label_font.render('Paused', True, white)
    subtext = small_font.render('(space)', True, light_gray)


    X = 200
    Y = 720    
    button = pygame.draw.rect(screen, color, [X, Y, 200, 100], 0, 3)
    screen.blit(subtext, (X+10, Y+40))
    screen.blit(text, (X+10, Y+10))
    
    return (button, playing, hover)
#========================================================
def tempo(bpm, hover):
    text1 = label_font.render("Tempo:", True, white)
    text2 = label_font.render(str(bpm), True, gold)

    if hover == -1:
        color = hover_gray
    else:
        color = gray
    
    X = 415
    Y = 720

    button = pygame.draw.rect(screen, color, [X, Y, 200, 100], 0, 3)
    screen.blit(text1, (X+10, Y+10))
    screen.blit(text2, (X+10, Y+50))
    return(button)
#========================================================
def num_beats(beats, hover):
    text1 = label_font.render("# of beats:", True, white)
    text2 = label_font.render(str(beats), True, gold)

    if hover == -1:
        color = hover_gray
    else:
        color = gray

    X = 630
    Y = 720
    button = pygame.draw.rect(screen, color, [X, Y, 200, 100], 0, 3)
    screen.blit(text1, (X+15, Y+10))
    screen.blit(text2, (X+15, Y+50))   
    return(button)
#========================================================
save_hover = 1
def save(hover):
    text1 = label_font.render("Save", True, white)
    X = 1215
    Y = 720
    if hover == -1:
        color = hover_gray
    else:
        color = gray
    button = pygame.draw.rect(screen, color, [X, Y, 180, 50], 0, 3)
    screen.blit(text1, (X+15, Y+8))
    return(button)
load_hover = 1
def load(hover):
    text1 = label_font.render("Load", True, white)
    X = 1215
    Y = 775
    if hover == -1:
        color = hover_gray
    else:
        color = gray
    button = pygame.draw.rect(screen, color, [X, Y, 180, 50], 0, 3)
    screen.blit(text1, (X+15, Y+8))
    return(button)
#======================================================== 
clear_hover = 1
def clear_button(hover):
    text1 = label_font.render("Clear", True, white)
    X = 850
    Y = 720
    if hover == -1:
        color = hover_gray
    else:
        color = gray
    button = pygame.draw.rect(screen, color, [X, Y, 120, 100], 0, 3)
    screen.blit(text1, (X+13, Y+12))
    return(button)
#======================================================== 
name = ""
#MAIN CODE
run = True
while run:                                                                                                                                                    
    timer.tick(fps)
    screen.fill((75, 75, 75))
    draw_grid_data = draw_grid(active_beat, beats, clicked, hover, name)
    boxes = draw_grid_data[0]
    clicked = draw_grid_data[1]
    hover = draw_grid_data[2]

    save_button = save(save_hover)
    load_button = load(load_hover)

    mouse_x, mouse_y = (pygame.mouse.get_pos())

    # for i in boxes:
    #     x = i[1][0]
    #     y = i[1][1]
    #     if (hover_func(i[0], mouse_x, mouse_y)) == -1:
    #         hover[y][x] = -1
    #     else:
    #         hover[y][x] = 1

    play_pause_button = play_pause(play_pause_val, play_val, play_pause_hover)
    
    if beat_changed:
        play_notes(beats, clicked)
        beat_changed = False

    num_beats_button = num_beats(beats, num_beats_hover)
    tempo_button = tempo(bpm, tempo_hover)
    clear = clear_button(clear_hover)

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN: 
            if event.key == pygame.K_SPACE:
                play_pause_val *= -1
        if event.type == pygame.QUIT:
            run = False
        #hover code for the control panel buttons
        play_pause_hover = hover_func(play_pause_button[0], mouse_x, mouse_y)
        tempo_hover = hover_func(tempo_button, mouse_x, mouse_y)
        num_beats_hover = hover_func(num_beats_button, mouse_x, mouse_y)
        save_hover = hover_func(save_button, mouse_x, mouse_y)
        load_hover = hover_func(load_button, mouse_x, mouse_y)
        clear_hover = hover_func(clear, mouse_x, mouse_y)

        for i in boxes: #hover color for the grid
            x = i[1][0]
            y = i[1][1]
            if (hover_func(i[0], mouse_x, mouse_y)) == -1:
                hover[y][x] = -1
            else:
                hover[y][x] = 1

        if event.type == pygame.MOUSEBUTTONDOWN:  #IF MOUSE IS CLICKED 
            for i in range(len(boxes)):
                if boxes[i][0].collidepoint(event.pos):
                    print(boxes[i][1])
                    coords = boxes[i][1]
                    clicked[coords[1]][coords[0]] *= -1

            if play_pause_button[0].collidepoint(event.pos):
                play_pause_val *= -1
                print(play_pause_button[1])
            
            if save_button.collidepoint(event.pos):
                name = (save_menu(bpm, beats, clicked, name))
                print(name)

            if clear.collidepoint(event.pos):
                clicked = [[-1 for _ in range(beats)] for _ in range(instruments)]

            
            if load_button.collidepoint(event.pos):
                try:
                    load_output = (load_menu())
                    name = load_output[3]
                    bpm = int(load_output[0])
                    beats = int(load_output[1])
                    clicked = load_output[2]
                    hover = [[1 for _ in range(beats)] for _ in range(instruments)]
                except:
                    pass
                else:
                    pass
                finally:
                    pass

            if tempo_button.collidepoint(event.pos):
                try:
                    bpm = int(user_tempo_input())
                except:
                    pass
                else:
                    pass
                finally:
                    pass

            if num_beats_button.collidepoint(event.pos):
                try:
                    beats = int(user_num_beats_input())
                    print(beats)
                except:
                    pass
                else:
                    clicked = [[-1 for _ in range(beats)] for _ in range(instruments)]
                    hover = [[1 for _ in range(beats)] for _ in range(instruments)]

                finally:
                    pass
        
    beat_length = 1600//bpm

    if play_pause_button[1] == True:
        if active_length < beat_length:
            active_length += 1
        else:
            active_length = 1
            if active_beat < beats:
                active_beat += 1
                beat_changed = True
            else:
                active_beat = 1
                beat_changed = True
    if play_pause_button[1] == False:
        active_beat = 0

    pygame.display.flip()

pygame.quit()

