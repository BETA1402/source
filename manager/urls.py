from django.contrib import admin
from django.urls import path
from .views import *
app_name='manager'
urlpatterns = [
    # this view include the main funtionality of the Web App
    path('', zero_view,name="main"),

    # this starts timer for specefic team 
    path('startTimer/<str:team_id>',start_view),
    
    # this ends timer  for a specefic team
    path('endTimer/<str:team_id>',end_view),
    
    # this calculate that a team with teamid <pk> how much gonna pay and how much plays 
    path('checkoutTeam/<str:team_id>',checkoutTeam_view),
    
    # this gonna let us to make a team payment done and delete them from database
    path('pay/<str:team_id>',payTeam_view,name="payTeam"),
    
    # this initial a team by giving team members and team play type(PC/PS)
    path('addTeam',teamCreate_view,name="addTeam"),
    
    # this view let ud initial a user
    path('addUser',userCreate_View,name="addUser"),

    path('addSystem/<str:systemType>',systemCreate_View,name="addSystem-SysType"),

    path('addSystem',systemCreate_View,name="addSystem"),

    path('remove-member/<int:team_id>/<int:member_id>/', remove_member_view, name='remove_member')]