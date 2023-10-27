import uuid
from django.db import models
from django.conf import settings
from accounts.models import Account

class Category(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	name = models.CharField(max_length=64,null=False,blank=False,unique=True)

	def __str__(self):
		return '#' + self.name


class Activity(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	title = models.CharField(max_length=255,blank=False,null=False)
	photo = models.ImageField(upload_to=settings.ACCOUNTS_PHOTOS_DIR, null=True, blank=True)
	is_free = models.BooleanField(default=True,blank=False,null=False)
	price = models.FloatField(blank=True,null=True)
	posted_by = models.ForeignKey(Account, null=True, blank=True,on_delete=models.SET_NULL)
	description = models.TextField(blank=True,null=True)
	location =models.CharField(max_length=255,null=False,blank=True,default='online')
	max_participants = models.IntegerField(null=True,blank=True)
	date = models.DateField(null=False,blank=False)

	categories = models.ManyToManyField(Category, blank=True, related_name='activities', through='ActivityCategory')
	likes = models.ManyToManyField(Account, blank=True,  related_name='liked_activites', through='ActivityLike')
	accounts_registrations = models.ManyToManyField(Account, blank=True,related_name='activities_registrations', through='ActivityRegistration')
	
	created_at = models.DateTimeField(auto_now_add=True, editable=False)
	updated_at = models.DateTimeField(auto_now=True)    


	def __str__(self):
		return self.title


class ActivityCategory(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
	category = models.ForeignKey(Category, on_delete=models.CASCADE)

	class Meta:
		unique_together = ('activity', 'category')

	def __str__(self):
		return str(self.activity.id) + " : " + str(self.category)



class ActivityLike(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	liked_by = models.ForeignKey(Account, on_delete=models.CASCADE)
	liked_activity = models.ForeignKey(Activity, on_delete=models.CASCADE)

	class Meta:
		unique_together = ('liked_by', 'liked_activity')
	
	def __str__(self):
		return str(self.liked_by) + ' liked ' + str(self.liked_activity)


class ActivityRegistration(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	account = models.ForeignKey(Account, on_delete=models.CASCADE,blank=False,null=False)
	activity = models.ForeignKey(Activity, on_delete=models.CASCADE,blank=False, null=False,)
	is_accepted = models.BooleanField(default=False,null=False,blank=True)
	is_payed = models.BooleanField(default=False,null=False,blank=True)
	
	created_at = models.DateTimeField(auto_now_add=True, editable=False)
	updated_at = models.DateTimeField(auto_now=True)  


	class Meta:
		unique_together = ('account', 'activity')

	def __str__(self):
		return str(self.account) + ' registred to ' + str(self.activity)
