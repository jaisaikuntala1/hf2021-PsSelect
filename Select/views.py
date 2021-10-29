from django.shortcuts import render,redirect
from django.http import JsonResponse
from .models import *
from .forms import PSForm, UpdatePSForm
from django.contrib import messages
import string    
import random

# Create your views here.
def login(request):
	if 'user' in request.session:
		return redirect('/home')
	return render(request,'login.html')

def logout(request):
	del request.session['user']
	messages.success(request, 'Logged out successfully!')
	return redirect('/')
	
def data(request):
	if 'user' not in request.session:
		return redirect('/home')
	teamNo=int(request.session['user'])
	if(teamNo!=88888):
		return redirect('/')
	probs=ProblemStatement.objects.all()
	ps=[]
	for prob in probs:
		n={}
		n['num']=prob.probNo
		n['name']=prob.psname
		n['desc']=prob.description
		n['count']=prob.count 
		ps.append(n)
	if request.method=="POST":
		return redirect('/')
	return JsonResponse(ps,safe=False)
		
def index(request):
	if 'user' not in request.session:
		return redirect('/')
	probs=ProblemStatement.objects.all().order_by('probNo')
	tno=Team.objects.get(teamNo=int(request.session['user']))
	taks=Taken.objects.filter(tNo=tno)
	if len(taks)>0:
		psnum=taks[0].psNo.probNo
		ownps=ProblemStatement.objects.get(probNo=psnum)
		own={}
		own['tno']=tno.teamNo
		own['num']=ownps.probNo
		own['name']=ownps.psname
		own['desc']=ownps.description
		return render(request,'default.html',{'own':own})
	
	context = {
		'probs':probs,
		'team_num' : tno.teamNo
	}
	print("team number", context['team_num'])
	return render(request,'index.html',context)
	
	
def validate(request):
	if request.method=='POST':
		username=request.POST['username']
		password=request.POST['password']
		try:
			passOrig=Team.objects.get(teamNo=username)
			if passOrig.password == password:
				request.session['user']=username
				return redirect('/home')
			else:
				messages.success(request, 'Team no. / Password is incorrect!  Try again..!')
				return redirect('/')
		except Exception:
			messages.success(request, 'Team no. / Password is incorrect!  Try again..!')
			return redirect('/')
	return redirect('/')
	
	
def save(request,pid):
	if 'user' not in request.session:
		return redirect('/')
	ps=ProblemStatement.objects.get(probNo=int(pid))
	if ps.count == 2:
		return redirect('/home')
	team=Team.objects.get(teamNo=int(request.session['user']))
	check=Taken.objects.filter(tNo=team)
	if len(check)>0:
		return redirect('/home')
	a=Taken(tNo=team,psNo=ps)
	a.save()
	p=ProblemStatement.objects.get(probNo=int(pid))
	p.count=p.count+1
	p.save()
	return redirect('/home')

def addPS(request):
	if 'user' not in request.session:
		return redirect('/')
	teamNo=int(request.session['user'])
	if(teamNo!=88888):
		return redirect('/')
	form = PSForm()
	if request.method == 'POST':
		form = PSForm(request.POST)
		num = -1
		if form.is_valid():
			num = form.cleaned_data['probNo']
		if num!=-1:
			PS = ProblemStatement.objects.filter(probNo=num)
			if len(PS)>0:
				messages.success(request, 'Problem Statement with already existing number cannot be created!')
				return redirect('home')
		form.save()
		messages.success(request, 'Problem Statement was added successfully!')
		return redirect('home')
	context = {'form': form,
				'action' : 'Add'
	}
	return render(request, 'psform.html', context)


def updatePS(request,pk):
	if 'user' not in request.session:
		return redirect('/')
	teamNo=int(request.session['user'])
	if(teamNo!=88888):
		return redirect('/')
	PS = ProblemStatement.objects.get(id=pk)
	form = UpdatePSForm(instance=PS)
	if request.method == 'POST':
		form = UpdatePSForm(request.POST, instance=PS)
		form.save()
		messages.success(request, 'Problem Statement was updated successfully!')
		return redirect('home')
	context = {'form': form,
				'action' : 'Update'
	}
	return render(request, 'psform.html', context)

def deletePS(request,pk):
	if 'user' not in request.session:
		return redirect('/')
	teamNo=int(request.session['user'])
	if(teamNo!=88888):
		return redirect('/')
	psno = ProblemStatement.objects.get(id=pk)
	taks=Taken.objects.filter(psNo = psno)
	if(len(taks)>0):
		msg = 'PS '+str(psno.probNo)+' cannot be deleted since one/more teams have already opted it!'+'\n'+'Hint:You can Reset!'
		messages.success(request, msg)		
	else:
		PS = ProblemStatement.objects.filter(id=pk).delete()
		messages.success(request, 'Problem Statement was deleted successfully!')
	return redirect('home')


def reset(request):
	if 'user' not in request.session:
		return redirect('/')
	teamNo=int(request.session['user'])
	if(teamNo!=88888):
		return redirect('/')
	ProblemStatement.objects.all().update(count=0)
	Taken.objects.all().delete()
	Team.objects.exclude(teamNo=88888).delete()
	for i in range(1,61):
		ran = ''.join(random.choices(string.ascii_letters + string.digits, k = 10))
		team=Team(teamNo=i,password=str(ran))
		team.save()
	messages.success(request, 'Reset was successful! Team credentials are now changed and PS counts are again set to 0!')
	return redirect('home')

def team_credentials(request):
	if 'user' not in request.session:
		return redirect('/')
	teamNo=int(request.session['user'])
	if(teamNo!=88888):
		return redirect('/')
	teams = Team.objects.exclude(teamNo=88888).order_by('teamNo')
	context = {
		'teams' : teams
	}
	return render(request, 'team_credentials.html', context)


def results(request):
	if 'user' not in request.session:
		return redirect('/')
	teamNo=int(request.session['user'])
	if(teamNo!=88888):
		return redirect('/')
	teams = Taken.objects.all().order_by('tNo')
	context = {
		'teams': teams
	}
	return render(request, 'results.html', context)


