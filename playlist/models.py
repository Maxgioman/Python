from django.db import models

# Create your models here.
class User(models.Model):
	"""docstring for user"""
	username = models.CharField(max_length=30)
	firstname = models.CharField(max_length=30)
	lastname = models.CharField(max_length=30)
	email = models.EmailField()
	password = models.CharField(max_length=20)
	phone = models.CharField(max_length=13)

class Track(models.Model):
    name = models.CharField(max_length=30)
    file = models.FileField(upload_to='track/')

class Playlist(models.Model):
	"""docstring for playlist"""
	creatorId = models.ForeignKey(User, on_delete=models.CASCADE, related_name='playlists')
	public = models.BooleanField()
	tracks = models.ManyToManyField(Track)
	
	def __str__(self):
   		return 'Playlist ' + str(self.id) +' \t ' + str(self.public)
		
	
	class Meta:
		order_with_respect_to = 'creatorId'
		
		