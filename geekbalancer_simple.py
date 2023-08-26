import json

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

def create_teams(data):
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

    return team_a, team_b

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

def main():
    print("\nGEEKFEST GEEK BALANCER\n")
    # Read JSON data from file
    data = read_json_file('summer_stats.json')

    if data is None:
        return

    # Set threshold
    threshold = 1.0

    # Create teams
    team_a, team_b = create_teams_plusminus(data, threshold)

    # Print team data
    print("Team A:")
    for player, score in team_a:
        print(f"{player}: {score:.4f}")
    print(f"Total players: {len(team_a)}")

    print("\nTeam B:")
    for player, score in team_b:
        print(f"{player}: {score:.4f}")
    print(f"Total players: {len(team_b)}")

    team_a_score = sum([score for _, score in team_a])
    team_b_score = sum([score for _, score in team_b])

    print(f"\nTeam A score    : {team_a_score:.4f}")
    print(f"Team B score    : {team_b_score:.4f}")
    print(f"Team Difference : {team_a_score - team_b_score:.4f}")
    print(f"Threshold       : {threshold:.4f}")

if __name__ == '__main__':
    main()