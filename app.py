from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# DB Models
class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    wins = db.Column(db.Integer, default=0)
    draws = db.Column(db.Integer, default=0)
    losses = db.Column(db.Integer, default=0)

class Match(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    white_player_id = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=False)
    black_player_id = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=False)
    result = db.Column(db.String(10), nullable=False)
    game_link = db.Column(db.String(200))
    date = db.Column(db.String(50))
    result_info = db.Column(db.String(200))

    white_player = db.relationship('Player', foreign_keys=[white_player_id])
    black_player = db.relationship('Player', foreign_keys=[black_player_id])

def update_player_record(match):
    white_player = Player.query.filter_by(id=match.white_player_id).first()
    black_player = Player.query.filter_by(id=match.black_player_id).first()

    if match.result == '1-0':  # White wins
        white_player.wins += 1
        black_player.losses += 1
    elif match.result == '0-1':  # Black wins
        white_player.losses += 1
        black_player.wins += 1
    elif match.result == '1/2-1/2':  # Draw
        white_player.draws += 1
        black_player.draws += 1

    db.session.commit()



# 초기화 엔드포인트 (첫 실행 시 사용)
@app.route('/init_db')
def init_db():
    db.create_all()
    return 'DB initialized!'

# 페이지 템플릿 엔드포인트
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/leaderboard')
def leaderboard():
    return render_template('leaderboard.html')

@app.route('/players')
def players():
    return render_template('players.html')

@app.route('/match_results')
def match_results():
    return render_template('match_results.html')

@app.route('/player_detail/<int:player_id>')
def player_detail(player_id):
    return render_template('player_detail.html')

@app.route('/add_match')
def add_match():
    return render_template('add_match.html')

@app.route('/match_detail/<int:match_id>')
def match_detail(match_id):
    return render_template('match_detail.html')


@app.route('/select_players')
def select_players():
    return render_template('select_players.html')

@app.route('/player_vs_player', methods=['POST'])
def player_vs_player():
    player1_id = request.form['player1']
    player2_id = request.form['player2']
    return redirect(url_for('player_vs_player_stats', player1_id=player1_id, player2_id=player2_id))

@app.route('/player_vs_player_stats')
def player_vs_player_stats():
    player1_id = request.args.get('player1_id')
    player2_id = request.args.get('player2_id')
    return render_template('player_vs_player.html', player1_id=player1_id, player2_id=player2_id)


@app.route('/api/player_vs_player')
def player_vs_player_data():
    player1_id = request.args.get('player1_id')
    player2_id = request.args.get('player2_id')

    # 데이터베이스에서 두 선수의 모든 경기를 조회
    matches = Match.query.filter(
        ((Match.white_player_id == player1_id) & (Match.black_player_id == player2_id)) |
        ((Match.white_player_id == player2_id) & (Match.black_player_id == player1_id))
    ).all()

    # 두 선수의 통계 초기화
    player1_wins = player1_draws = player1_losses = 0
    player2_wins = player2_draws = player2_losses = 0
    player1_as_white_wins = player1_as_white_draws = player1_as_white_losses = 0
    player2_as_white_wins = player2_as_white_draws = player2_as_white_losses = 0

    # 통계 계산
    print(matches[0].result,matches[0].white_player_id,player1_id)
    for match in matches:
        if str(match.white_player_id) == str(player1_id):
            print('11')
            if match.result == '1-0':
                player1_wins += 1
                player2_losses += 1
                player1_as_white_wins += 1
            elif match.result == '0-1':
                player1_losses += 1
                player2_wins += 1
                player1_as_white_losses += 1
            elif match.result == '1/2-1/2':
                player1_draws += 1
                player2_draws += 1
                player1_as_white_draws += 1
        elif str(match.white_player_id) == str(player2_id):
            if match.result == '1-0':
                player2_wins += 1
                player1_losses += 1
                player2_as_white_wins += 1
            elif match.result == '0-1':
                player2_losses += 1
                player1_wins += 1
                player2_as_white_losses += 1
            elif match.result == '1/2-1/2':
                player2_draws += 1
                player1_draws += 1
                player2_as_white_draws += 1
        else:print('?')

    total_games = len(matches)

    def calculate_win_rate(wins, total):
        return (wins / total * 100) if total > 0 else 0

    response = {
        'player1': {
            'name': Player.query.get(player1_id).name,
            'total_games': total_games,
            'wins': player1_wins,
            'win_rate': calculate_win_rate(player1_wins, total_games),
            'draws': player1_draws,
            'draw_rate': calculate_win_rate(player1_draws, total_games),
            'losses': player1_losses,
            'losses_rate': calculate_win_rate(player1_losses,total_games)
        },
        'player2': {
            'name': Player.query.get(player2_id).name,
            'total_games': total_games,
            'wins': player2_wins,
            'win_rate': calculate_win_rate(player2_wins, total_games),
            'draws': player2_draws,
            'draw_rate': calculate_win_rate(player2_draws, total_games),
            'losses': player2_losses,
            'losses_rate': calculate_win_rate(player2_losses,total_games)
        },
        'player1_as_white': {
            'wins': player1_as_white_wins,
            'win_rate': calculate_win_rate(player1_as_white_wins, total_games),
            'draws': player1_as_white_draws,
            'draw_rate': calculate_win_rate(player1_as_white_draws, total_games),
            'losses': player1_as_white_losses,
            'losses_rate': calculate_win_rate(player1_as_white_losses,total_games)
        },
        'player2_as_white': {
            'wins': player2_as_white_wins,
            'win_rate': calculate_win_rate(player2_as_white_wins, total_games),
            'draws': player2_as_white_draws,
            'draw_rate': calculate_win_rate(player2_as_white_draws, total_games),
            'losses': player2_as_white_losses,
            'losses_rate': calculate_win_rate(player2_as_white_losses,total_games)
        }
    }

    return jsonify(response)
# API 엔드포인트
@app.route('/api/players', methods=['GET'])
def get_players():
    players = Player.query.all()
    players_data = [{'id': p.id, 'name': p.name, 'wins': p.wins, 'draws': p.draws, 'losses': p.losses} for p in players]
    return jsonify(players_data)

@app.route('/api/leaderboard', methods=['GET'])
def get_leaderboard():
    players = Player.query.all()
    players.sort(key=lambda p: (p.wins, p.draws, p.losses), reverse=True)
    return jsonify([{'name': p.name, 'wins': p.wins, 'draws': p.draws, 'losses': p.losses} for p in players])

@app.route('/api/player/<int:player_id>', methods=['GET'])
def get_player(player_id):
    player = Player.query.get_or_404(player_id)
    matches = Match.query.filter((Match.white_player_id == player.id) | (Match.black_player_id == player.id)).all()
    match_data = []
    for match in matches:
        match_data.append({
            'white_player': match.white_player.name,
            'black_player': match.black_player.name,
            'result': match.result,
            'game_link': match.game_link,
            'date': match.date,
            'result_info': match.result_info
        })
    player_data = {
        'id': player.id,
        'name': player.name,
        'wins': player.wins,
        'draws': player.draws,
        'losses': player.losses,
        'matches': match_data
    }
    return jsonify(player_data)

@app.route('/api/match/<int:match_id>', methods=['GET'])
def get_match(match_id):
    match = Match.query.get_or_404(match_id)
    match_data = {
        'white_player': match.white_player.name,
        'black_player': match.black_player.name,
        'result': match.result,
        'game_link': match.game_link,
        'date': match.date,
        'result_info': match.result_info
    }
    return jsonify(match_data)

@app.route('/api/matches', methods=['GET'])
def get_matches():
    matches = Match.query.order_by(Match.date.desc()).all()
    matches_data = [{
        'id': m.id,
        'white_player': m.white_player.name,
        'black_player': m.black_player.name,
        'result': m.result,
        'date': m.date
    } for m in matches]
    return jsonify(matches_data)

@app.route('/api/add_player', methods=['POST'])
def add_player():
    data = request.json
    new_player = Player(name=data['name'])
    db.session.add(new_player)
    db.session.commit()
    return jsonify({'message': 'Player added successfully!'})

@app.route('/api/add_match', methods=['POST'])
def add_match_api():
    data = request.json
    new_match = Match(
        white_player_id=data['white_player_id'],
        black_player_id=data['black_player_id'],
        result=data['result'],
        game_link=data.get('game_link', ''),
        date=data['date'],
        result_info=data.get('result_info', '')
    )
    db.session.add(new_match)
    db.session.commit()
    
    update_player_record(new_match)
    
    return jsonify({'message': 'Match added successfully!'})

if __name__ == '__main__':
    app.run(debug=True)

