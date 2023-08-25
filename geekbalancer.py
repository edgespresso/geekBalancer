import random
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
    return sum([player_data['KDR'], player_data['aKDR'], player_data['alltime_kdr'], player_data['year_kdr'], player_data['last90_kdr']]) / 5.0

def balance_teams(data, threshold, max_attempts=10):
    # Calculate composite score for each player
    scores = []
    for player in data:
        composite_score = sum([player['KDR'], player['aKDR'], player['alltime_kdr'], player['year_kdr'], player['last90_kdr']]) / 5.0
        scores.append((player['player'], composite_score))

    # Sort players by composite score
    scores.sort(key=lambda x: x[1], reverse=True)

    for i in range(max_attempts):
        # Assign players to teams
        team_a = []
        team_b = []
        for j, (player, score) in enumerate(scores):
            if j % 2 == 0:
                team_a.append((player, score))
            else:
                team_b.append((player, score))

        # Check if teams are balanced
        team_a_score = sum([score for _, score in team_a])
        team_b_score = sum([score for _, score in team_b])
        if abs(team_a_score - team_b_score) <= threshold:
            print(f"Teams balanced after {i+1} attempts:")
            print(f"Team A aggregate score: {team_a_score:.4f}")
            print(f"Team B aggregate score: {team_b_score:.4f}")
            print(f"Aggregate score differential: {abs(team_a_score - team_b_score):.4f}")
            return team_a, team_b, team_a_score, team_b_score, i+1

        print(f"Attempt {i+1}:")
        print(f"Team A aggregate score: {team_a_score:.4f}")
        print(f"Team B aggregate score: {team_b_score:.4f}")
        print(f"Aggregate score differential: {abs(team_a_score - team_b_score):.4f}")

        # Swap players between teams to get closer to the threshold
        for j in range(len(team_a)):
            for k in range(len(team_b)):
                if abs(team_a[j][1] - team_b[k][1]) <= threshold:
                    if random.random() < 0.5:
                        team_a[j], team_b[k] = team_b[k], team_a[j]
                    else:
                        team_a[j], team_a[(j+1)%len(team_a)] = team_a[(j+1)%len(team_a)], team_a[j]
                    break

    print(f"Cannot balance teams with the given threshold ({threshold:.4f}) and maximum number of attempts ({max_attempts}).")
    return None, None, None, None, max_attempts

def main():
    print("\nGEEKFEST GEEK BALANCER\n")
    # Read JSON data from file
    data = read_json_file('geekstats.json')

    if data is None:
        return

    # Set threshold
    threshold = 0.7

    # Balance teams
    team_a, team_b, team_a_score, team_b_score, attempts = balance_teams(data, threshold)

    # Check if teams are balanced
    if team_a is None:
        print("Cannot balance teams with the given threshold and maximum number of attempts.")
        return

    # Print team data
    print("Team A:")
    for player, score in team_a:
        print(f"{player}: {score:.4f}")
    print(f"Total players: {len(team_a)}")
    print(f"Aggregate score: {team_a_score:.4f}")

    print("\nTeam B:")
    for player, score in team_b:
        print(f"{player}: {score:.4f}")
    print(f"Total players: {len(team_b)}")
    print(f"Aggregate score: {team_b_score:.4f}")

    print() # prints a blank line
    print() # prints a blank line
    print(f"Team A score    : {team_a_score:.4f}")
    print(f"Team B score    : {team_b_score:.4f}")
    print(f"Team Difference : {team_a_score - team_b_score:.4f}")
    print(f"Threshold       : {threshold:.4f}")
    print(f"Attempts        : {attempts}")

if __name__ == '__main__':
    main()

if __name__ == '__main__':
    main()