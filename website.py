from flask import Flask, jsonify, render_template
import lxml
import requests
from bs4 import BeautifulSoup
import re
from threading import Timer

from data_collection import get_table
from data_collection import test_creating_tables

hard_coded_predictions = ['Manchester City', 'Liverpool', 'Chelsea', 'Arsenal', 'Tottenham', "Manchester United",
    "West Ham", "Newcastle United", "Wolves", "Crystal Palace", "Leicester", "Aston Villa", "Brighton", "Fulham",
    "Everton", "Brentford", "Leeds", "Southampton", "Nottingham Forest", "Bournemouth"]


app = Flask(__name__)

@app.route('/')
def index():
    #print(get_table())
    meta_predictions = []
    meta_list = test_creating_tables()
    standings_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
    meta_predictions.append(standings_list)
    meta_predictions.append(hard_coded_predictions)
    return render_template("index.html", meta_list=meta_list, predictions = meta_predictions)

@app.route('/dashboard')
def dashboard():
    return render_template("dashboard.html")


@app.route('/fixtures')
def fixtures_list():
    link = f"https://onefootball.com/en/competition/premier-league-9/fixtures"
    source = requests.get(link).text
    page = BeautifulSoup(source, "lxml")
    fix = page.find_all("li", class_="simple-match-cards-list__match-card")
    
    fixtures = []
    for i in range(len(fix)):
        fixtures.append(fix[i].text.strip())
    
    return jsonify(fixtures)



@app.route('/fixtures/<team>', methods=['GET'])
def get_fixtures(team):
    link = f"https://onefootball.com/en/competition/premier-league-9/fixtures"
    source = requests.get(link).text
    page = BeautifulSoup(source, "lxml")
    fix = page.find_all("li", class_="simple-match-cards-list__match-card")
    
    fixtures = []
    for i in range(len(fix)):
        fixtures.append(fix[i].text.strip())
    
    a = []
    for i in range(len(fixtures)):
        if team in fixtures[i]:
            a.append(fixtures[i])

    return jsonify(a)



if __name__ == '__main__':
    app.run(use_reloader = False)

    
    