import json
import requests
from flask import Flask, request, jsonify

def create_api_string(base_url, start_date, end_date):
    api_string = f"{base_url}?start_date={start_date}&end_date={end_date}"
    return api_string

def get_json_from_api(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
    except ValueError:
        print(f"Error: Invalid JSON data from API.")

def write_json_file(filename, data):
    try:
        # Parse JSON object from string
        parsed_data = json.loads(data)

        # Write parsed JSON object to file
        with open(filename, 'w') as f:
            json.dump(parsed_data, f, indent=4)
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON data in file '{filename}'.")
    except IOError:
        print(f"Error: Failed to write JSON data to file '{filename}'.")
    
def read_json_file(filename):
    try:
        with open(filename) as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON data in file '{filename}'.")

def filter_player_stats(data, players):
    filtered_data = []
    for player in players:
        for item in data:
            if item['player'] == player:
                filtered_data.append(item)
                break
    return filtered_data

def calculate_composite_score(player_data):
    # Get player data into variables
    kdr = player_data.get('kdr', 0)
    akdr = player_data.get('akdr', 0)
    alltime_kdr = player_data.get('alltime_kdr', 0)
    year_kdr = player_data.get('year_kdr', 0)
    last90_kdr = player_data.get('last90_kdr', 0)
    kills = player_data.get('kills', 0)
    deaths = player_data.get('deaths', 0)
    assists = player_data.get('assists', 0)
    tier = player_data.get('tier', '')

    # Check types and replace None with 0
    if not isinstance(kdr, (int, float)):
        kdr = 0
    if not isinstance(akdr, (int, float)):
        akdr = 0
    if not isinstance(alltime_kdr, (int, float)):
        alltime_kdr = 0
    if not isinstance(year_kdr, (int, float)):
        year_kdr = 0
    if not isinstance(last90_kdr, (int, float)):
        last90_kdr = 0
    if not isinstance(kills, (int, float)):
        kills = 0
    if not isinstance(deaths, (int, float)):
        deaths = 0
    if not isinstance(assists, (int, float)):
        assists = 0

    # Calculate composite score
    return sum([
        kdr,
        akdr,
        alltime_kdr,
        year_kdr,
        last90_kdr,
        kills / (deaths + 1),
        assists / (deaths + 1),
        kills / (assists + 1),
        tier == 'West1: Master'
    ]) / 9.0

def create_teams_plusminus(data, threshold):
    # Calculate composite score for each player
    scores = []
    for player in data:
        composite_score = calculate_composite_score(player)
        scores.append((player['player'], composite_score))
    
    # Sort players by composite score
    scores.sort(key=lambda x: x[1], reverse=True)

    # Assign players to teams
    team_a = []
    team_b = []
    for i, (player, score) in enumerate(scores):
        if i % 2 == 0:
            team_a.append((player, score))
        else:
            team_b.append((player, score))

    # Check if teams are balanced
    team_a_score = sum([score for _, score in team_a])
    team_b_score = sum([score for _, score in team_b])
    while abs(team_a_score - team_b_score) > threshold:
        # Swap players between teams
        if team_a_score > team_b_score:
            player, score = team_a.pop()
            team_b.append((player, score))
        else:
            player, score = team_b.pop()
            team_a.append((player, score))

        # Recalculate team scores
        team_a_score = sum([score for _, score in team_a])
        team_b_score = sum([score for _, score in team_b])

    return team_a, team_b

def create_teams_plusminus_new(data, threshold):
    # Calculate composite score for each player
    scores = []
    for player in data:
        composite_score = calculate_composite_score(player)
        scores.append((player['player'], composite_score))
    
    # Sort players by composite score
    scores.sort(key=lambda x: x[1], reverse=True)

    # Assign players to teams
    team_a = []
    team_b = []
    for i, (player, score) in enumerate(scores):
        if i % 2 == 0:
            team_a.append((player, score))
        else:
            team_b.append((player, score))

    # Check if teams are balanced
    while abs(len(team_a) - len(team_b)) > 1:
        if len(team_a) > len(team_b):
            player, score = team_a.pop()
            team_b.append((player, score))
        else:
            player, score = team_b.pop()
            team_a.append((player, score))

    return team_a, team_b

def balance_teams(data, threshold, max_attempts=1):
    teams = []
    attempts = 0
    while len(teams) < 5 and attempts < max_attempts:
        attempts += 1
        # Create teams
        team_a, team_b = create_teams_plusminus_new(data, threshold)

        # Check if teams are balanced
        team_a_score = sum([score for _, score in team_a])
        team_b_score = sum([score for _, score in team_b])
        if abs(team_a_score - team_b_score) <= threshold:
            teams.append((team_a, team_b))

    if len(teams) == 0:
        print(f"Cannot balance teams with the given threshold ({threshold:.4f}) and maximum number of attempts ({max_attempts}).")
        return None, None

    # Swap players between teams to generate different permutations
    new_teams = []
    for team_a, team_b in teams:
        for i in range(len(team_a)):
            for j in range(len(team_b)):
                # Swap players
                new_team_a = team_a[:i] + [team_b[j]] + team_a[i+1:]
                new_team_b = team_b[:j] + [team_a[i]] + team_b[j+1:]

                # Check if new teams are balanced
                new_team_a_score = sum([score for _, score in new_team_a])
                new_team_b_score = sum([score for _, score in new_team_b])
                if abs(new_team_a_score - new_team_b_score) <= threshold:
                    new_teams.append((new_team_a, new_team_b))

    if len(new_teams) == 0:
        print(f"Cannot generate new team permutations with the given threshold ({threshold:.4f}).")
        return teams[0]

    return new_teams

def print_top_teams(teams, max_teams=10):
    sorted_teams = sorted(teams, key=lambda x: abs(sum([score for _, score in x[0]]) - sum([score for _, score in x[1]])))
    print(f"\nTop {max_teams} Team Configurations - Sorted by Score Differential\n")
    for i, (team_a, team_b) in enumerate(sorted_teams[:max_teams]):
        team_a_score = sum([score for _, score in team_a])
        team_b_score = sum([score for _, score in team_b])
        print("=========================================================")
        print(f"OPTION #{i+1}:")
        print(f"Team A score   : {team_a_score:.4f}")
        print(f"Team B score   : {team_b_score:.4f}")
        print(f"Difference     : {abs(team_a_score - team_b_score):.4f}")
        print(f"\nTeam A players : {len(team_a)}")
        for name, score in sorted(team_a, key=lambda x: x[1], reverse=True):
            print(f" - {name} ({score:.4f})")
        print(f"\nTeam B players : {len(team_b)}")
        for name, score in sorted(team_b, key=lambda x: x[1], reverse=True):
            print(f" - {name} ({score:.4f})")
        print()

def main():
    # Set threshold
    threshold = 3.0

    # Set parameters for the API call
    base_url = "http://stats.geekfestclan.com/api/stats/playerstats/"
    start_date = "2023-02-28"
    end_date = "2023-08-30"
    api_string = create_api_string(base_url, start_date, end_date)
    statsURL = api_string

    #statsURL = "http://stats.geekfestclan.com/api/stats/playerstats/?start_date=2023-01-01&end_date=2023-01-31"
    #statsURL = "http://stats.geekfestclan.com/api/stats/playerstats/?start_date=2023-07-01&end_date=2023-07-07"

    print("\nGEEKFEST GEEK BALANCER\n")
    print(f"Start Date : {start_date}")
    print(f"End Date   : {end_date}")

    # Read JSON data from file
    #data_temp = get_json_from_api(statsURL)

    # Write FIXED JSON data to file
    #write_json_file('stats.json', data_temp)
    
    # Read the fixed JSON file and start balance
    data = read_json_file('stats.json')
    
    if data is None:
        return

    # Balance teams
    teams = balance_teams(data, threshold)

    # Check if teams are balanced
    if len(teams) == 0:
        print("Cannot balance teams with the given threshold and maximum number of attempts.")
        return

    # Print top teams
    print_top_teams(teams, 5)

    # Filter data for specific players
    players = ['Edge', 'Mailboxhead', 'Dream']
    filtered_data = filter_player_stats(data, players)
    print(filtered_data)

    # Balance teams
    teams = balance_teams(filtered_data, threshold)

    # Check if teams are balanced
    if len(teams) == 0:
        print("Cannot balance teams with the given threshold and maximum number of attempts.")
        return
    print_top_teams(teams, 5)

import json

def create_team_json(team, team_name, team_score):
    team_json = {
        'team_name': team_name,
        'team_score': team_score,
        'team_num_players': len(team),
        'players': {}
    }
    for i, (name, score) in enumerate(team, start=1):
        player_json = {
            'player_name': name,
            'player_score': score
        }
        team_json['players'][i] = player_json
    return team_json

def get_top_teams(teams, max_teams=10):
    sorted_teams = sorted(teams, key=lambda x: abs(sum([score for _, score in x[0]]) - sum([score for _, score in x[1]])))
    top_teams = {}
    for i, (team_a, team_b) in enumerate(sorted_teams[:max_teams], start=1):
        team_a_score = sum([score for _, score in team_a])
        team_b_score = sum([score for _, score in team_b])
        team_a_json = create_team_json(team_a, 'Alpha', team_a_score)
        team_b_json = create_team_json(team_b, 'Bravo', team_b_score)
        top_teams[f'option_{i}'] = {'team': [team_a_json, team_b_json]}
    print(json.dumps(top_teams, indent=4))

app = Flask(__name__)

# Set threshold
threshold = 3.0

# Read the fixed JSON file and start balance
data = read_json_file('stats.json')

@app.route('/balance', methods=['POST'])
def balance_teams_api():
    # Get the list of players from the JSON payload
    players = request.json['players']

    # Filter data for specific players
    filtered_data = filter_player_stats(data, players)

    # Balance teams
    teams = balance_teams(filtered_data, threshold)

    # Check if teams are balanced
    if len(teams) == 0:
        return jsonify({'error': 'Cannot balance teams with the given threshold and maximum number of attempts.'}), 400

    # Return the top teams as JSON
    top_teams = get_top_teams(teams, 5)
    return jsonify(top_teams)

if __name__ == '__main__':
    app.run(debug=True)

#if __name__ == '__main__':
#    main()
