from django.test import TestCase

from .models import TransferWindow
from .models import Position, EventType
from .models import Season, Team, Player
from .models import User, Squad, Fantasy
from .models import Game, PointScoringEvent

# Create your tests here.

class FantasyPointsTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:

        season = Season.objects.create(name="Test Season", startDate="2024-01-01")

        team1 = Team.objects.create(name="Team 1")
        team2 = Team.objects.create(name="Team 2")
        team3 = Team.objects.create(name="Team 3")
        team4 = Team.objects.create(name="Team 4")

        t1_gk1=Player.objects.create(
            name="Raydale",
            team=team1,
            position=Position.GOALKEEPER,
            cost=70
        )
        t1_def1=Player.objects.create(
            name="Zimber",
            team=team1,
            position=Position.DEFENDER,
            cost=70
        )
        t1_def2=Player.objects.create(
            name="Sabiel",
            team=team1,
            position=Position.DEFENDER,
            cost=100
        )
        t1_def3=Player.objects.create(
            name="Kiwing",
            team=team1,
            position=Position.DEFENDER,
            cost=60
        )
        t1_def4=Player.objects.create(
            name="Calite",
            team=team1,
            position=Position.DEFENDER,
            cost=90
        )
        t1_mid1=Player.objects.create(
            name="Sternelli",
            team=team1,
            position=Position.MIDFIELDER,
            cost=120
        )
        t1_mid2=Player.objects.create(
            name="Oderi",
            team=team1,
            position=Position.MIDFIELDER,
            cost=150
        )
        t1_mid3=Player.objects.create(
            name="Ricinho",
            team=team1,
            position=Position.MIDFIELDER,
            cost=60
        )
        t1_mid4=Player.objects.create(
            name="Raka",
            team=team1,
            position=Position.MIDFIELDER,
            cost=160
        )
        t1_fwd1=Player.objects.create(
            name="Trovertz",
            team=team1,
            position=Position.FORWARD,
            cost=110
        )
        t1_fwd2=Player.objects.create(
            name="Girott",
            team=team1,
            position=Position.FORWARD,
            cost=70
        )


        t2_gk1=Player.objects.create(
            name="Arez",
            team=team2,
            position=Position.GOALKEEPER,
            cost=60
        )
        t2_def1=Player.objects.create(
            name="Chillames",
            team=team2,
            position=Position.DEFENDER,
            cost=70
        )
        t2_def2=Player.objects.create(
            name="Rudihill",
            team=team2,
            position=Position.DEFENDER,
            cost=60
        )
        t2_def3=Player.objects.create(
            name="Telva",
            team=team2,
            position=Position.DEFENDER,
            cost=70
        )
        t2_def4=Player.objects.create(
            name="Azpella",
            team=team2,
            position=Position.DEFENDER,
            cost=60
        )
        t2_mid1=Player.objects.create(
            name="Lampack",
            team=team2,
            position=Position.MIDFIELDER,
            cost=80
        )
        t2_mid2=Player.objects.create(
            name="Matien",
            team=team2,
            position=Position.MIDFIELDER,
            cost=50
        )
        t2_fwd1=Player.objects.create(
            name="Pagba",
            team=team2,
            position=Position.FORWARD,
            cost=170
        )
        t3_gk1=Player.objects.create(
            name="Vicis",
            team=team3,
            position=Position.GOALKEEPER,
            cost=60
        )
        t3_def1=Player.objects.create(
            name="Vertoven",
            team=team3,
            position=Position.DEFENDER,
            cost=90
        )
        t3_mid1=Player.objects.create(
            name="Madisevski",
            team=team3,
            position=Position.MIDFIELDER,
            cost=110
        )
        t3_mid2=Player.objects.create(
            name="Hojbelso",
            team=team3,
            position=Position.MIDFIELDER,
            cost=50
        )
        t3_fwd1=Player.objects.create(
            name="Kon",
            team=team3,
            position=Position.FORWARD,
            cost=160
        )
        t4_def1=Player.objects.create(
            name="Robold",
            team=team4,
            position=Position.DEFENDER,
            cost=120
        )
        t4_def2=Player.objects.create(
            name="Virgip",
            team=team4,
            position=Position.DEFENDER,
            cost=80
        )
        t4_mid1=Player.objects.create(
            name="Hendinho",
            team=team4,
            position=Position.MIDFIELDER,
            cost=60
        )
        t4_mid2=Player.objects.create(
            name="Salister",
            team=team4,
            position=Position.MIDFIELDER,
            cost=140
        )
        t4_fwd1=Player.objects.create(
            name="Firmigi",
            team=team4,
            position=Position.FORWARD,
            cost=110
        )

        cls.squad=Squad.objects.create(
            gk=t3_gk1,
            rb=t1_def1,
            rcb=t1_def2,
            lcb=t2_def1,
            lb=t2_def2,
            rm=t3_mid1,
            rcm=t4_mid1,
            lcm=t3_mid2,
            lm=t2_mid1,
            rs=t1_fwd1,
            ls=t4_fwd1
        )

        user = User.objects.create(username="testuser")

        fantasy = Fantasy.objects.create(
            manager=user,
            chemistry=float(0),
            currentSquad=cls.squad,
            season=season
        )

        game1 = Game.objects.create(
            ourTeam=team1,
            theirTeam="Test Opponent 1",
            ourScore=3,
            theirScore=1,
            home=True,
            played=True,
            date="2024-01-15"
        )

        for p in [
            t1_gk1,
            t1_def1,
            t1_def2,
            t1_def3,
            t1_def4,
            t1_mid1,
            t1_mid2,
            t1_mid3,
            t1_mid4,
            t1_fwd1,
            t1_fwd2
        ]:
            PointScoringEvent.objects.create(
                player=p,
                game=game1,
                event=EventType.PLAYED
            )

        PointScoringEvent.objects.create(
            player=t1_fwd1,
            game=game1,
            event=EventType.SCORED_GOAL
        )
        PointScoringEvent.objects.create(
            player=t1_fwd1,
            game=game1,
            event=EventType.SCORED_GOAL
        )
        PointScoringEvent.objects.create(
            player=t1_mid1,
            game=game1,
            event=EventType.SCORED_GOAL
        )
        PointScoringEvent.objects.create(
            player=t1_mid2,
            game=game1,
            event=EventType.ASSISTED_GOAL
        )
        PointScoringEvent.objects.create(
            player=t1_mid3,
            game=game1,
            event=EventType.ASSISTED_GOAL
        )
        PointScoringEvent.objects.create(
            player=t1_def2,
            game=game1,
            event=EventType.YELLOW_CARD
        )
        PointScoringEvent.objects.create(
            player=t1_mid1,
            game=game1,
            event=EventType.MOTM
        )

        game2 = Game.objects.create(
            ourTeam=team1,
            theirTeam="Test Opponent 2",
            ourScore=0,
            theirScore=2,
            home=False,
            played=True,
            date="2024-01-15"
        )

        for p in [
            t2_gk1,
            t2_def1,
            t2_def2,
            t2_def3,
            t2_def4,
            t2_mid1,
            t2_mid2,
            t3_mid1,
            t3_mid2,
            t2_fwd1,
            t3_fwd1
        ]:
            PointScoringEvent.objects.create(
                player=p,
                game=game1,
                event=EventType.PLAYED
            )

        PointScoringEvent.objects.create(
            player=t2_mid1,
            game=game1,
            event=EventType.MOTM
        )
        
        return super().setUpTestData()
    
    def test_squad_cost(self):
        self.assertAlmostEqual(self.squad.cost(), 880)

    def test_valid_squad_is_valid(self):
        tw = TransferWindow.getInstance()
        if tw.sameSquadMax > 3 and tw.budget > 880:
            self.assertTrue(self.squad.validate())
