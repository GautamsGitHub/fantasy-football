"""
URL configuration for Fantasy project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views

urlpatterns = [
    path("<int:season_id>/manage_fantasy", views.manageTeam, name="Manage Fantasy Team"),
    path("<int:season_id>/create_fantasy", views.createTeam, name="Create Fantasy Team"),
    path("new_fixture", views.createFixture, name="Create Fixture"),
    path("<int:season_id>/table", views.fantasyLeague, name="Fantasy League"),
    path('game/<int:game_id>/', views.gameDetail, name='Game Detail'),
    path('player/<int:player_id>/', views.playerDetail, name='Player Detail'),
    path('update_game/<int:game_id>/', views.updateGame, name='Update Game'),
    path('games', views.gameList, name="List of Games"),
    path('players', views.playerList, name="List of Players"),
    path('confirm_transfers', views.confirmTransfers, name="Confirm Transfers"),
    path('weekly_update', views.weeklyUpdate, name="Weekly Update"),
    path('total_recalc', views.totalRecalc, name="Total Recalculation and Recollection"),
    path("", views.welcome, name="Welcome")
]
