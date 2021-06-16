from django.shortcuts import render, redirect
from .models import League, Team, Player
from django.db.models import Q, Count
from . import team_maker

def index(request):
	atlantic=League.objects.get(name__icontains="Atlantic Soccer Conference") 
	atlanticTeams=atlantic.teams.all()

	penguins=Team.objects.get(team_name__icontains="penguin", location="Boston")
	pengPlayers=penguins.curr_players.all()	
	
	baseball=League.objects.get(name="International Collegiate Baseball Conference")#obtengo la liga	
	teams=baseball.teams.all()#lista de los teams de la liga	
	teamIds=[]   #lista que guardara los id de los teams de la liga de baseball
	for team in teams:
		teamIds.append(team.id)#agrego solo id de los teams a la lista teamids
	players=Player.objects.filter(curr_team__in=teamIds) #traigo los players de esos teams
	
	football=League.objects.get(name__icontains="Amateur football")#get league
	teamsFootball=football.teams.values_list("id")#get list with only id from football
	players2=Player.objects.filter(Q(curr_team__in=teamsFootball) & Q(last_name__icontains="lopez"))
	#players where curr_team este en teamsFootball Y last_name contenga lopez case insensitive	
	
	sportFootball=League.objects.filter(sport__icontains="Football").values_list("id")#get ids de los fb teams
	footballPlayers=Player.objects.filter(all_teams__in=sportFootball)#get players by teams ids

	sofiaPlayers=Player.objects.filter(first_name__icontains="sophia")#players named sophia
	sofiaTeams=Team.objects.filter(curr_players__in=sofiaPlayers)#teams con sophia en curr_players
	sofiaLeagues=League.objects.filter(teams__in=sofiaTeams)#leagues donde esta sofia
	
	washRoughriders=Team.objects.get(team_name__icontains="roughriders")
	flores=Player.objects.filter(last_name__icontains="flores").exclude(curr_team=washRoughriders.id)
	
	samuelEvans=Player.objects.get(first_name__icontains="samuel", last_name__icontains="evans")
	samuelTeams=Team.objects.filter(Q(curr_players=samuelEvans) | Q(all_players=samuelEvans)).distinct

	tigerCats=Team.objects.get(team_name__icontains="tiger")
	allTigerCatsPlayers=Player.objects.filter(Q(curr_team__exact=tigerCats.id) | Q(all_teams__exact=tigerCats.id)).distinct

	wichita=Team.objects.get(team_name__icontains="vikings")
	oldWichitaPlayers=Player.objects.filter(all_teams__exact=wichita.id).exclude(curr_team__exact=wichita.id)

	jacobGray=Player.objects.get(first_name__icontains="jacob", last_name__icontains="gray")
	jacobTeams=Team.objects.filter(all_players__exact=jacobGray).exclude(team_name__icontains="colts")

	league=League.objects.get(name="Atlantic Federation of Amateur Baseball Players")
	leagueTeams=league.teams.values_list("id")
	joshuaPlayers2=Player.objects.filter(Q(all_teams__in=leagueTeams) & Q(first_name__icontains="joshua"))

	bigTeams=Team.objects.annotate(num_players=Count("all_players")).filter(num_players__gte="12")#los teams con mas de 12 players

	allPlayersAndTeams=Player.objects.annotate(num_teams=Count("all_teams")).order_by("num_teams")

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
		"wyattAlexPlayer":Player.objects.extra(where=["first_name='Alexander' OR first_name='Wyatt'"]),
		"atlanticTeams":atlanticTeams,
		"pengPlayers":pengPlayers,
		"players":players,
		"players2":players2,
		"footballPlayers":footballPlayers,
		"sofiaTeams":sofiaTeams,
		"sofiaLeagues":sofiaLeagues,
		"flores":flores,
		"samuelTeams":samuelTeams,
		"allTigerCatsPlayers":allTigerCatsPlayers,
		"oldWichitaPlayers":oldWichitaPlayers,
		"jacobTeams":jacobTeams,
		"joshuaPlayers2":joshuaPlayers2,
		"bigTeams":bigTeams,
		"allPlayersAndTeams":allPlayersAndTeams
	}
	return render(request, "leagues/index.html", context)

def make_data(request):
	team_maker.gen_leagues(10)
	team_maker.gen_teams(50)
	team_maker.gen_players(200)

	return redirect("index")