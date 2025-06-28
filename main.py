import pgzrun

WIDTH = 870
HEIGHT = 650
TITLE = "QUIZ GAME"

marquee_box = Rect(0,0,880,80)
skip_box = Rect(0,0,150,330)
timer_box = Rect(0,0,150,150)
question_box = Rect(0,0,650,150)
ans_box1 = Rect(0,0,300,150)
ans_box2 = Rect(0,0,300,150)
ans_box3 = Rect(0,0,300,150)
ans_box4 = Rect(0,0,300,150)
score_box = Rect(0,0,150,50)

score = 0
timer_left = 5
marquee_msg = ""
question_file_name = "questions.txt"
is_game_over = False

answer_boxes = [ans_box1,ans_box2,ans_box3,ans_box4]
questions = []
question_count = 0
question_index = 0

marquee_box.move_ip(0,0)
skip_box.move_ip(700,270)
timer_box.move_ip(700,100)
question_box.move_ip(20,100)
ans_box1.move_ip(20,270)
ans_box2.move_ip(370,270)
ans_box3.move_ip(20,450)
ans_box4.move_ip(370,450)
score_box.move_ip(700,50)

def draw():
    global marquee_msg
    screen.clear()
    screen.fill(color = "#FF5666")
    screen.draw.filled_rect(marquee_box, "#FF5666")
    screen.draw.filled_rect(skip_box, "#A50104")
    screen.draw.filled_rect(timer_box, "#BA3B46")
    screen.draw.filled_rect(score_box, "#FF5666")
    screen.draw.filled_rect(question_box, "#F4A698")
    for answer_box in answer_boxes:
        screen.draw.filled_rect(answer_box, "#ED217C")

    marquee_msg = f"Welcome to quizmaster... Q: {question_index} out of {question_count}"
    screen.draw.textbox(marquee_msg, marquee_box, color = "#1B998B")
    screen.draw.textbox("SKIP", skip_box, color = "#1B998B", angle = -90)
    screen.draw.textbox(f"{timer_left}", timer_box, color = "#0496FF", shadow = (0.8,0.8), scolor = "#006BA6")
    screen.draw.textbox(f"Score: {score}", score_box, color = "#49A078")

    screen.draw.textbox(question[0].strip(), question_box, color = "#61C9A8", shadow = (0.8,0.8), scolor = "#B6C2D9")
    index = 1
    for answer_box in answer_boxes:
        screen.draw.textbox(question[index].strip(), answer_box, color = "#7DBA84")
        index = index + 1

def update():
    move_marquee()

def move_marquee():
    marquee_box.x = marquee_box.x - 2
    if marquee_box.right < 0:
        marquee_box.left = WIDTH

def read_question_file():
    global question_count, questions
    q_file = open(question_file_name, "r")
    for question in q_file:
        questions.append(question)
        question_count = question_count + 1
    q_file.close()

def read_next_question():
    global question_index
    question_index = question_index + 1
    return questions.pop(0).split(",")

def on_mouse_down(pos):
    index = 1
    for answer_box in answer_boxes:
        if answer_box.collidepoint(pos):
            if index == int(question[5]):
                correct_answer()
            else:
                game_over()
        index = index + 1
    if skip_box.collidepoint(pos):
        skip_question()

def correct_answer():
    global score, question, timer_left, questions
    score = score + 1
    if questions:
        question = read_next_question()
        timer_left = 5
    else:
        game_over()

def game_over():
    global question, timer_left, is_game_over, msg
    msg = f"GAME OVER! you answered {score} questions correctly!"
    question = [msg, "-", "-", "-", "-", 5]
    timer_left = 0
    is_game_over = True

def skip_question():
    global question, timer_left
    if questions and not is_game_over:
        question = read_next_question()
        timer_left = 5
    else:
        game_over()

def update_time():
    global timer_left
    if timer_left:
        timer_left = timer_left - 1
    else:
        game_over()

read_question_file()
question = read_next_question()
clock.schedule_interval(update_time, 1)

pgzrun.go()