from django.shortcuts import render, redirect
from django.http import HttpResponse
from . import models as myModels
from datetime import date
from django import forms
from django.forms.formsets import formset_factory
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required


class SeasonChooser(forms.Form):
    season = forms.ModelChoiceField(
        queryset=myModels.Season.objects.all(),
        required=True
        )


class FixtureForm(forms.ModelForm):
    class Meta:
        model = myModels.Game
        fields = [
            'ourTeam', 'theirTeam', 'home', 'date'
        ]
        widgets = {
            'date' : forms.DateInput(attrs={"type" : "date"})
        }


class PlayerContributionForm(forms.Form):
    player = forms.ModelChoiceField(
        queryset=myModels.Player.objects.all(),
        required=False
        )
    goals = forms.IntegerField(required=False)
    assists = forms.IntegerField(required=False)
    yellow = forms.BooleanField(required=False)
    red = forms.BooleanField(required=False)
    motm = forms.BooleanField(required=False)


PlayerContributionsFormSet = formset_factory(
    PlayerContributionForm,
    extra=20
    )

class ResultForm(forms.ModelForm):
    class Meta:
        model = myModels.Game
        fields = [
            'ourScore',
            'theirScore'
        ]


class SquadForm(forms.ModelForm):
    class Meta:
        model = myModels.Squad
        fields = ['gk', 'rb', 'rcb', 'lcb', 'lb',
                  'rm', 'rcm', 'lcm', 'lm', 'rs', 'ls']
        
        
class confirmSquadForm(forms.Form):
    squad = forms.ModelChoiceField(
        widget=forms.HiddenInput,
        queryset=myModels.Squad.objects.all()
    )

def index(request):
    return(render(request, "points/index.html"))


@staff_member_required
def weeklyUpdate(request):
    if request.method == 'POST':
        form = SeasonChooser(request.POST)
        if form.is_valid():
            season = form.cleaned_data["season"]
            myModels.calcNewWeek(date.today(), season)
            messages.success(request, "Added a game week!")
            return redirect("/")
    form = None
    try:
        currentSeason = myModels.Season.objects.latest('startDate')
        form = SeasonChooser(initial={"season" : currentSeason})
    except:
        form = SeasonChooser()
    return render(
        request,
        "points/weekly_update.html",
        {"form" : form}
    )


@staff_member_required
def totalRecalc(request):
    if request.method == 'POST':
        form = SeasonChooser(request.POST)
        if form.is_valid():
            season = form.cleaned_data["season"]
            myModels.recalcWPP(season)
            myModels.totalRecollectFantasyPoints(season)
            messages.success(request, "Totally Recalculated and Recollected!")
            return redirect("/")
    form = None
    try:
        currentSeason = myModels.Season.objects.latest('startDate')
        form = SeasonChooser(initial={"season" : currentSeason})
    except:
        form = SeasonChooser()
    return render(
        request,
        "points/total_recalc.html",
        {"form" : form}
    )


@login_required
def manageTeam(request, season_id):
    allPlayers = {
        player.pk : (str(player.cost), str(player.team)) for player in (
            myModels.Player.objects.all()
        )
    }
    currentSeason = None        
    fantasy = None
    try:
        currentSeason = myModels.Season.objects.get(pk=season_id)
    except myModels.Season.DoesNotExist:
        return redirect("/")
    try:
        fantasy = myModels.Fantasy.objects.get(
            manager=request.user, season=currentSeason
            )
    except myModels.Fantasy.DoesNotExist:
        playerlessSquad = myModels.Squad.objects.create()
        fantasy = myModels.Fantasy.objects.create(
            manager=request.user,
            chemistry=float(0),
            currentSquad=playerlessSquad,
            season=currentSeason,
        )
    if request.method == 'POST':
        form = SquadForm(request.POST)
        if form.is_valid():
            newSquad: myModels.Squad = form.save()
            if newSquad.validate():
                chem, playersIn, playersOut = fantasy.chemTransfers(newSquad)
                newBudget = myModels.BUDGET - newSquad.cost()
                confirmForm = confirmSquadForm(initial={
                    "squad" : newSquad
                })
                return render(
                    request,
                    "points/check_transfers.html",
                    {
                        "confirmForm" : confirmForm,
                        "playersIn" : playersIn,
                        "playersOut" : playersOut,
                        "chemistryReduction" : chem,
                        "newBudget" : newBudget,
                        "season_id" : season_id,
                        "all_players" : allPlayers,
                    }
                    )
            else:
                messages.error(request, "Invalid Squad")
                return redirect("Manage Fantasy Team", season_id=season_id)
    form = SquadForm(instance=fantasy.currentSquad)
    currentCost = fantasy.currentSquad.cost()
    remainingBudget = myModels.BUDGET - currentCost
    return render(request, "points/fantasise_squad.html", context={
        "form" : form,
        "remainingBudget" : remainingBudget,
        "messages" : messages.get_messages(request),
        "all_players" : allPlayers,
        })


@login_required
def confirmTransfers(request, season_id):
    print("confirming transfers")
    fantasy = None
    currentSeason = None
    try:
        currentSeason = myModels.Season.objects.get(pk=season_id)
        fantasy = myModels.Fantasy.objects.get(
            manager=request.user, season=currentSeason)
    except myModels.Season.DoesNotExist:
        return redirect("/")
    except myModels.Fantasy.DoesNotExist:
        return redirect("Manage Fantasy Team", season_id=season_id)
    if request.method == 'POST':
        form = confirmSquadForm(request.POST)
        if form.is_valid():
            newSquad = form.cleaned_data['squad']
            if fantasy.makeTransfers(newSquad):
                messages.success(request, "Made Transfers")
                return redirect("Manage Fantasy Team", season_id=season_id)
            else:
                messages.error(request, "Invalid Squad")
                return redirect("Manage Fantasy Team", season_id=season_id)
    return redirect("Manage Fantasy Team", season_id=season_id)


@login_required
def createTeam(request, season_id):
    allPlayers = {
        player.pk : (str(player.cost), str(player.team)) for player in (
            myModels.Player.objects.all()
        )
    }
    currentSeason = None
    try:
        currentSeason = myModels.Season.objects.get(pk=season_id)
        myModels.Fantasy.objects.get(
            manager=request.user,
            season=currentSeason
            )
    except myModels.Season.DoesNotExist:
        return redirect("/")
    except myModels.Fantasy.DoesNotExist:
        if request.method == 'POST':
            form = SquadForm(request.POST)
            if form.is_valid():
                newSquad = form.save()
                if newSquad.validate():
                    myModels.Fantasy.objects.create(
                        manager=request.user,
                        chemistry=float(0),
                        currentSquad=newSquad,
                        season=currentSeason
                        )
                    return redirect("Manage Fantasy Team", season_id=season_id)
                else:
                    return redirect("Create Fantasy Team", season_id=season_id)
        form = SquadForm()
        return render(
            request,
            "points/fantasise_squad.html",
            {
                "form" : form,
                "all_players" : allPlayers,
            }
            )
    return redirect("Manage Fantasy Team", season_id=season_id)
    

def fantasyLeague(request, season_id):
    currentSeason = None
    try:
        currentSeason = myModels.Season.objects.get(pk=season_id)
    except myModels.Season.DoesNotExist:
        return redirect("/")
    fantasies = myModels.Fantasy.objects.filter(
        season=currentSeason
    ).order_by('-preCalcedPoints')
    context = {
        'fantasies' : fantasies
    }
    return render(request, 'points/fantasy_league.html', context)


@staff_member_required
def createFixture(request):
    if request.method == 'POST':
        form = FixtureForm(request.POST)
        if form.is_valid():
            fixture = form.save()
            return redirect("List of Games")
    form = FixtureForm()
    return render(request, 'points/create_fixture.html', {
        "form" : form
    })


def gameDetail(request, game_id):
    game = myModels.Game.objects.get(pk=game_id)
    events = myModels.PointScoringEvent.objects.filter(game=game)
    return render(request, 'points/game_detail.html', {
        'game' : game,
        'events' : events
    })


def gameList(request):
    games = myModels.Game.objects.all()
    return render(request, 'points/game_list.html', {
        "games" : games
    })


@staff_member_required
def updateGame(request, game_id):
    game = myModels.Game.objects.get(pk=game_id)
    if request.method == 'POST':
        resultForm = ResultForm(request.POST, instance=game) 
        playerContributionsFormSet = PlayerContributionsFormSet(
            request.POST,
            prefix = "contributions",
            )
        if (resultForm.is_valid() and playerContributionsFormSet.is_valid()):
            resultForm.instance.played = True
            resultForm.save()
            for contributionForm in playerContributionsFormSet:
                player = contributionForm.cleaned_data.get('player')
                if player is None:
                    continue
                myModels.PointScoringEvent.objects.create(
                    player=player,
                    game=game,
                    event=myModels.EventType.PLAYED
                )
                goals = contributionForm.cleaned_data.get('goals')
                if goals is not None:
                    for _ in range(goals):
                        myModels.PointScoringEvent.objects.create(
                            player=player,
                            game=game,
                            event=myModels.EventType.SCORED_GOAL
                        )
                assists = contributionForm.cleaned_data.get('assists')
                if assists is not None:
                    for _ in range(assists):
                        myModels.PointScoringEvent.objects.create(
                            player=player,
                            game=game,
                            event=myModels.EventType.ASSISTED_GOAL
                        )
                if contributionForm.cleaned_data.get('yellow'):
                    myModels.PointScoringEvent.objects.create(
                        player=player,
                        game=game,
                        event=myModels.EventType.YELLOW_CARD
                    )
                if contributionForm.cleaned_data.get('red'):
                    myModels.PointScoringEvent.objects.create(
                        player=player,
                        game=game,
                        event=myModels.EventType.RED_CARD
                    )
                if contributionForm.cleaned_data.get('motm'):
                    myModels.PointScoringEvent.objects.create(
                        player=player,
                        game=game,
                        event=myModels.EventType.MOTM
                    )
            return redirect("Game Detail", game_id=game_id)
    resultForm = ResultForm(instance=game)
    playerContributionsFormSet = PlayerContributionsFormSet(
        prefix="contributions",
        )
    return render(request, 'points/update_game.html', {
        "game_id" : game_id,
        "result_form" : resultForm,
        "contributions_formset" : playerContributionsFormSet
    })


def playerList(request):
    lastThreeWeeks = myModels.WeekCount.objects.order_by("-date")[:3]
    players = myModels.Player.objects.all()
    for player in players:
        player.vital_stats = player.getVitalStats()
        player.points_in_last_three_weeks = [
            player.pointsInWeek(week) for week in lastThreeWeeks]
    return render(request, 'points/player_list.html', {
        'lastThreeWeeks' : lastThreeWeeks,
        "players" : players
    })


def seasonList(request):
    seasons = myModels.Season.objects.all()
    return render(request, 'points/season_list.html', {
        "seasons" : seasons
    })


def seasonDetail(request, season_id):
    season = myModels.Season.objects.get(pk=season_id)
    return render(request, 'points/season_detail.html', {
        'season' : season,
    })


def playerDetail(request, player_id):
    player = myModels.Player.objects.get(pk=player_id)
    events = myModels.PointScoringEvent.objects.filter(player=player)
    return render(request, 'points/player_detail.html', {
        'player' : player,
        'events' : events
    })


def weekList(request, season_id):
    weeks = myModels.WeekCount.objects.filter(season_id=season_id)
    fantasy = myModels.Fantasy.objects.get(
        season_id=season_id, manager=request.user)
    fsws = myModels.FantasySquadWeek.objects.filter(
        week__in=weeks, fantasy=fantasy
    )
    return render(request, 'points/week_list.html', context={
        'fsws' : fsws,
        'season' : season_id
    })


def weekDetail(request, season_id, week_id):
    fantasy = myModels.Fantasy.objects.get(
        season_id=season_id, manager=request.user)
    fsw = myModels.FantasySquadWeek.objects.get(
        fantasy=fantasy, week_id=week_id)
    posPlayers = fsw.squad.toDict()
    posPlayerPoints = {
        position: myModels.WeekPlayerPoints.objects.get(
            week_id=week_id, player=player
            ) for position, player in posPlayers.items()}
    return render(request, 'points/week_detail.html', context={
        'fsw' : fsw,
        'posPlayerPoints' : posPlayerPoints
    })