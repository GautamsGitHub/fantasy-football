from django.core.management.base import BaseCommand
from points.demo_utils.shared import create_demo_data

class Command(BaseCommand):
    help = 'Seeds the database with demo data for maintainers to explore the app.'

    def handle(self, *args, **options):
        from points.models import Season, Team, Player, Squad, Fantasy, Game, PointScoringEvent
        # Check for existing data (excluding auth/superuser)
        if (Season.objects.exists() or Team.objects.exists() or Player.objects.exists() or
            Squad.objects.exists() or Fantasy.objects.exists() or Game.objects.exists() or
            PointScoringEvent.objects.exists()):
            self.stdout.write(self.style.ERROR('Database is not empty. Aborting demo data seeding.'))
            self.stdout.write('If you want to reseed, please clear relevant tables first.')
            return
        demo = create_demo_data()
        self.stdout.write(self.style.SUCCESS('Demo data seeded successfully!'))
        self.stdout.write('Created objects:')
        self.stdout.write(f"  Season: {demo['season']}")
        self.stdout.write(f"  Teams: {[t.name for t in demo['teams']]}")
        self.stdout.write(f"  Players: {[p.name for p in demo['players']]}")
        self.stdout.write(f"  Squad: {demo['squad']}")
        self.stdout.write(f"  User: {demo['user']}")
        self.stdout.write(f"  Fantasy: {demo['fantasy']}")
        self.stdout.write(f"  Games: {[str(g) for g in demo['games']]}")
        self.stdout.write(f"  TransferWindow: {demo['transfer_window']}")
