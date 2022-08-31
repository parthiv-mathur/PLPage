from flask import Flask, jsonify, render_template
import lxml
import requests
from bs4 import BeautifulSoup
import re
from threading import Timer

from data_collection import get_table
from data_collection import test_creating_tables


app = Flask(__name__)

@app.route('/')
def index():
    #print(get_table())
    meta_list = test_creating_tables()
    return render_template("index.html", meta_list=meta_list)

@app.route('/')
def prem_table():
    return "hello"

@app.route('/players/<player_name>', methods=['GET'])
def get_player(player_name):

    try:
        link = f"https://www.google.com/search?q={player_name}+premier+league.com+stats"
        source = requests.get(link).text
        page = BeautifulSoup(source, "lxml")
        page = page.find("div",class_="kCrYT")
        link = page.find("a", href=re.compile(r"[/]([a-z]|[A-Z])\w+")).attrs["href"]
    
    except:
        link = f"https://www.google.com/search?q={player_name}+pl+stats"
        source = requests.get(link).text
        page = BeautifulSoup(source, "lxml")
        page = page.find("div",class_="kCrYT")
        link = page.find("a", href=re.compile(r"[/]([a-z]|[A-Z])\w+")).attrs["href"]

    spl_word = '&sa'
    res = link[7:].partition(spl_word)[0]
    if "stats" in res:
        res = res.replace('stats','overview')
        
    sta = res.replace('overview','stats')
    source = requests.get(sta).text
    page = BeautifulSoup(source, "lxml")
    side = page.find("div",class_="label").text
    
    ###
    name = page.find("div",class_="name t-colour").text
    position = page.find("div",class_="info").text.strip()
    club = "No longer part of EPL"
    
    if "Club" in side:
        a = page.find_all("div",class_="info")
        club = page.find("div",class_="info").text.strip()
        position = a[1].text.strip()

    #####
    stats = page.find_all("div",class_="topStat")
    basic = []
    for i in range(len(stats)):
        basic.append(stats[i].text.strip())
    basic_stats = []
    
    for k in range(len(basic)):
        basic_stats.append(basic[k].split("\n"))
        
    ####
    source2 = requests.get(res).text
    page2 = BeautifulSoup(source2, "lxml")
    personal_details = page2.find("div",class_="playerInfo")
    pd = personal_details.find_all("div",class_="info")
    ####
    nationality = personal_details.find("span",class_="playerCountry").text
    dob = pd[1].text.strip()

    fin = page.find_all("div",class_="normalStat")
    final=[]
    for j in range(len(fin)):
        final.append(fin[j].text.strip())
    
    all_stats = []
    for k in range(len(final)):
        all_stats.append(final[k].split("\n"))

    try:
        height = pd[2].text.strip()
        return jsonify({'name': name, 'position': position, 'club': club, 'key_stats': basic_stats, 'Nationality': nationality, 'Date of Birth': dob,'height':height,'complete stats': all_stats})
    except:
        return jsonify({'name': name, 'position': position, 'club': club, 'key_stats': basic_stats, 'Nationality': nationality, 'Date of Birth': dob, 'complete stats': all_stats})
        
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


@app.route('/table')
def table():
    link = f"https://onefootball.com/en/competition/premier-league-9/table"
    source = requests.get(link).text
    page = BeautifulSoup(source, "lxml")
    tab = page.find_all("a", class_="standings__row-grid")
    table = []
    table.append("  ________________ PL W D L GD PTS")
    
    for i in range(len(tab)):
        table.append(tab[i].text.strip())




#def open_browser():
    #webbrowser.open_new_tab("http://127.0.0.1:4999/")

if __name__ == '__main__':
    #port = 5000 + random.randint(0, 999)
    #url = "http://127.0.0.1:{0}".format(port)

    #threading.Timer(1.25, lambda: webbrowser.open(url, new=1, autoraise=True)).start()

    #app.run(port=port, debug=False)
    #subprocess.Popen(['python', '-m', 'SimpleHTTPServer', '5000'])

    app.run(use_reloader = False)
    #open_browser()
    #app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)

    #url = 'http://127.0.0.1:5000/'
    #webbrowser.get('chrome').open_new_tab(url)
    #app.run(debug=False)
    
    #new_table = get_table()
    #print(new_table)

#if __name__ =="__main__":
    #from waitress import serve
    #serve(app, host="0.0.0.0", port=8080)
 #   app.run(debug=True)

    
    