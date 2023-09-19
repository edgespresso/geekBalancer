# geekBalancer

Python program to balance CSGO teams based on player stats from GeekFest.

v1.0 [Sep 2023]
 - Receives player names from GF Discord
 - Retrieves latest stats from Geekfest Stats for each player
 - Calculates a composite score (9 metrics: kills/deaths/assists over last 60 days, ;ast 120 days, etc)
 - Creates balanced teams (Alpha / Bravo) with a total team score differential within a specified threshold
 - Ensures the captains are on different teams
 - Simple logging
