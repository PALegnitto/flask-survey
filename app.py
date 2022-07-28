from http.client import responses
from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import Question, satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

responses = []

@app.get('/')
def start_survey():

    return render_template("survey_start.html", survey = survey)
#render should not with a slash

@app.post("/begin")
def go_to_questions():

    return redirect("/question/0")



@app.get("/question/<int:id>")
def surface_question(id):

    question = survey.questions[id]


    return render_template("question.html", question = question)


@app.post('/answer')
def handle_answers():
    responses.append(request.form['answer'])

    if len(responses) == len(survey.questions):
        return redirect("/completion")
    else:
        return redirect(f"/question/{len(responses)}")


@app.get('/completion')
def show_thank_you_message():

    return render_template("completion.html")