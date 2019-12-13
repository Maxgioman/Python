from django.shortcuts import render

# Create your views here.
from django.core.files import File
from django.template import loader
from django.http import HttpResponse
from django.http import Http404, HttpResponseForbidden, HttpResponseBadRequest
from .models import User, Track, Playlist
import re

# Registration index/
def index(request):
    if request.method == 'GET':
        return render(request, 'registr.html')
        
    if request.method == 'POST':
        return render(request, 'registr.html')
        #raise Http404('What are you posting into the index page?!')
    return HttpResponse(str(request.method))
# User Data Rigistration
def registration(request):
    if request.method == 'POST':
        def validate_params(data, validators):
            for validator in validators:
                data[validator['name']]

        validate_params(request.POST, [{"name": "username", "requeired": True}])

        username = request.POST.get('username', False)
        firstname = request.POST.get('firstname', False)
        lastname = request.POST.get('lastname', False)
        email = request.POST.get('email', False)
        password = request.POST.get('password', False)
        phone = request.POST.get('phone', False)

        if re.search('[a-zA-Z]', phone):
            raise HttpResponseForbidden('phone has letters')
        if not (username and firstname and lastname and email and password and phone):
            return HttpResponseForbidden('user ' + str(username) + ' firstname '+str(firstname) +' lastname '+str(lastname)+' email ' +str(email)+' password ' +str(password)+' phone ' +str(phone))
        
        User.objects.create(username=username, firstname=firstname, lastname=lastname, email=email, password=password, phone=phone)
        
        return HttpResponse('All done')
    return HttpResponse('registration here')
#  LogIn login/
def login(request):
    if request.method == 'GET':
        username = request.GET.get('username', False)
        password = request.GET.get('password', False)
        
        if not (username and password):
            return HttpResponseForbidden('403 not propriet Data')
        logined = User.objects.get(username=username, password=password)
        if not logined:
            raise Http404('User not found')
        
    return HttpResponse('You logined as <b> ' +str(logined.email))

# LogOut should be here logout/
def logout(request):
    if request.method == 'GET':
        pass
    return HttpResponse('logout here')

# Elements of playlist

# adding new Track
def addTrack(request):
    if request.method == 'POST':
        trackName = request.POST.get('name', False)
        trackFile = request.FILES

        if not (trackName and trackFile):
            return HttpResponseBadRequest('You may inputed wrong data...'+' ='+str(trackFile))
        
        Track.objects.create(name=trackName, file=File(trackFile['file']))
        return HttpResponse('Track was added ')
    # page
    elif request.method == 'GET':
        return render(request, 'add_track.html')
    else:    
        return Http404('No such site')                    

def userlist(request):
    userId = request.GET.get('userId', False)
    playlistId = request.GET.get('playlistId', False)
    # display all trecks related to a playlist
    if not userId:
        raise Http404("No such user")

    if request.method == 'GET':
        try:
            user = User.objects.get(id=userId)
            tracks_list = user.playlists.all()
        except Playlist.DoesNotExist:
            raise Http404('There is no such playlist')
        
        somePretty = '<ul>'
        if not playlistId:
            for i in tracks_list:
                somePretty += '<li><a> ' + str(i) + ' id= '+ str(i.id) + '</a></li> '
                somePretty += '<ul>'
                for t in i.tracks.all():
                    somePretty += '<li><a> ' + str(t) + ' id= '+ str(t.id) + '</a></li> '
                somePretty += '</ul>'
            somePretty += '</ul>'
        else:
            tracks_list = tracks_list.get(id=playlistId)
            for i in tracks_list.tracks.all():
                somePretty += '<li><a> ' + str(i) + ' id= '+ str(i.id) + '</a></li> '
            somePretty += '</ul>'
        return HttpResponse(somePretty)
    
    #if request.method == 'POST':
    #    pass WAS RENAMED TO addTrack

    if request.method == 'DELETE':
        deleteObjectId = request.GET.get('trackId', False)
        if deleteObjectId:
            deletedObj = Playlist.objects.select_related('creatorId').get(id=userId).tracks.get(id=deleteObjectId)
        else:
            return HttpResponse('No such track here')
        if deletedObj:
            Playlist.objects.select_related('creatorId').get(id=userId).tracks.remove(deletedObj)
        return HttpResponse('track <b>' + str(deletedObj) + '</b> was deleted')
    return HttpResponse('userlist here')

# playlists

def addPlaylist(request):
    if request.method == 'GET':
        return render(request, 'add_playlist.html')
    

    if request.method == 'POST':
        userId = request.POST.get('creatorId', False)
        public = True if request.POST.get('public', False) == 'on' else False
        tracks = File(request.FILES['file'])
        tracksName = request.POST.get('tracksName', False)

        if not (userId and tracks and tracksName):
            return HttpResponseBadRequest('<h2><b>Bad data!</b></h2>'+str(userId))
        
        newTrack = Track.objects.create(name=tracksName, file=tracks)

        if not newTrack:
            return HttpResponseBadRequest('<h2>Cannot create track</h2>')

        newPl = Playlist.objects.create(creatorId=User.objects.get(id=userId), public=public)
        newPl.tracks.add(newTrack)
        
        return HttpResponse('<b>' + str(newPl) + '</b> was created.')

    return Http404()

def userlists(request):
    
    userId = request.GET.get('userId', False)
    # display all related playlists
    if not (userId):
        raise Http404('No playlists in such user')

    if request.method == 'GET':
        allUserPlaylists = Playlist.objects.all().filter(creatorId=userId)
        somePretty = '<h1>' + str(User.objects.get(id=userId).username) + "'s playlists:</h1><ul>"
        for i in allUserPlaylists:
            somePretty += '<li><a> ' + str(i) + '</a></li> '
        somePretty += '</ul>'
        return HttpResponse(somePretty)
        


    #if request.method == 'PUT':
     #   Замість пут mod_put

    if request.method == 'DELETE':
        deleteObjectId = request.GET.get('playlistId', False)
        if deleteObjectId:
            try:
                deletedObj = Playlist.objects.get(id=deleteObjectId)
            except Playlist.DoesNotExist:
                raise Http404('There is no such playlist')
            
        else:
            return HttpResponse('No such playlist here')
        if deletedObj:
            deletedObj.delete()
            return HttpResponse('track <b>' + str(deletedObj) + '</b> id' + deleteObjectId +' was deleted')
    return HttpResponse('Wrong id.')
#------------------------------------------------
def mod_put(request):
    if request.method == 'GET':
        return render(request, 'mod_pl_put.html')
#------------------------------------------------
    if request.method == 'POST':
        playlistId = request.POST.get('playlistId', False)
        tracksId = request.POST.get('tracksId', False)
        if not (playlistId and tracksId):
            return HttpResponse('405 bad data ')

        playlist = Playlist.objects.get(id=playlistId)
        track = Track.objects.get(id=tracksId)
    
        if not (playlist and track):
            return HttpResponse('405 bad data ')

        newone = playlist.tracks.remove(track)
        
        return HttpResponse('Was unbind to'+ str(Playlist.objects.get(id=playlistId)))
#------------------------------------------------
def modify_pl(request):

    if request.method == 'POST':
        userId = request.POST.get('userId', False)
        playlistId = request.POST.get('playlistId', False)
        tracksId = request.POST.get('tracksId', False)
        if not (playlistId and tracksId):
            return HttpResponse('405 bad data ')

        playlist = Playlist.objects.get(id=playlistId)
        public = playlist.public
        creatorId = playlist.creatorId.id
        
        track = Track.objects.get(id=tracksId)
    # Hsow HERE
        if not (playlist and track and userId):
            return HttpResponseBadRequest('Wrong')
        
        if userId != creatorId and not public:
            return HttpResponseForbidden('It is mine')

        newone = playlist.tracks.add(track)
        return HttpResponse('Was bind to'+ str(newone))
#------------------------------------------------
    if request.method == 'GET':
        return render(request, 'mod_pl.html')
    return HttpResponse('Wrong http request')