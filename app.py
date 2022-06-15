from flask import *
import random

app = Flask(__name__)
app.secret_key = 'numbers are great'


@app.route('/')
def index():
    return render_template('index.html')


secret_number = random.randint(0, 100)
turn = 0
success = False


@app.route('/', methods=['POST'])
def game():
    global secret_number, turn, success
    context = {}
    hint = ''
    guessed_number = None

    if request.method == 'POST' and request.form["guess"]:
        guessed_number = int(request.form["guess"])

        turn += 1
        if guessed_number == secret_number:
            success = True
        else:
            if guessed_number < secret_number:
                hint = 'Think higher'
            else:
                hint = 'Think lower'

    else:
        secret_number = random.randint(0, 100)
        turn = 0
        success = False
        hint = ''
        guessed_number = None

    context['success'] = success
    context['turn'] = turn
    context['hint'] = hint
    context['guessed_number'] = guessed_number

    if context['turn'] == 10:
        flash('Game Over')
        flash('Secret Number : ' + str(secret_number))
        flash("Please Press 'Start over' to play again")
        secret_number = random.randint(0, 100)
        turn = 0
        success = False
        hint = ''
        guessed_number = None
        return redirect("http://127.0.0.1:5000/", code=302)

    elif context['success']:
        flash('Congratulations ')
        flash('Your Score : ' + str((10 - context['turn'] + 1)*10))
        flash("Please Press 'Start over' to play again")
        secret_number = random.randint(0, 100)
        turn = 0
        success = False
        hint = ''
        guessed_number = None
        return render_template('index.html')

    else:
        flash('Guessed Number : ' + str(context['guessed_number']))
        flash('Success : '+str(context['success']))
        flash('Hint : '+str(context['hint']))
        flash('Remaining turns : ' + str(10-context['turn']))

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
