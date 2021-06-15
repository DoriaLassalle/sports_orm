from django.shortcuts import render, redirect
from .models import League, Team, Player

from . import team_maker

def index(request):
	context = {
		#"leagues": League.objects.all(),
		"teams": Team.objects.all(),
		"players": Player.objects.all(),
		"baseballLeagues": League.objects.filter(sport="Baseball"),
		"womenLeagues":League.objects.filter(name__contains="women"),
		"hockeyLeagues":League.objects.filter(sport__contains="hockey"),
		"noFootballLeagues":League.objects.exclude(sport="Football"),
		"conferenceLeagues":League.objects.filter(name__contains="conference"),
		"atlanticLeagues":League.objects.filter(name__contains="atlantic"),
		"dallasTeams":Team.objects.filter(location="Dallas"),
		"raptorsTeams":Team.objects.filter(team_name__contains="raptors"),
		"cityTeams":Team.objects.filter(location__contains="city"),
		"tNameTeams":Team.objects.filter(team_name__istartswith="t"),
		"orderedTeams":Team.objects.all().order_by("location"),
		"inversedTeams":Team.objects.all().order_by("-team_name"),
		"cooperPlayers":Player.objects.filter(last_name="Cooper"),
		"joshuaPlayers":Player.objects.filter(first_name="Joshua"),
		"cooperButJoshPlayers":Player.objects.filter(last_name="Cooper").exclude(first_name="Joshua"),
		"wyattAlexPlayer":Player.objects.extra(where=["first_name='Alexander' OR first_name='Wyatt'"])
	}
	return render(request, "leagues/index.html", context)

def make_data(request):
	team_maker.gen_leagues(10)
	team_maker.gen_teams(50)
	team_maker.gen_players(200)

	return redirect("index")