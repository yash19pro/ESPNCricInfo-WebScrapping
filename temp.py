from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import requests
from bs4 import BeautifulSoup
import html5lib

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///players.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class Player(db.Model):
    id_no = db.Column(db.Integer, primary_key=True, autoincrement=True)
    squad_name = db.Column(db.String(200), nullable=False)
    player_name = db.Column(db.String(200), nullable=False)
    player_role = db.Column(db.String(200), nullable=False)
    player_nationality = db.Column(db.String(200), nullable=False)

    def __repr__(self) -> str:
        return f"{self.player_name} -> {self.squad_name}"


@app.route('/temp_create')
def temp_create():
    player = Player(squad_name="RCB", player_name="Virat Kohli", player_role="Batsmen", player_nationality="India")
    db.session.add(player)

    player = Player(squad_name="MI", player_name="Rohit Sharma", player_role="Batsmen", player_nationality="India")
    db.session.add(player)

    player = Player(squad_name="DC", player_name="Trent Boult", player_role="Bowler", player_nationality="New Zealand")
    db.session.add(player)

    player = Player(squad_name="RCB", player_name="AB De Villiers", player_role="Batsmen",
                    player_nationality="South Africa")
    db.session.add(player)

    db.session.commit()
    return "Done!"


@app.route('/get_all_players')
def get_app_players():
    players = Player.query.all()
    return render_template("get_all_players.html", players=players)


@app.route('/get_players', methods=["GET", "POST"])
def get_players():
    if request.method == "POST":
        print("In Post!")
        team_name = request.form['squad_name']
        print(team_name)
        players = Player.query.filter_by(squad_name=team_name).all()
        print(players)
        return render_template("get_players.html", players=players)
    else:
        return render_template("get_players.html")


def foobar(url) -> None:
    base_url = "https://www.espncricinfo.com/"
    squads = url + '/squads'
    print(squads)
    r = requests.get(squads)
    html_content = r.content
    soup = BeautifulSoup(html_content, "html.parser")

    # fetching the squads
    squads_tags = soup.find_all('a', class_="black-link")
    squads = set()
    for team in squads_tags:
        squads.add((team.text, base_url+team['href'][1:]))
    print(squads)

    squads = list(squads)

    # fetching the team members
    squad = squads[0]
    link = squad[1]
    r = requests.get(link)
    html_content = r.content
    soup = BeautifulSoup(html_content, "html.parser")
    members_tags = soup.find_all('a', class_="name")
    print(members_tags)
    members = []
    for member in members_tags:
        members.append(member.text[:-1])
    print(members)


@app.route('/', methods=['GET', "POST"])
def home_page():
    if request.method == "POST":
        url = request.form['url']
        foobar("https://www.espncricinfo.com/series/big-bash-league-2021-22-1269637")

    return render_template("home.html")


if __name__ == '__main__':
    app.run(debug=True)
