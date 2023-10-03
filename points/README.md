# The Models

- WeekCount: like a game week number.
- Team: real team.
- Player: real player.
- Game: real football match.
- PointScoringEvent: players make these in games.
- WeekPlayerPoints: number of points for a real player in a week.
- Fantasy: fantasy team.
- FantasyPlayer: presence of a real player in a fantasy.
- FantasyInvolvement: what a real player contributed to a fantasy.
- normalizeGoals, teamModifiers: helper functions for calculating scores.

Games award points. Fantasies collect points.

Maybe the way I do formations is a little silly..

I invented the scoring system in normalizeGoals and teamModifiers.
Feel free to change it.

# Important Notes

- Games don't have a week or season at creation, they get assigned
one at awarding.