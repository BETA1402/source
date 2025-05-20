import math
from django.shortcuts import redirect, render,get_object_or_404
from django.utils import timezone
from django.http import JsonResponse
from manager.models import PlaySession, System, Team,User
from django.shortcuts import get_object_or_404
from django.contrib import messages
from .forms import TeamForm, UserForm,SystemForm,playSessionSearchForm
import pytz
from datetime import timedelta
from django.urls import reverse

# Create your views here.
def zero_view(request):
    # playSession=PlaySession.objects.all()
    play_sessions=None
    if 'uuid' in request.GET:
        print(request.GET)
        searchform=playSessionSearchForm(request.GET)
        # print(searchform)
        if searchform.is_valid():
            uuid=request.GET.get("uuid")
            print(uuid)
            user=User.objects.filter(uuid=uuid)
            print(user[0].uuid)
            play_sessions=PlaySession.objects.filter(user__uuid=user[0].uuid).order_by('-start_time')
            print(play_sessions)
        else:
            searchform=playSessionSearchForm()

    team = Team.objects.all()
    system=System.objects.all()
    users=User.objects.all()
    try:
        totalSystems=system.count()
        totalPc=system.filter(systemType='PC').count()
        totalPs=system.filter(systemType='PS').count()
        availablePc=system.filter(is_available=True,systemType='PC').count()
        availablePs=system.filter(is_available=True,systemType='PS').count()
    except:
        totalSystems=0
        totalPc=0
        totalPs=0
        availablePc=0
        availablePs=0
    # print(users)
    context={'totalSystems':totalSystems,'totalPc':totalPc,'totalPs':totalPs,'availablePc':availablePc,'availablePs':availablePs,'team':team}
    if request.method == 'POST':
       form = TeamForm(request.POST)
       secondForm=UserForm(request.POST)
       thirdform=playSessionSearchForm(request.POST)
       forthform=SystemForm(request.POST)
    else:
        form = TeamForm()
        secondForm=UserForm()
        thirdform=playSessionSearchForm()
        forthform=SystemForm()

    return render(request,'zero.html',{'users':users,'context':context,'form': form,'secondForm':secondForm,'thirdForm':thirdform,'play_sessions':play_sessions,'forthform':forthform}) 

def start_view(request, team_id):
    tehran_tz = pytz.timezone('Asia/Tehran')
    team = get_object_or_404(Team, id=team_id)
    startTime = timezone.now()  # Set the start time to the current time
    tehran_now = startTime.astimezone(tehran_tz)
    print(tehran_now)
    team.startTime=tehran_now
    team.save()
    return JsonResponse({'success': True, 'message': 'Timer started.','startTime':team.startTime})

def end_view(request, team_id):
    team = get_object_or_404(Team, id=team_id)

    tehran_tz = pytz.timezone('Asia/Tehran')
    endTime = timezone.now()  
    tehran_now = endTime.astimezone(tehran_tz)
    # team.endTime=tehran_now.strftime("%H:%M")
    team.endTime=tehran_now

    team.save()
    print(tehran_now)
    return JsonResponse({'success': True, 'message': 'Timer Ended.','endTime':tehran_now})

def checkoutTeam_view(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    print(team)
    teamCount=team.teamMembers.all().count()
    startTime = team.startTime  
    # startHour=startTime.strftime("%H")
    # startMin=startTime.strftime("%M")
    # print(startTime.minute)
    # print(str(startTime).split()[1])
    startHour=startTime.hour
    startMin=startTime.minute
    start_t = timedelta(hours=startHour, minutes=startMin)
    # print(startHour,'\n',startMin)
    stopTime = team.endTime
    endHour=stopTime.hour
    endMin=stopTime.minute
    end_t = timedelta(hours=endHour, minutes=endMin)
    # print(endHour,'\n',endMin)
    duration=((end_t-start_t).total_seconds())/60
    print(duration)
    #this pph must be dynamic and will come from hourlyPrice
    pph = System.objects.filter(systemType=team.systemType).first().hourlyRate
    # multipleControllerCount =0
    if(team.systemType=='PS'):
        initialMultipleControllerCount=int(team.teamCount)
        multipleControllerCount=teamCount-2
        if(duration!=0):
            if(initialMultipleControllerCount>=2):
                checkout=duration * (int(pph) +  300*multipleControllerCount)
            else:
                checkout=duration * int(pph)
        else:
            checkout=0
    elif(team.systemType=='PC'):
        checkout=duration*int(pph)*teamCount
    # print(duration,pph,teamCount,multipleControllerCount)
    # print(type cg)
    team.duration=duration
    team.checkout=checkout
    context={'success': True, 'message': 'Timer started.','duration':duration,'checkout':checkout}
    team.save()
    return JsonResponse(context)
    # return JsonResponse({'success': True, 'message': 'Timer started'})

def teamCreate_view(request):
    if request.method == 'POST':
        # print(request.POST)
        form = TeamForm(request.POST)   
        # team_members = form.cleaned_data['teamMembers']
        if form.is_valid():
            team_members=request.POST.get("teamMembers")
            # print(team_members)
            team_membersCount = form.cleaned_data['teamMembers'].count()
            team_systemsType = form.cleaned_data['systemType']
            # print(team_systemsType)
            validate=False
            available_systems=System.objects.filter(is_available=True,systemType=team_systemsType)
            if(available_systems.count()>=team_membersCount and team_systemsType=='PC'):
                counter=0
                for system in available_systems:
                    if(counter!=team_membersCount):
                        system.is_available = False
                        system.save()
                        counter+=1
                    else:
                        break
                validate=True
                messages.add_message(request,messages.SUCCESS,'your team just created!')
            elif(available_systems.count()!=0 and team_systemsType=='PS'):
                # print(available_systems[0].is_available)
                # available_systems[0].is_available = False
                # available_systems[0].save()
                validate=True
                counter=0
                team_membersCount
                for system in available_systems:
                    if(counter!=1):
                        system.is_available = False
                        system.save()
                        counter+=1
                    else:
                        break
            else:
                messages.add_message(request,messages.ERROR,'can not add this team with this quantity!')
                return redirect('/addSystem')

                #this gonna handle the alowed-counter for the systems (+ and -)
            print(validate)
            if(validate):
                # Team.objects.set(teamMembers=team_members)
                # form.save(teamMembers=team_members)
                form.save(commit=False) 
                print("sdadasda",team_membersCount)
                form.teamCount=team_membersCount
                form.save() 
            # if(system.count()<teamCount):
            #     context={'success': False, 'message': 'Not enough systems available'}
            #     return JsonResponse(context)
            # else:
            #     for i in range(teamCount):
            #         print(system[i])
            #         system[i].is_available=False
            #         print(system[i].is_available)
            #     system.save()   
            # return redirect('index/')  
    
                return redirect('/')                
        else:
            messages.add_message(request,messages.ERROR,'your team not created!')      
    else:
        form = TeamForm()
    return redirect(reverse("manager:main"))
    # return render(request,'zero.html', {'form': form})

def userCreate_View(request):
    
    print('user req',request)

    if request.method   == 'POST':
        # updated_request = request.POST.copy()
        # updated_request.update({'uuid': uuid})
        # print(updated_request)
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            try:
                # Get latest user safely
                last_user = User.objects.latest('id')
                next_id = last_user.id + 1
            except:
                # No users exist yet, start at 1
                next_id = 1
            # print(users.id)
            #need refactor
            if(len(str(next_id))==1):
                uuid='000{}'.format(next_id)

            elif(len(str(next_id))==2):
                uuid='00{}'.format(next_id)
            
            elif(len(str(next_id))==3):
                uuid='0{}'.format(next_id)    

            
            # Add UUID 
            user.uuid = uuid

            # Save to database
            user.save()

            messages.add_message(request,messages.SUCCESS,'your user just created!')
            return redirect('/')  
        else:
            messages.add_message(request,messages.ERROR,'your user not created!')
    else:
        form = UserForm()
        return redirect(reverse("manager:main"))

def payTeam_view(request,team_id=None):
    team_to_delete=Team.objects.get(id=team_id)
    team_to_delete_members=team_to_delete.teamMembers.all()
    play_quantity=team_to_delete.duration
    print(team_to_delete)
    # team_to_delete_members[0].playedMinutes+=team_to_delete.duration
    # team_to_delete_members.save()
    durationList=str(play_quantity).split(':')
    for tm in team_to_delete_members:
        PlaySession.objects.get_or_create(
            user=tm,
            team=team_to_delete,
            start_time= team_to_delete.startTime,
            sesionDuration=durationList[1],
            sessionType=team_to_delete.systemType,
            sessionAmount=team_to_delete.checkout
        )
        print(tm.playedMinutes,str(play_quantity).split(':'))
        if durationList[0]=='0':
            tm.playedMinutes=int(tm.playedMinutes)+int(durationList[1])
        else:
            tm.playedMinutes=int(tm.playedMinutes)+int(durationList[1])+int(durationList[0]*60)
        tm.save()     
    teamCount=team_to_delete.teamMembers.all().count()
    team_to_delete.checkedout=True
    # team_to_delete.delete()
    team_to_delete.save()

    if(team_to_delete.systemType=='PC'):
        availablePc=System.objects.filter(is_available=False,systemType='PC')
        counter=0
        for sys in availablePc:
            if counter<teamCount:
                sys.is_available=True
                sys.save()
                counter=counter+1
            else:
                break
    if(team_to_delete.systemType=='PS'):
        availablePS=System.objects.filter(is_available=False,systemType='PS')
        counter=0
        for sys in availablePS:
            if counter!=1:
                sys.is_available=True
                sys.save()
                counter=counter+1
            else:
                break
    return redirect(reverse("manager:main"))
    # return render(request,'zero.html')

def systemCreate_View(request):
    # print(request.POST)
    if request.method == 'POST':
        if 'PC_button' in request.POST:
            system_type = 'PC'
        # Check if the PS button was clicked
        elif 'PS_button' in request.POST:
            system_type = 'PS'
        print(request.POST)
        # Create a new system object and save it
        new_system = System(systemType=system_type,systemName=request.POST.get("systemName"))
        new_system.save()
    return redirect(reverse("manager:main"))

    # return render(request,'addSystem.html',{'form':form})

def remove_member_view(request,team_id,member_id):
  # Get the team and member
    team = get_object_or_404(Team, id=team_id)
    teamCount=team.teamMembers.all().count()
    member_to_remove = get_object_or_404(User, id=member_id)
    print(member_to_remove)
    # Verify member is actually in the team
    if not team.teamMembers.filter(id=member_id).exists():
        messages.error(request, "Member not found in this team")
        return redirect('manager:main')
    
    try:
        teamCount=team.teamMembers.all().count()
        print(teamCount)
        # Remove member from the team
        system_to_unreserve=[]
        if(team.systemType=="PC"):
            # Update system reservation status for this member
            system_to_unreserve = System.objects.filter(
                is_available=False,
                systemType=team.systemType  
            ).first()
        elif(team.systemType=="PS" and teamCount==1):
            system_to_unreserve = System.objects.filter(
                is_available=False,
                systemType=team.systemType  
            ).first()
        # print("sdsds",system_to_unreserve)
        if system_to_unreserve:
            system_to_unreserve.is_available = True
            # system_to_unreserve.team = None
            system_to_unreserve.save()
        
        # Optional: Create partial play session for this member
        if team.startTime and team.endTime:
            duration = team.endTime - team.startTime
            print(math.ceil(duration.total_seconds() /60))
            minutes_played = duration.total_seconds() / 60
            print(minutes_played)
            if(minutes_played>1):
                minutes_played = math.ceil(minutes_played)
            
            PlaySession.objects.get_or_create(
                user=member_to_remove,
                team=team,
                start_time= team.startTime,
                sesionDuration=minutes_played,
                sessionType=team.systemType,
                sessionAmount=int(float(team.checkout)/teamCount)
            )
        team.teamMembers.remove(member_to_remove)
        messages.success(request, f"{member_to_remove.id} removed from team")
    
    except Exception as e:
        messages.error(request, f"Error removing member: {str(e)}")
    # Construct the URL with query parameter
    redirect_url = f"{reverse('manager:main')}?uuid={member_to_remove.uuid}"
    
    return redirect(redirect_url) 