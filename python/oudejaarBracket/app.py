from flask import Flask, render_template, request, jsonify, current_app
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__, template_folder='front')

DB_USER = "dbuser"
DB_PASSWORD = "PoppyJungle"
DB_NAME = "NYE"
DB_HOST = "91.180.11.226"

app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Team(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(255), nullable=False)

class Match(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    round = db.Column(db.Integer, nullable=False)
    team1_id = db.Column(db.BigInteger, db.ForeignKey('team.id'), nullable=True)
    team2_id = db.Column(db.BigInteger, db.ForeignKey('team.id'), nullable=True)
    winner_id = db.Column(db.BigInteger, db.ForeignKey('team.id'), nullable=True)

class Challenge(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    description = db.Column(db.Text, nullable=False)
    completed = db.Column(db.Boolean, default=False)

with app.app_context():
    db.create_all()

@app.route('/')
def bracket():
    rounds = []
    num_rounds = db.session.query(db.func.max(Match.round)).scalar() or 0
    print(f"Number of rounds: {num_rounds}")
    
    for round_index in range(num_rounds + 1):
        print(f"Processing round {round_index}")
        matches = Match.query.filter_by(round=round_index).all()
        print(f"Matches in round {round_index}: {matches}")
        
        round_matches = []
        for match in matches:
            team1 = Team.query.get(match.team1_id)
            team2 = Team.query.get(match.team2_id)
            round_matches.append((team1.name if team1 else "TBD", team2.name if team2 else "TBD"))
            
        print(f"Round {round_index} matches: {round_matches}")
        rounds.append(round_matches)
    
    print(f"Final rounds data: {rounds}")
    return render_template('bracket.html', rounds=rounds, challenge_text="Initial Challenge Text", enumerate=enumerate)

@app.route('/control')
def control():
    teams = Team.query.all()
    return render_template('control.html', teams=[team.name for team in teams])

@app.route('/select_team', methods=['POST'])
def select_team():
    data = request.json
    selected_team = data['team']
    return jsonify(success=True)

@app.route('/report_win', methods=['POST'])
def report_win():
    data = request.json
    team_name = data['team']
    team = Team.query.filter_by(name=team_name).first()
    
    if not team:
        return jsonify(success=False, error="Team not found"), 400
    
    match = Match.query.filter((Match.team1_id == team.id) | (Match.team2_id == team.id)).first()
    if not match:
        return jsonify(success=False, error="Match not found"), 400
    
    match.winner_id = team.id
    db.session.commit()
    
    # Propagate the winner to the next round
    next_round = match.round + 1
    winners = Match.query.filter(Match.round == match.round, Match.winner_id.isnot(None)).all()
    winner_ids = [winner.winner_id for winner in winners]
    
    # Create new matches for the next round if they don't exist
    if not Match.query.filter_by(round=next_round).count():
        for i in range(0, len(winner_ids), 2):
            team1_id = winner_ids[i]
            team2_id = winner_ids[i + 1] if i + 1 < len(winner_ids) else None
            new_match = Match(round=next_round, team1_id=team1_id, team2_id=team2_id)
            db.session.add(new_match)
    
    db.session.commit()
    
    return jsonify(success=True)

def get_eligible_teams(round_number):
    winners = Match.query.filter(Match.round == round_number, Match.winner_id.isnot(None)).all()
    winner_ids = [winner.winner_id for winner in winners]
    
    # Placeholder for adding teams based on challenges completed
    # completed_challenges = Challenge.query.filter_by(completed=True).all()
    # for challenge in completed_challenges:
    #     team_id = challenge.team_id
    #     if team_id not in winner_ids:
    #         winner_ids.append(team_id)
    
    return winner_ids

if __name__ == '__main__':
    app.run(debug=True)