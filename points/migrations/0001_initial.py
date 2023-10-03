# Generated by Django 4.2.5 on 2023-10-02 23:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Fantasy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chemistry', models.FloatField()),
                ('preCalcedPoints', models.FloatField(default=0.0)),
            ],
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('theirTeam', models.CharField(max_length=50)),
                ('ourScore', models.IntegerField(null=True)),
                ('theirScore', models.IntegerField(null=True)),
                ('home', models.BooleanField()),
                ('played', models.BooleanField(default=False)),
                ('date', models.DateField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('position', models.CharField(choices=[('GK', 'Goal Keeper'), ('DEF', 'Defender'), ('MID', 'Midfielder'), ('FWD', 'Forward')], max_length=50)),
                ('cost', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Season',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('startDate', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('name', models.CharField(max_length=50, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='WeekCount',
            fields=[
                ('count', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('date', models.DateField()),
                ('season', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='points.season')),
            ],
        ),
        migrations.CreateModel(
            name='WeekPlayerPoints',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('played', models.BooleanField()),
                ('points', models.FloatField()),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='points.player')),
                ('week', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='points.weekcount')),
            ],
        ),
        migrations.CreateModel(
            name='Squad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gk', models.ForeignKey(limit_choices_to={'position': 'GK'}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='squadGK', to='points.player', verbose_name='Goalkeeper')),
                ('lb', models.ForeignKey(limit_choices_to={'position': 'DEF'}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='squadLB', to='points.player', verbose_name='Left Back')),
                ('lcb', models.ForeignKey(limit_choices_to={'position': 'DEF'}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='squadLCB', to='points.player', verbose_name='Left Centre Back')),
                ('lcm', models.ForeignKey(limit_choices_to={'position': 'MID'}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='squadLCM', to='points.player', verbose_name='Left Centre Mid')),
                ('lm', models.ForeignKey(limit_choices_to={'position': 'MID'}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='squadLM', to='points.player', verbose_name='Left Mid')),
                ('ls', models.ForeignKey(limit_choices_to={'position': 'FWD'}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='squadLS', to='points.player', verbose_name='Left Striker')),
                ('rb', models.ForeignKey(limit_choices_to={'position': 'DEF'}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='squadRB', to='points.player', verbose_name='Right Back')),
                ('rcb', models.ForeignKey(limit_choices_to={'position': 'DEF'}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='squadRCB', to='points.player', verbose_name='Right Centre Back')),
                ('rcm', models.ForeignKey(limit_choices_to={'position': 'MID'}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='squadRCM', to='points.player', verbose_name='Right Centre Mid')),
                ('rm', models.ForeignKey(limit_choices_to={'position': 'MID'}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='squadRM', to='points.player', verbose_name='Right Mid')),
                ('rs', models.ForeignKey(limit_choices_to={'position': 'FWD'}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='squadRS', to='points.player', verbose_name='Right Striker')),
            ],
        ),
        migrations.CreateModel(
            name='PointScoringEvent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event', models.CharField(choices=[('Played', 'Touched Grass'), ('Goal', 'Goal'), ('Assist', 'Assist'), ('Yellow', '1 Yellow'), ('Red', 'Straight Red / 2 Yellows'), ('MOTM', 'Man of the Match')], max_length=50)),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='points.game')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='points.player')),
            ],
        ),
        migrations.AddField(
            model_name='player',
            name='team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='points.team'),
        ),
        migrations.AddField(
            model_name='game',
            name='ourTeam',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='points.team'),
        ),
        migrations.AddField(
            model_name='game',
            name='week',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='points.weekcount'),
        ),
        migrations.CreateModel(
            name='FantasySquadWeek',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chemistry', models.FloatField()),
                ('preCalcedPoints', models.FloatField(null=True)),
                ('fantasy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='points.fantasy')),
                ('squad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='points.squad')),
                ('week', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='points.weekcount')),
            ],
        ),
        migrations.AddField(
            model_name='fantasy',
            name='currentSquad',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='points.squad'),
        ),
        migrations.AddField(
            model_name='fantasy',
            name='manager',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='fantasy',
            name='season',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='points.season'),
        ),
    ]
