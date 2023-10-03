# from django.db import models
# from django.contrib.auth.models import User

# BUDGET = 500
# SQUAD_SIZE = 15

# class WeekCount(models.Model):
#     count = models.AutoField(primary_key=True, auto_created=True)
#     date = models.DateField()


# class Team(models.Model):
#     name = models.CharField(max_length=50, primary_key=True)


# class Position(models.TextChoices):
#     GOALKEEPER = "GK", "Goal Keeper"
#     DEFENDER = "DEF", "Defender"
#     MIDFIELDER = "MID", "Midfielder"
#     FORWARD = "FWD", "Forward"


# class Player(models.Model):
#     name = models.CharField(max_length=50, primary_key=True)
#     team = models.ForeignKey(Team, on_delete=models.CASCADE)
#     position = models.CharField(choices=Position.choices, max_length=50)
#     cost = models.FloatField()


# class EventType(models.TextChoices):
#     PLAYED = "Played", "Touched Grass"
#     SCORED_GOAL = "Goal", "Goal"
#     ASSISTED_GOAL = "Assist", "Assist"
#     YELLOW_CARD = "Yellow", "1 Yellow"
#     RED_CARD = "Red", "Straight Red / 2 Yellows"
#     MOTM = "MOTM", "Man of the Match"


# class Game(models.Model):
#     ourTeam = models.ForeignKey(Team, on_delete=models.PROTECT)
#     theirTeam = models.CharField(max_length=50)
#     ourScore = models.IntegerField()
#     theirScore = models.IntegerField()
#     home = models.BooleanField()
#     awarded = models.BooleanField()
#     week = models.ForeignKey(WeekCount, models.SET_NULL, null=True)
#     # date = models.DateField()

#     def awardPoints(self, weekCount):
#         mods = teamModifiers(self)
#         currentWeek = WeekPlayerPoints.objects.filter(week=weekCount)
#         events = PointScoringEvent.objects.filter(game=self)
#         for e in events:
#             toChange = currentWeek.get(player=e.player)
#             if e.event == EventType.PLAYED:
#                 toChange.played = True
#                 if e.player.position == Position.GOALKEEPER:
#                     toChange.points += mods["gk"]
#                 elif e.player.position == Position.DEFENDER:
#                     toChange.points += mods["d"]
#                 elif e.player.position == Position.MIDFIELDER:
#                     toChange.points += mods["m"]
#                 elif e.player.position == Position.FORWARD:
#                     toChange.points += mods["f"]
#             elif e.event == EventType.SCORED_GOAL:
#                 toChange.points += 5
#             elif e.event == EventType.ASSISTED_GOAL:
#                 toChange.points += 3
#             elif e.event == EventType.MOTM:
#                 toChange.points += 8
#             elif e.event == EventType.YELLOW_CARD:
#                 toChange.points -= 3
#             elif e.event == EventType.RED_CARD:
#                 toChange.points -= 7
#             toChange.save()
#         # could do in bulk perhaps
#         self.awarded = True
#         self.week = weekCount
#         self.save()


# class PointScoringEvent(models.Model):
#     player = models.ForeignKey(Player, on_delete=models.CASCADE)
#     game = models.ForeignKey(Game, on_delete=models.CASCADE)
#     event = models.CharField(choices=EventType.choices, max_length=50)


# class WeekPlayerPoints(models.Model):
#     week = models.ForeignKey(WeekCount, on_delete=models.PROTECT)
#     player = models.ForeignKey(Player, on_delete=models.CASCADE)
#     played = models.BooleanField()
#     points = models.FloatField()


# class Fantasy(models.Model):
#     manager = models.ForeignKey(User, on_delete=models.CASCADE)
#     chemistry = models.FloatField()
#     # totalPoints = models.IntegerField()
#     currentPlayers = models.ManyToManyField(Player, through="FantasyPlayer")
#     pastPlays = models.ManyToManyField(WeekPlayerPoints, through="FantasyInvolvement")

#     def collectPoints(self, weekCount):
#         squad = self.currentPlayers.all().order_by("fantasyplayer__depth")
#         hadGK = False
#         hadCount = 0
#         for p in squad:
#             playerPoints = WeekPlayerPoints.objects.get(week=weekCount, player=p)
#             ppplayed = False
#             if playerPoints.played and hadCount < 11 and (
#                 not ((p.position == Position.GOALKEEPER) & hadGK)
#                                                       ):
#                 ppplayed = True
#                 hadCount += 1
#                 if p.position == Position.GOALKEEPER:
#                     hadGK = True
#             fi = FantasyInvolvement.objects.create(
#                     fantasy=self, wpp=playerPoints, fromBench=ppplayed
#                 )
#             fi.save()

#     def makeTransfers(self, newSquad):
#         oldSquad = set(self.currentPlayers)
#         signingCount = len(set(newSquad) - oldSquad)
#         self.chemistry -= signingCount
#         self.currentPlayers.clear()
#         for i in range(SQUAD_SIZE):
#             FantasyPlayer.objects.create(
#                 fantasy=self,
#                 player=newSquad[i],
#                 depth=i+1
#                 )
            
#     def totalPoints(self):
#         return (
#             self.chemistry
#             + sum(list(map(
#                 lambda fi: fi.wpp.points,
#                 FantasyInvolvement.objects.filter(fantasy=self, onBench=False)
#                 )))
#         )


# class FantasyPlayer(models.Model):
#     fantasy = models.ForeignKey(Fantasy, on_delete=models.CASCADE)
#     player = models.ForeignKey(Player, on_delete=models.CASCADE)
#     depth = models.IntegerField() 


# class FantasyInvolvement(models.Model):
#     fantasy = models.ForeignKey(Fantasy, on_delete=models.CASCADE)
#     wpp = models.ForeignKey(WeekPlayerPoints, on_delete=models.CASCADE)
#     fromBench = models.BooleanField()


# def normalizeGoals(n):
#     gs = [0, 2, 3.5, 4.4]
#     if n < 0:
#         return -normalizeGoals(-n)
#     elif n > 3:
#         return (n+6)*0.5
#     else:
#         return gs[n]


# def teamModifiers(game: Game):
#     teamMod = 1
#     if game.home: teamMod = 0
#     if game.ourScore < game.theirScore: teamMod -= 2
#     elif game.ourScore > game.theirScore: teamMod += 2
#     teamMod += normalizeGoals(game.ourScore - game.theirScore)
#     gkMod = 6.5 + teamMod - normalizeGoals(game.theirScore)
#     dMod = 4 + teamMod - 0.8*normalizeGoals(game.theirScore)
#     mMod = teamMod + normalizeGoals(game.ourScore - game.theirScore)*0.75
#     fMod = teamMod + 0.9*normalizeGoals(game.ourScore)
#     return {
#         "gk": gkMod,
#         "d": dMod,
#         "m": mMod,
#         "f": fMod,
#     }


# def zeroPlayersWeek(newDate):
#     weekCount = WeekCount(date=newDate)
#     weekCount.save()
#     players = Player.objects.all()
#     # maybe list(map...)
#     zeroPlayers = map(lambda p: WeekPlayerPoints(
#         week=weekCount, player=p, points=0, played=False
#         ), players)
#     WeekPlayerPoints.objects.bulk_create(zeroPlayers)
#     return weekCount


# def awardPoints(newDate):
#     weekCount = zeroPlayersWeek(newDate)
#     games = Game.objects.filter(awarded=False)
#     for g in games:
#         g.awardPoints(weekCount)
#     fantasies = Fantasy.objects.all()
#     for f in fantasies:
#         f.collectPoints(weekCount)

# def validateSquad(squad):
#     gkCount = 0
#     dCount = 0
#     mCount = 0
#     fCount = 0
#     totalCost = 0
#     for player in squad:
#         totalCost += player.cost
#         if player.position == Position.GOALKEEPER:
#             gkCount += 1
#         elif player.position == Position.DEFENDER:
#             dCount += 1
#         elif player.position == Position.MIDFIELDER:
#             mCount += 1
#         elif player.position == Position.FORWARD:
#             fCount += 1
#     return (
#         (len(squad) == SQUAD_SIZE)
#         and (len(set(squad)) == SQUAD_SIZE)
#         and (gkCount == 2)
#         and (dCount == 5)
#         and (mCount == 5)
#         and (fCount == 3)
#         and (BUDGET >= totalCost)
#         and len()
#         )
