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

        cls.t1_gk1 = Player.objects.create(
            name="Raydale",
            team=team1,
            position=Position.GOALKEEPER,
            cost=70
        )
        cls.t1_def1 = Player.objects.create(
            name="Zimber",
            team=team1,
            position=Position.DEFENDER,
            cost=70
        )
        cls.t1_def2 = Player.objects.create(
            name="Sabiel",
            team=team1,
            position=Position.DEFENDER,
            cost=100
        )
        cls.t1_def3 = Player.objects.create(
            name="Kiwing",
            team=team1,
            position=Position.DEFENDER,
            cost=60
        )
        cls.t1_def4 = Player.objects.create(
            name="Calite",
            team=team1,
            position=Position.DEFENDER,
            cost=90
        )
        cls.t1_mid1 = Player.objects.create(
            name="Sternelli",
            team=team1,
            position=Position.MIDFIELDER,
            cost=120
        )
        cls.t1_mid2 = Player.objects.create(
            name="Oderi",
            team=team1,
            position=Position.MIDFIELDER,
            cost=150
        )
        cls.t1_mid3 = Player.objects.create(
            name="Ricinho",
            team=team1,
            position=Position.MIDFIELDER,
            cost=60
        )
        cls.t1_mid4 = Player.objects.create(
            name="Raka",
            team=team1,
            position=Position.MIDFIELDER,
            cost=160
        )
        cls.t1_fwd1 = Player.objects.create(
            name="Trovertz",
            team=team1,
            position=Position.FORWARD,
            cost=110
        )
        cls.t1_fwd2 = Player.objects.create(
            name="Girott",
            team=team1,
            position=Position.FORWARD,
            cost=70
        )
        cls.t2_gk1 = Player.objects.create(
            name="Arez",
            team=team2,
            position=Position.GOALKEEPER,
            cost=60
        )
        cls.t2_def1 = Player.objects.create(
            name="Chillames",
            team=team2,
            position=Position.DEFENDER,
            cost=70
        )
        cls.t2_def2 = Player.objects.create(
            name="Rudihill",
            team=team2,
            position=Position.DEFENDER,
            cost=60
        )
        cls.t2_def3 = Player.objects.create(
            name="Telva",
            team=team2,
            position=Position.DEFENDER,
            cost=70
        )
        cls.t2_def4 = Player.objects.create(
            name="Azpella",
            team=team2,
            position=Position.DEFENDER,
            cost=60
        )
        cls.t2_mid1 = Player.objects.create(
            name="Lampack",
            team=team2,
            position=Position.MIDFIELDER,
            cost=80
        )
        cls.t2_mid2 = Player.objects.create(
            name="Matien",
            team=team2,
            position=Position.MIDFIELDER,
            cost=50
        )
        cls.t2_fwd1 = Player.objects.create(
            name="Pagba",
            team=team2,
            position=Position.FORWARD,
            cost=170
        )
        cls.t3_gk1 = Player.objects.create(
            name="Vicis",
            team=team3,
            position=Position.GOALKEEPER,
            cost=60
        )
        cls.t3_def1 = Player.objects.create(
            name="Vertoven",
            team=team3,
            position=Position.DEFENDER,
            cost=90
        )
        cls.t3_mid1 = Player.objects.create(
            name="Madisevski",
            team=team3,
            position=Position.MIDFIELDER,
            cost=110
        )
        cls.t3_mid2 = Player.objects.create(
            name="Hojbelso",
            team=team3,
            position=Position.MIDFIELDER,
            cost=50
        )
        cls.t3_fwd1 = Player.objects.create(
            name="Kon",
            team=team3,
            position=Position.FORWARD,
            cost=160
        )
        cls.t4_def1 = Player.objects.create(
            name="Robold",
            team=team4,
            position=Position.DEFENDER,
            cost=120
        )
        cls.t4_def2 = Player.objects.create(
            name="Virgip",
            team=team4,
            position=Position.DEFENDER,
            cost=80
        )
        cls.t4_mid1 = Player.objects.create(
            name="Hendinho",
            team=team4,
            position=Position.MIDFIELDER,
            cost=60
        )
        cls.t4_mid2 = Player.objects.create(
            name="Salister",
            team=team4,
            position=Position.MIDFIELDER,
            cost=140
        )
        cls.t4_fwd1 = Player.objects.create(
            name="Firmigi",
            team=team4,
            position=Position.FORWARD,
            cost=110
        )

        cls.squad1 = Squad.objects.create(
            gk=cls.t3_gk1,
            rb=cls.t1_def1,
            rcb=cls.t1_def2,
            lcb=cls.t2_def1,
            lb=cls.t2_def2,
            rm=cls.t3_mid1,
            rcm=cls.t4_mid1,
            lcm=cls.t3_mid2,
            lm=cls.t2_mid1,
            rs=cls.t1_fwd1,
            ls=cls.t4_fwd1
        )

        user1 = User.objects.create(username="testuser")

        cls.fantasy1 = Fantasy.objects.create(
            manager=user1,
            chemistry=float(0),
            currentSquad=cls.squad1,
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
            cls.t1_gk1,
            cls.t1_def1,
            cls.t1_def2,
            cls.t1_def3,
            cls.t1_def4,
            cls.t1_mid1,
            cls.t1_mid2,
            cls.t1_mid3,
            cls.t1_mid4,
            cls.t1_fwd1,
            cls.t1_fwd2
        ]:
            PointScoringEvent.objects.create(
                player=p,
                game=game1,
                event=EventType.PLAYED
            )

        PointScoringEvent.objects.create(
            player=cls.t1_fwd1,
            game=game1,
            event=EventType.SCORED_GOAL
        )
        PointScoringEvent.objects.create(
            player=cls.t1_fwd1,
            game=game1,
            event=EventType.SCORED_GOAL
        )
        PointScoringEvent.objects.create(
            player=cls.t1_mid1,
            game=game1,
            event=EventType.SCORED_GOAL
        )
        PointScoringEvent.objects.create(
            player=cls.t1_mid2,
            game=game1,
            event=EventType.ASSISTED_GOAL
        )
        PointScoringEvent.objects.create(
            player=cls.t1_mid3,
            game=game1,
            event=EventType.ASSISTED_GOAL
        )
        PointScoringEvent.objects.create(
            player=cls.t1_def2,
            game=game1,
            event=EventType.YELLOW_CARD
        )
        PointScoringEvent.objects.create(
            player=cls.t1_mid1,
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
            cls.t2_gk1,
            cls.t2_def1,
            cls.t2_def2,
            cls.t2_def3,
            cls.t2_def4,
            cls.t2_mid1,
            cls.t2_mid2,
            cls.t3_mid1,
            cls.t3_mid2,
            cls.t2_fwd1,
            cls.t3_fwd1
        ]:
            PointScoringEvent.objects.create(
                player=p,
                game=game1,
                event=EventType.PLAYED
            )

        PointScoringEvent.objects.create(
            player=cls.t2_mid1,
            game=game1,
            event=EventType.MOTM
        )

        cls.tw = TransferWindow.getInstance()
        
        return super().setUpTestData()
    
    def test_squad_cost(self):
        self.assertAlmostEqual(self.squad1.cost(), 880)

    def test_valid_squad_is_valid(self):
        self.tw.sameSquadMax = 3
        self.tw.budget = 881
        self.tw.save()
        self.assertTrue(self.squad1.validate())

    # test invalid versions of everything too. next
    # check cant make team with null player

    def test_valid_make_transfers(self):
        self.tw.sameSquadMax = 4
        self.tw.budget = 891
        self.tw.shut = False
        self.tw.reactivity = float(1)
        self.tw.save()
        newSquad=Squad.objects.create(
            gk=self.t1_gk1,
            rb=self.t1_def1,
            rcb=self.t1_def2,
            lcb=self.t2_def1,
            lb=self.t2_def2,
            rm=self.t3_mid1,
            rcm=self.t4_mid1,
            lcm=self.t3_mid2,
            lm=self.t2_mid1,
            rs=self.t1_fwd1,
            ls=self.t4_fwd1
        )
        self.assertTrue(self.fantasy1.makeTransfers(newSquad))
        print(self.fantasy1.currentSquad)
        self.assertAlmostEqual(self.fantasy1.chemistry, float(-1))
