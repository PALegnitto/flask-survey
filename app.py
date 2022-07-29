from http.client import responses
from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import Question, satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "kjascnabghac_LookAtThisKadeem_Elie_Sarah_Brian0918"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

@app.get('/')
def start_survey():
    """ Creates the session that will hold responses and starts survey"""
    session["responses"] = [];

    return render_template("survey_start.html", survey = survey)
#render should not with a slash

@app.post("/begin")
def go_to_questions():
    """ Directs user to the first question"""

    return redirect("/question/0")



@app.get("/question/<int:id>")
def surface_question(id):
    """Extracts the survey ID and displays the id at that index """
    
    session_list_length = len(session["responses"])

    if id != session_list_length:
        flash("Please answer these questions in order")
        return redirect(f"/question/{session_list_length}")
    
    if session_list_length == len(survey.questions):
        return redirect("/completion")


    question = survey.questions[id]

    return render_template("question.html", question = question)


@app.post('/answer')
def handle_answers():
    """ Stores the answer sends user to the next question and ends survey"""

    session_list = session["responses"]
    session_list.append(request.form['answer'])
    session["responses"] = session_list

    if len(session_list) == len(survey.questions):
        return redirect("/completion")
    else:
        return redirect(f"/question/{len(session_list)}")


@app.get('/completion')
def show_thank_you_message():

    return render_template("completion.html")