from flask import Flask, render_template
from Model import model
import csv
import random

app = Flask(__name__)

@app.route("/")
def hello():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/predictor")
def predictor():

    # Get predictions from model
    model()

    # Empty rankings dictionary to pass to html file
    the_rankings = []

    with open('predictions.csv') as predictions:
        rankings = csv.reader(predictions)
        
        for row in rankings:
            the_rankings.append(row)
    
    # Get length of "the_rankings" to pass to html file for loop
    length = len(the_rankings)

    # Possible words to choose from to make website a little more interactive
    intro = ["Currently", "At this point", "At present", "Right now", "For now", "As of now", "Well"]
    intro_next = ["it seems like", "it seems as though", "it looks like", "chances are that"]

    intro_for_predictor = random.choice(intro)
    intro_next_for_predictor = random.choice(intro_next)

    team1 = the_rankings[1][1]
    team2 = the_rankings[2][1]
    team3 = the_rankings[3][1]
    team4 = the_rankings[4][1]
    team5 = the_rankings[5][1]
    team6 = the_rankings[6][1]

    team3rdlast = the_rankings[-3][1]
    team2ndlast = the_rankings[-2][1]
    teamlast = the_rankings[-1][1]

    return render_template("predictor.html", the_rankings=the_rankings, length=length, intro_for_predictor=intro_for_predictor, intro_next_for_predictor=intro_next_for_predictor, team1=team1, team2=team2, team3=team3, team4=team4, team5=team5, team6=team6, team3rdlast=team3rdlast, team2ndlast=team2ndlast, teamlast=teamlast)

if __name__ == "__main__":
    app.run(debug = True)