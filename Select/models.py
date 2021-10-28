from django.db import models
import uuid

# Create your models here.
class ProblemStatement(models.Model):
	probNo = models.IntegerField()
	psname = models.CharField(max_length=100)
	description = models.CharField(max_length=5000)
	count = models.IntegerField(default=0)
	id = models.UUIDField(default=uuid.uuid4,  unique=True, primary_key=True, editable=False)

class Team(models.Model):
	teamNo=models.IntegerField()
	password = models.CharField(max_length=10)
	

class Taken(models.Model):
	tNo = models.ForeignKey(Team,on_delete=models.CASCADE,related_name='teamNum',default=1)
	psNo = models.ForeignKey(ProblemStatement,on_delete=models.PROTECT,related_name='problemstatementNum',default=1)
	