from flask import Flask
import requests
import jsonify

app = Flask(__name__)

@app.route('/sort_players', methods=['POST'])
def sort_players():
    player_data = request.get_json()
    usernames = player_data.get('usernames', [])
    alphabetized = sorted(usernames)
    return jsonify({'alphabetized_usernames': alphabetized})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
