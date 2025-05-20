from datetime import timezone
from django.db import models

# Create your models here.
class User(models.Model):
    uuid=models.CharField(max_length=10,default='',null=True,blank=True)
    name=models.CharField(max_length=30)
    playedMinutes=models.CharField(max_length=30,default='0')
    phoneNumber=models.CharField(max_length=30)
    def __str__(self):
        return '{} - {}'.format(self.uuid,self.name)
    def getNameOnly(self):
        return self.name   
     
class System(models.Model):
    SYSTEM_TYPE_CHOICES = [
        ('PC', 'PC'),
        ('PS', 'PS'),
    ]
    systemName=models.CharField(max_length=50,default='')
    systemType=models.CharField(max_length=2,choices=SYSTEM_TYPE_CHOICES,default='PC')
    is_available=models.BooleanField(default=True)
    hourlyRate=models.CharField(max_length=20,default='',null=True,blank=True)

    # whom rent this?
    def __str__(self):
        return f"{self.systemType}"
    def save(self, *args, **kwargs):
        if self.systemType == 'PC':
            self.hourlyRate = 1000
        elif self.systemType == 'PS':
            self.hourlyRate = 2000
        super().save(*args, **kwargs)


class Team(models.Model):
    SYSTEM_TYPE_CHOICES = [
        ('PC', 'Personal Computer'),
        ('PS', 'PlayStation'),
    ]
    teamMembers=models.ManyToManyField(User, blank=True)
    teamCount=models.IntegerField(default=0)
    startTime=models.DateTimeField(auto_now_add=True,editable=True,null=True,blank=True)
    systemType=models.CharField(max_length=2,choices=SYSTEM_TYPE_CHOICES,default='PC')
    endTime=models.DateTimeField(null=True,blank=True)
    duration=models.DurationField(null=True,blank=True)
    checkout=models.CharField(max_length=50,default='',null=True,blank=True)
    checkedout=models.BooleanField(default=False)

    def __str__(self):
        return f"{self.id}"
    def save(self, *args, **kwargs):
        # Calculate duration when endTime is set
        if self.endTime and self.startTime:
            self.duration = self.endTime - self.startTime
            
        #     # Calculate checkout amount based on duration and system type
        #     hourly_rate = 1000 if self.systemType == 'PC' else 2000
        #     hours = self.duration.total_seconds() / 3600
        #     self.checkout = hours * hourly_rate
            self.teamCount=self.teamMembers.count()
        super().save(*args, **kwargs)
    def getDurationMin(self):
        durationMin=str(self.duration).split(':')
        return durationMin[1]
    # def create_member_sessions(self):
    #     for member in self.teamMembers.all():
    #         PlaySession.objects.get_or_create(
    #             user=member,
    #             team=self,
    #             # defaults={
    #             #     'start_time': self.startTime,
    #             #     'sesionDuration': self.duration
    #             # }
    #         ) 

# Systems-teams

class PlaySession(models.Model):
    SYSTEM_TYPE_CHOICES = [
        ('PC', 'Personal Computer'),
        ('PS', 'PlayStation'),
    ]
    user = models.ForeignKey(User, on_delete=models.SET_NULL,null=True, related_name='play_sessions')
    team=models.ForeignKey(Team,on_delete=models.SET_NULL,null=True,related_name='playsession')
    start_time = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    sesionDuration = models.PositiveIntegerField(null=True, blank=True)
    sessionType=models.CharField(max_length=2,choices=SYSTEM_TYPE_CHOICES,default='NOT ASIGEND')
    sessionAmount=models.CharField(max_length=50,default='',null=True,blank=True)
    def __str__(self):
        return f"{self.user.uuid}"