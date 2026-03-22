from flask import Flask, render_template, request, session, url_for, redirect
import random

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# list for quiz
questions_animals = [
    {
        "question": "Which one is a blue whale?",
        "answer": "blue_whale.png"
    },
    {
        "question": "Which one is a coral reef?",
        "answer": "coral_reef.png"
    },
    {
        "question": "Which one is a sperm whale?",
        "answer": "sperm_whale.png"
    },
]

images_all_animals = ["blue_whale.png", "coral_reef.png", "sperm_whale.png"]
questions_asked= []

@app.route('/')
def root():
    return render_template("index.html")

@app.route('/plastic_game')
def plastic_game():
    return render_template('game.html')

@app.route('/start_quiz')
def start_quiz():
    global questions_asked
    questions_asked= []
    quiz_id =request.args.get('quiz_id')
    quiz_id = "animals"
    session['current_quiz'] = quiz_id
    session['score'] = 0
    session['question_count'] = 0
    return redirect(url_for('quiz'))

@app.route('/quiz')
def quiz():
    session['question_count'] += 1
    quiz_id = session.get('current_quiz')


    if quiz_id == "animals":
        questions = questions_animals
    else:
        return render_template("index.html")

    #picking a question that hasn't been asked yet
    count = 0
    question_picked = False
    while question_picked == False and count < 100:
        count += 1
        rand_question = random.choice(questions)
        if rand_question not in questions_asked:
            questions_asked.append(rand_question)
            question_picked = True

    #add answer images to image_choices
    image_choices = [rand_question["answer"]]

    #add 2 more random images to the list?
    count = 0
    while len(image_choices) < 3 and count < 100:
        count += 1
        if quiz_id == "animals":
            random_image=random.choice(images_all_animals)

        if random_image not in image_choices:
            image_choices.append(random_image)

    #shuffle the images displayed
    random.shuffle(image_choices)

    #updating the current answer for the current user
    session['current_answer'] = rand_question['answer']
    return render_template('quiz.html', question=rand_question, options=image_choices, quiz_name =quiz_id.capitalize())

@app.route('/answer', methods=['POST'])
def answer():
    player_guess = request.form['option']
    correct_answer = session['current_answer']
    if player_guess == correct_answer:
        session['score'] += 1
    else:
        session['score'] -= 1

    #number of questions asked to the players
    if session['question_count'] < 3:
        return redirect(url_for('quiz'))
    else:
        return redirect(url_for('result'))

@app.route('/result')
def result():
    return render_template('result.html', score=session.get('score', 0))

