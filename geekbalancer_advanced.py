import json
import itertools
import random
import requests

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

def print_json_from_api(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        print(data)
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
    except ValueError:
        print(f"Error: Invalid JSON data from API.")

def read_json_file(filename):
    try:
        with open(filename) as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON data in file '{filename}'.")

def calculate_composite_score(player_data):
    return sum([
        player_data['KDR'],
        player_data['aKDR'],
        player_data['alltime_kdr'],
        player_data['year_kdr'],
        player_data['last90_kdr'],
        player_data['kills'] / (player_data['deaths'] + 1),
        player_data['assists'] / (player_data['deaths'] + 1),
        player_data['kills'] / (player_data['assists'] + 1),
        player_data['tier'] == 'West1: Master'
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


def balance_teams(data, threshold, max_attempts=1):
    teams = []
    attempts = 0
    while len(teams) < 5 and attempts < max_attempts:
        attempts += 1
        # Create teams
        team_a, team_b = create_teams_plusminus(data, threshold)

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

    print(f"Total attempts: {attempts}")
    return new_teams

def print_top_teams(teams):
    sorted_teams = sorted(teams, key=lambda x: abs(sum([score for _, score in x[0]]) - sum([score for _, score in x[1]])))
    print("Top 10 team configurations with smallest difference in aggregate scores:")
    for i, (team_a, team_b) in enumerate(sorted_teams[:10]):
        team_a_score = sum([score for _, score in team_a])
        team_b_score = sum([score for _, score in team_b])
        print("=====================================")
        print(f"BALANCE TEAM OPTION #{i+1}:")
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
    print("\nGEEKFEST GEEK BALANCER\n")
    # Read JSON data from file
    data = read_json_file('summer_stats.json')

    if data is None:
        return

    # Set threshold
    threshold = 1.0

    # Balance teams
    teams = balance_teams(data, threshold)

    # Check if teams are balanced
    if len(teams) == 0:
        print("Cannot balance teams with the given threshold and maximum number of attempts.")
        return

    # Print team data
    #for i, (team_a, team_b) in enumerate(teams):
    #    print(f"\nTeam {i+1}:")
    #    print("Team A:")
    #    for player, score in team_a:
    #        print(f"{player}: {score:.4f}")
    #    print(f"Total players: {len(team_a)}")
    #    print(f"Aggregate score: {sum([score for _, score in team_a]):.4f}")
    #
    #    print("\nTeam B:")
    #    for player, score in team_b:
    #        print(f"{player}: {score:.4f}")
    #    print(f"Total players: {len(team_b)}")
    #    print(f"Aggregate score: {sum([score for _, score in team_b]):.4f}")

    # Print top teams
    print_top_teams(teams)

    get_json_from_api("http://stats.geekfestclan.com/api/stats/playerstats/?start_date=2023-01-01&end_date=2023-01-31")
    print_json_from_api("http://stats.geekfestclan.com/api/stats/playerstats/?start_date=2023-01-01&end_date=2023-01-31")

if __name__ == '__main__':
    main()
