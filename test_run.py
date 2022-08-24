#import lxml
import requests
from bs4 import BeautifulSoup
import re
import time
from pprint import pprint


def get_table() -> list:
    link = f"https://onefootball.com/en/competition/premier-league-9/table"
    source = requests.get(link).text
    page = BeautifulSoup(source, "lxml")
    tab = page.find_all("a", class_="standings__row-grid")

    table = []
    table.append("  ________________ PL W D L GD PTS")



    for i in range(len(tab)):
        table.append(tab[i].text.strip())

    true_table = convert_table(table)
    returned = []
    for i in range(len(true_table) - 1):
        returned.append(true_table[i+1])
    print(returned)
    return returned


def convert_table(predictions) -> list:
    answer = []
    for i in range(len(predictions)):
        result = ''.join([j for j in predictions[i] if not (j.isdigit() or j == "-")])
        result.replace(" ", "")
        result.replace("-", "")
        result = result.strip()
        answer.append(result)
    return answer






#### WE NOW NEED TO LOGIC OUT THE TABLE DIFFERENCE

def get_current_prediction_value(table, predictions) -> int:
    total = 0
    for i in range(len(table)):
        prediction_index = predictions.index(table[i])
        total += abs(prediction_index - i)
    
    return total

if __name__ == "__main__":
    true_table = get_table()
    #pprint(true_table)
    
    hard_coded_predictions = ['Manchester City', 'Liverpool', 'Chelsea', 'Arsenal', 'Tottenham', "Manchester United",
    "West Ham", "Newcastle United", "Wolves", "Crystal Palace", "Leicester", "Aston Villa", "Brighton", "Fulham",
    "Everton", "Brentford", "Leeds", "Bournemouth", "Nottingham Forest", "Southampton"]

    dummy_test = true_table

    true_difference = get_current_prediction_value(true_table, hard_coded_predictions)

    print("Your prediction value is: ")
    print(true_difference)

