#import lxml
#from this import d
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


    length = len(tab)
    for i in range(length):            
        table.append(tab[i].text.strip())


    true_table = convert_table(table)
    returned = []
    for i in range(len(true_table) - 1):
        returned.append(true_table[i+1])
    #print(returned)
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



def test_creating_tables():
    link = f"https://onefootball.com/en/competition/premier-league-9/table"
    source = requests.get(link).text
    page = BeautifulSoup(source, "lxml")
    tab = page.find_all("a", class_="standings__row-grid")

    position_table = []
    team_table = []
    played_table = []
    win_table = []
    draw_table = []
    loss_table = []
    gd_table = []
    points_table = []
    

    length = len(tab)
    for i in range(length):  
        to_add = (tab[i].text.strip()).split()
        if not to_add[2].isdigit():
            to_add[1] = to_add[1] + " " + to_add[2]
            del(to_add[2])
        

        #print(to_add)


        position_table.append(to_add[0])
        team_table.append(to_add[1])
        played_table.append(to_add[2])
        win_table.append(to_add[3])
        draw_table.append(to_add[4])
        loss_table.append(to_add[5])
        gd_table.append(to_add[6])
        points_table.append(to_add[7])

    """
    print(position_table)
    print(team_table)
    print(played_table)
    print(win_table)
    print(draw_table)
    print(loss_table)
    print(gd_table)
    print(points_table)
    """

    meta_list = []
    meta_list.append(position_table)
    meta_list.append(team_table)
    meta_list.append(played_table)
    meta_list.append(win_table)
    meta_list.append(draw_table)
    meta_list.append(loss_table)
    meta_list.append(gd_table)
    meta_list.append(points_table)
    print(meta_list)
    return meta_list


if __name__ == "__main__":
    true_table = get_table()
    #pprint(true_table)
    
    hard_coded_predictions = ['Manchester City', 'Liverpool', 'Chelsea', 'Arsenal', 'Tottenham', "Manchester United",
    "West Ham", "Newcastle United", "Wolves", "Crystal Palace", "Leicester", "Aston Villa", "Brighton", "Fulham",
    "Everton", "Brentford", "Leeds", "Bournemouth", "Nottingham Forest", "Southampton"]

    dummy_test = true_table

   # true_difference = get_current_prediction_value(true_table, hard_coded_predictions)

   # print("Your prediction value is: ")
    #print(true_difference)

    test_creating_tables()

