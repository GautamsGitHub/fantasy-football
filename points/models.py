from django.db import models
from django.contrib.auth.models import User
from typing import Iterable
from datetime import date
from collections import Counter


class TransferWindow(models.Model):
    shut = models.BooleanField(default=False)
    budget = models.FloatField(default=1000)
    squadSize = models.IntegerField(default=11)
    sameSquadMax = models.IntegerField(default=4)
    reactivity = models.FloatField(default=1.0)

    def save(self, *args, **kwargs):
        self.pk = 1
        super(TransferWindow, self).save(*args, **kwargs)

    @classmethod
    def getInstance(cls):
        return cls.objects.get_or_create(pk=1)[0]
        

class Season(models.Model):
    name = models.CharField(max_length=50)
    startDate = models.DateField()

    def __str__(self) -> str:
        return self.name


class WeekCount(models.Model):
    count = models.AutoField(primary_key=True, auto_created=True)
    date = models.DateField()
    season = models.ForeignKey(Season, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"Week Added {self.date}"


class Team(models.Model):
    name = models.CharField(max_length=50, primary_key=True)

    def __str__(self) -> str:
        return self.name


class Position(models.TextChoices):
    GOALKEEPER = "GK", "Goal Keeper"
    DEFENDER = "DEF", "Defender"
    MIDFIELDER = "MID", "Midfielder"
    FORWARD = "FWD", "Forward"


class Player(models.Model):
    name = models.CharField(max_length=50)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    position = models.CharField(choices=Position.choices, max_length=50)
    cost = models.FloatField()

    def __str__(self) -> str:
        return self.name
    
    def getVitalStats(self):
        playerEvents = PointScoringEvent.objects.filter(
            player=self)
        played = playerEvents.filter(event=EventType.PLAYED).count()
        goals = playerEvents.filter(event=EventType.SCORED_GOAL).count()
        assists = playerEvents.filter(event=EventType.ASSISTED_GOAL).count()
        return {
            "played" : played,
            "goals" : goals,
            "assists" : assists
        }
    
    def pointsInWeek(self, week):
        return WeekPlayerPoints.objects.get(week=week, player=self).points


class Squad(models.Model):
    gk = models.ForeignKey(Player, null=True, on_delete=models.SET_NULL,
                           limit_choices_to={"position": Position.GOALKEEPER},
                           related_name="squadGK",
                           verbose_name="Goalkeeper")
    rb = models.ForeignKey(Player, null=True, on_delete=models.SET_NULL,
                           limit_choices_to={"position": Position.DEFENDER},
                           related_name="squadRB",
                           verbose_name="Right Back")
    rcb = models.ForeignKey(Player, null=True, on_delete=models.SET_NULL,
                            limit_choices_to={"position": Position.DEFENDER},
                            related_name="squadRCB",
                            verbose_name="Right Centre Back")
    lcb = models.ForeignKey(Player, null=True, on_delete=models.SET_NULL,
                            limit_choices_to={"position": Position.DEFENDER},
                            related_name="squadLCB",
                            verbose_name="Left Centre Back")
    lb = models.ForeignKey(Player, null=True, on_delete=models.SET_NULL,
                           limit_choices_to={"position": Position.DEFENDER},
                           related_name="squadLB",
                           verbose_name="Left Back")
    rm = models.ForeignKey(Player, null=True, on_delete=models.SET_NULL,
                           limit_choices_to={"position": Position.MIDFIELDER},
                           related_name="squadRM",
                           verbose_name="Right Mid")
    rcm = models.ForeignKey(Player, null=True, on_delete=models.SET_NULL,
                            limit_choices_to={"position": Position.MIDFIELDER},
                            related_name="squadRCM",
                            verbose_name="Right Centre Mid")
    lcm = models.ForeignKey(Player, null=True, on_delete=models.SET_NULL,
                            limit_choices_to={"position": Position.MIDFIELDER},
                            related_name="squadLCM",
                            verbose_name="Left Centre Mid")
    lm = models.ForeignKey(Player, null=True, on_delete=models.SET_NULL,
                           limit_choices_to={"position": Position.MIDFIELDER},
                           related_name="squadLM",
                           verbose_name="Left Mid")
    rs = models.ForeignKey(Player, null=True, on_delete=models.SET_NULL,
                           limit_choices_to={"position": Position.FORWARD},
                           related_name="squadRS",
                           verbose_name="Right Striker")
    ls = models.ForeignKey(Player, null=True, on_delete=models.SET_NULL,
                           limit_choices_to={"position": Position.FORWARD},
                           related_name="squadLS",
                           verbose_name="Left Striker")

    
    def toSet(self):
        return ({
            self.gk,
            self.rb,
            self.rcb,
            self.lcb,
            self.lb,
            self.rm,
            self.rcm,
            self.lcm,
            self.lm,
            self.rs,
            self.ls
        })
    
    def toDict(self):
        return ({
            "GK" : self.gk,
            "RB" : self.rb,
            "RCB" : self.rcb,
            "LCB" : self.lcb,
            "LB" : self.lb,
            "RM" : self.rm,
            "RCM" : self.rcm,
            "LCM" : self.lcm,
            "LM" : self.lm,
            "RS" : self.rs,
            "LS" : self.ls
        })
    
    def cost(self):
        return (sum(list(map(lambda p: p.cost if p is not None else 0, self.toSet()))))
    
    def validate(self):
        c = Counter([p.team for p in self.toSet()])
        return (
            len(self.toSet()) == TransferWindow.getInstance().squadSize
            and (TransferWindow.getInstance().budget >= self.cost())
            and (c.most_common(1)[0][1] <= TransferWindow.getInstance().sameSquadMax)
        )

class EventType(models.TextChoices):
    PLAYED = "Played", "Touched Grass"
    SCORED_GOAL = "Goal", "Goal"
    ASSISTED_GOAL = "Assist", "Assist"
    YELLOW_CARD = "Yellow", "1 Yellow"
    RED_CARD = "Red", "Straight Red / 2 Yellows"
    MOTM = "MOTM", "Man of the Match"


class Game(models.Model):
    ourTeam = models.ForeignKey(Team, on_delete=models.CASCADE)
    theirTeam = models.CharField(max_length=50)
    ourScore = models.IntegerField(null=True)
    theirScore = models.IntegerField(null=True)
    home = models.BooleanField()
    played = models.BooleanField(default=False)
    week = models.ForeignKey(
        WeekCount, on_delete=models.SET_NULL, null=True)
    date = models.DateField(null=True)

    def awardPoints(self, weekCount):
        mods = teamModifiers(self)
        currentWeek = WeekPlayerPoints.objects.filter(week=weekCount)
        events = PointScoringEvent.objects.filter(game=self)
        for e in events:
            toChange = currentWeek.get(player=e.player)
            if e.event == EventType.PLAYED:
                toChange.played = True
                if e.player.position == Position.GOALKEEPER:
                    toChange.points += mods["gk"]
                elif e.player.position == Position.DEFENDER:
                    toChange.points += mods["d"]
                elif e.player.position == Position.MIDFIELDER:
                    toChange.points += mods["m"]
                elif e.player.position == Position.FORWARD:
                    toChange.points += mods["f"]
            elif e.event == EventType.SCORED_GOAL:
                toChange.points += 5
            elif e.event == EventType.ASSISTED_GOAL:
                toChange.points += 3
            elif e.event == EventType.MOTM:
                toChange.points += 8
            elif e.event == EventType.YELLOW_CARD:
                toChange.points -= 3
            elif e.event == EventType.RED_CARD:
                toChange.points -= 7
            toChange.save()
        self.week = weekCount
        self.save()

    def __str__(self) -> str:
        if self.home:
            return f"{self.ourTeam} vs. {self.theirTeam}"
        else:
            return f"{self.theirTeam} vs. {self.ourTeam}"


class PointScoringEvent(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    event = models.CharField(choices=EventType.choices, max_length=50)

    def __str__(self) -> str:
        return f"{self.player} did {self.event} in {self.game}"


class WeekPlayerPoints(models.Model):
    week = models.ForeignKey(WeekCount, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    played = models.BooleanField()
    points = models.FloatField()


class Fantasy(models.Model):
    manager = models.ForeignKey(User, on_delete=models.CASCADE)
    chemistry = models.FloatField(default=float(0))
    currentSquad = models.ForeignKey(Squad, null=True, on_delete=models.SET_NULL)
    season = models.ForeignKey(Season, on_delete=models.CASCADE)

    preCalcedPoints = models.FloatField(default=0.0)

    def record(self, weekCount):
        FantasySquadWeek.objects.create(
            fantasy=self,
            week=weekCount,
            squad=self.currentSquad,
            chemistry=self.chemistry
        )
        self.chemistry = float(0)
        self.save()

    def weekRecollectPoints(self, weekCount):
        fsw = FantasySquadWeek.objects.get(fantasy=self, week=weekCount)
        self.preCalcedPoints += fsw.calcPoints()
        self.save()

    def totalRecollectPoints(self):
        seasonWeeks = WeekCount.objects.filter(season=self.season)
        fsws = FantasySquadWeek.objects.filter(
            fantasy=self, week__in=seasonWeeks)
        self.preCalcedPoints = sum([fsw.calcPoints() for fsw in fsws])
        self.save()
        return self.preCalcedPoints
        

    def chemTransfers(self, newSquad: Squad):
        playersIn = newSquad.toSet() - self.currentSquad.toSet()
        playersOut = self.currentSquad.toSet() - newSquad.toSet()
        signingCount = len(playersIn)
        return (
            float(signingCount) * TransferWindow.getInstance().reactivity,
            playersIn,
            playersOut
        )

    def makeTransfers(self, newSquad: Squad):
        if TransferWindow.getInstance().shut:
            return False
        if (newSquad.validate()):
            self.chemistry -= self.chemTransfers(newSquad)[0]
            self.currentSquad = newSquad
            self.save()
            return True
        else:
            return False
        
    def __str__(self) -> str:
        return (f"Fantasy of {self.manager} for {self.season}")


class FantasySquadWeek(models.Model):
    fantasy = models.ForeignKey(Fantasy, on_delete=models.CASCADE)
    week = models.ForeignKey(WeekCount, on_delete=models.CASCADE)
    squad = models.ForeignKey(Squad, on_delete=models.CASCADE)
    chemistry = models.FloatField()

    preCalcedPoints = models.FloatField(null=True)

    def calcPoints(self):
        self.preCalcedPoints = (
            self.chemistry
            + sum(list(map(
                lambda wpp: wpp.points,
                WeekPlayerPoints.objects.filter(
                    week=self.week,
                    player__in=self.squad.toSet()
                    ))))
        )
        self.save()
        return self.preCalcedPoints
    
    def __str__(self) -> str:
        return (f"{self.fantasy} in {self.week}")


def normalizeGoals(n):
    gs = [0, 2, 3.5, 4.4]
    if n < 0:
        return -normalizeGoals(-n)
    elif n > 3:
        return (n+6)*0.5
    else:
        return gs[n]


def teamModifiers(game: Game):
    teamMod = 1
    if game.home: teamMod = 0
    if game.ourScore < game.theirScore: teamMod -= 2
    elif game.ourScore > game.theirScore: teamMod += 2
    teamMod += normalizeGoals(game.ourScore - game.theirScore)
    gkMod = 6.5 + teamMod - normalizeGoals(game.theirScore)
    dMod = 4 + teamMod - 0.8*normalizeGoals(game.theirScore)
    mMod = teamMod + normalizeGoals(game.ourScore - game.theirScore)*0.75
    fMod = teamMod + 0.9*normalizeGoals(game.ourScore)
    return {
        "gk": gkMod,
        "d": dMod,
        "m": mMod,
        "f": fMod,
    }


def zeroPlayersWeek(weekCount):
    players = Player.objects.all()
    # maybe list(map...)
    WeekPlayerPoints.objects.filter(week=weekCount).delete()
    zeroPlayers = map(lambda p: WeekPlayerPoints(
        week=weekCount, player=p, points=0, played=False
        ), players)
    WeekPlayerPoints.objects.bulk_create(zeroPlayers)

def awardPoints(weekCount, games: Iterable[Game]):
    zeroPlayersWeek(weekCount)
    for g in games:
        g.awardPoints(weekCount)

def recordAndCollectFantasies(weekCount: WeekCount):
    fantasies = Fantasy.objects.filter(season=weekCount.season)
    for f in fantasies:
        f.record(weekCount)
        f.weekRecollectPoints(weekCount)

def calcNewWeek(newDate, season):
    weekCount = WeekCount.objects.create(
        date=newDate,
        season=season
        )
    games = Game.objects.filter(
        models.Q(week__isnull=True) & models.Q(played=True)
        )
    awardPoints(weekCount, games)
    recordAndCollectFantasies(weekCount)

def recalcWPP(season):
    seasonWeeks = WeekCount.objects.filter(season=season)
    WeekPlayerPoints.objects.filter(week__in=seasonWeeks).delete()
    Fantasy.objects.filter(season=season).update(preCalcedPoints=0)
    games = Game.objects.filter(week__isnull=False)
    for week in seasonWeeks:
        awardPoints(week, games)

def totalRecollectFantasyPoints(season):
    for f in Fantasy.objects.filter(season=season):
        f.totalRecollectPoints()
