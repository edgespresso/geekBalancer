import  json
import  requests
from    flask import Flask, request, jsonify, Response
from datetime import datetime, timedelta

def create_api_string(base_url, start_date, end_date):
    """
    Creates an API string using the given base URL, start date, and end date.

    Args:
        base_url (str): The base URL for the API.
        start_date (str): The start date for the API query.
        end_date (str): The end date for the API query.

    Returns:
        str: The API string with the start and end dates included.
    """
    api_string = f"{base_url}?start_date={start_date}&end_date={end_date}"
    return api_string

def get_json_from_api(url):
    """
    Sends a GET request to the specified URL and returns the JSON data.

    Args:
        url (str): The URL to send the GET request to.

    Returns:
        dict: The JSON data returned from the API.

    Raises:
        requests.exceptions.RequestException: If an error occurs while sending the GET request.
        ValueError: If the JSON data returned from the API is invalid.
    """
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
    """
    Writes a JSON object to a file.

    Args:
        filename (str): The name of the file to write to.
        data (str): The JSON object to write to the file.

    Raises:
        json.JSONDecodeError: If the data is not a valid JSON object.
        IOError: If there is an error writing the data to the file.
    """
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
    """
    Reads a JSON file and returns its contents as a Python object.

    Args:
        filename (str): The path to the JSON file.

    Returns:
        dict: A dictionary containing the contents of the JSON file.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        json.JSONDecodeError: If the specified file contains invalid JSON data.
    """
    try:
        with open(filename) as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON data in file '{filename}'.")

def filter_player_stats(data, players):
    """
    Filters the given stats data to only include stats for the specified players.

    Args:
        data (list): A list of dictionaries containing player stats.
        players (list): A list of player handles to filter the data.

    Returns:
        list: A list of dictionaries containing stats for the specified players.
    """
    mydata_parsed = json.loads(data)
    filtered_data = []
    for player in players:
        for entry in mydata_parsed:
            if entry['player'] == player:
                filtered_data.append(entry)
                break

    return filtered_data

def find_captains(players):
    """
    Finds the captains from the given list of players.

    Args:
        players (list): A list of dictionaries containing player data.

    Returns:
        A list of dictionaries containing the captain data.
    """
    players_parsed = json.loads(players)
    captains = []
    for player in players_parsed:
        if player['captain'] == 'TRUE':
            captains.append(player)

    return captains


def calculate_composite_score(player_data):
    """
    Calculates the composite score for a player based on their performance data.

    Args:
        player_data (dict): A dictionary containing the player's performance data, including:
            - kdr (float): Kill-death ratio.
            - akdr (float): Asist-kill-death ratio.
            - alltime_kdr (float): All-time kill-death ratio.
            - year_kdr (float): Yearly kill-death ratio.
            - last90_kdr (float): Kill-death ratio for the last 90 days.
            - kills (int): Total number of kills.
            - deaths (int): Total number of deaths.
            - assists (int): Total number of assists.
            - tier (str): The player's tier.

    Returns:
        float: The composite score for the player.
    """
    # Get player data into variables
    kdr         = player_data.get('kdr', 0)
    akdr        = player_data.get('akdr', 0)
    alltime_kdr = player_data.get('alltime_kdr', 0)
    year_kdr    = player_data.get('year_kdr', 0)
    last90_kdr  = player_data.get('last90_kdr', 0)
    kills       = player_data.get('kills', 0)
    deaths      = player_data.get('deaths', 0)
    assists     = player_data.get('assists', 0)
    tier        = player_data.get('tier', '')

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

def assign_players(data, threshold):
    """
    Assigns players to two teams based on their composite score, ensuring that the teams are balanced.

    Args:
        data (list): A list of player dictionaries, where each dictionary contains the player's name and stats.
        threshold (float): The minimum composite score required for a player to be considered for team assignment.

    Returns:
        tuple: A tuple containing two lists of player tuples, where each player tuple contains the player's name and composite score.
    """
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
        team_a, team_b = assign_players(data, threshold)

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

def create_team_json_list(team, team_name, team_score, player_dict):
    players = []
    for name, score in team:

        # get discord name for the specified player handle from player_dict
        discord = player_dict[name]['discord']

        # get steam_id for the specified player handle from player_dict
        steam_id = player_dict[name]['steam_id']

        player = {
            'player_name': name,
            'player_score': round(score, 4),
            'discord': discord,
            'steam_id': steam_id
        }
        players.append(player)
    team_json = {
        'team_name': team_name,
        'team_score': round(team_score, 10),
        'team_num_players': len(team),
        'players': players
    }
    return team_json

def get_top_teams(teams, player_dict, max_teams=10, output_file='top_teams.json'):
    sorted_teams = sorted(teams, key=lambda x: abs(sum([score for _, score in x[0]]) - sum([score for _, score in x[1]])))
    top_teams = []
    for team_a, team_b in sorted_teams[:max_teams]:
        team_a_score = sum([score for _, score in team_a])
        team_b_score = sum([score for _, score in team_b])
        team_a_json = create_team_json_list(team_a, 'Alpha', team_a_score, player_dict)
        team_b_json = create_team_json_list(team_b, 'Bravo', team_b_score, player_dict)
        top_teams.append({'team_a': team_a_json, 'team_b': team_b_json})
    with open(output_file, 'w') as f:
        json.dump(top_teams, f, indent=4)
    #print(json.dumps(top_teams, indent=4))
    return(top_teams)

def filter_teams_by_captains(data, captain1, captain2):
    """
    Filters the given JSON payload based on the captains' names.

    Args:
        data (list): A list of dictionaries containing team data.
        captain1 (str): The name of the captain for team A.
        captain2 (str): The name of the captain for team B.

    Returns:
        A list of dictionaries containing the team data that match the captains' names.
    """
    mydata_parsed = json.loads(data)
    filtered_data = []
    for item in mydata_parsed:
        team_a_captain = next((player for player in item['team_a']['players'] if player['player_name'] == captain1), None)
        team_b_captain = next((player for player in item['team_b']['players'] if player['player_name'] == captain2), None)
        if team_a_captain and team_b_captain and team_a_captain != team_b_captain:
            filtered_data.append(item)
    return filtered_data

def get_player_data(player_name, player_data):
    # Check if the player name is in the player data dictionary
    if player_name in player_data:
        # Return the steam ID and handle for the player
        return player_data[player_name]['steam_id'], player_data[player_name]['handle']
    else:
        # Return None if the player name is not found
        return None, None


###################################################################################################

app = Flask(__name__)

# Set threshold
threshold = 2.0

@app.route('/balance', methods=['POST'])
def balance_teams_api():
    # Set parameters for the API call
    base_url    = "http://stats.geekfestclan.com/api/stats/playerstats/"
    
    # Get the date 6 months ago from today
    start_date  = (datetime.today() - timedelta(days=30*6)).strftime('%Y-%m-%d')
    end_date    = datetime.today().strftime('%Y-%m-%d')

    # Create the fully qualified API string
    api_string  = create_api_string(base_url, start_date, end_date)
    statsURL    = api_string

    # Get the latest stats for all players (passed on the start and end date)
    # We get all the stats for all the players on the server - then we filter based on who is currently in discord
    all_stats = get_json_from_api(statsURL)
    print("STATS FROM API [all_stats]]")
    print(all_stats)
    print("")

    # Get the list of players being passed to the API from discord via JSON
    discord_players = request.get_json()
    print("PLAYERS FROM DISCORD [discord_players]")
    print(discord_players)
    print("")

    # Get the captains from discord_players (should be 2)
    captains = []
    for player in discord_players:
        if player['captain'] == 'TRUE':
            captains.append(player['handle'])
    print("CAPTAINS FROM DISCORD [captains]")
    print(captains)
    print("")

    # Create an empty dictionary to store the player data (discord name, steam id, csgo handle)
    # This makes it easier to pass this information to the final function that creates the teams
    # The discord bot needs this info
    player_dict = {}
    # Loop through each player in the discord players list
    for player in discord_players:
        # Add the player data to the dictionary using the player name as the key
        player_dict[player['handle']] = {
            'steam_id': player['steam_id'],
            'discord': player['discord']
        }
    print("PLAYER DICTIONARY [player_dict]")
    print(player_dict)
    print("")

    # Get the list of player names from discord_players
    # We use this simple list to filter the stats to only the current players in discord
    print("PLAYER HANDLES FROM DISCORD [player_handles]")
    player_handles = []
    for player in discord_players:
        player_handles.append(player['handle'])
    print(player_handles)
    print("")
    
    # Filter stats for only the specified player handles
    filtered_stats = filter_player_stats(all_stats, player_handles)
    print("FILTERED STATS [filtered_stats]")
    print(filtered_stats)
    print("")

    # Create balanced teams within the specified threshold for only the filtered players
    teams = balance_teams(filtered_stats, threshold)

    # Check if balanced teams were possible for the specified players
    if len(teams) == 0:
        return jsonify({'error': 'Cannot balance teams with the given threshold and maximum number of attempts.'}), 400

    # Return the specified number of teams (sorted by difference in team scores in descending order)
    top_teams = get_top_teams(teams, player_dict, 10)

    # Serialize the response data to JSON format
    # Send back the top_teams
    response_data = json.dumps(top_teams)

    # filter the response data to only include the teams with the specified captains
    
    #print("FILTERED TEAMS")
    #print("")
    #print(captains[0])
    #print(captains[1])
    #print("")
    #filtered_data = filter_teams_by_captains(response_data, captains[0], captains[1])
    #print(json.dumps(filtered_data, indent=4))

    # Set the Content-Type header to indicate that the response is in JSON format
    headers = {'Content-Type': 'application/json'}

    # Return the JSON response with the appropriate headers
    return Response(response_data, headers=headers)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
