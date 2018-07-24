from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse#, Http404
from django.views import generic
from django.views.generic import View
from django.views.generic.edit import CreateView, UpdateView
from .models import Album, Song
from .forms import UserForm
from django.db.models import Q

# Create your views here.
def index2(request):
    return render(request, 'music/albums.html', {'albums_list': Album.objects.all()})

def index(request):
    if not request.user.is_authenticated:
        return render(request, 'music/login.html')
    else:
        albums = Album.objects.filter(user=request.user)
        song_results = Song.objects.all()
        query = request.GET.get("q")
        if query:
            albums = albums.filter(
                Q(album_title__icontains=query) |
                Q(artist__icontains=query)
            ).distinct()
            song_results = song_results.filter(
                Q(song_title__icontains=query)
            ).distinct()
            return render(request, 'music/index.html', {
                'albums': albums,
                'songs': song_results,
            })
        else:
            return render(request, 'music/index.html', {'albums': albums})

def index1(request):
    #return HttpResponse('Hellow world')
    html_content = '<ul>'
    albums_list = Album.objects.all()
    for album in albums_list:
        html_content += '<li> <a href="album/' + str(album.id) + '"> ' + album.title + '</a> </li>'
    html_content += '</ul>'
    return HttpResponse(html_content)

def tell(request):
    return HttpResponse('I am in tell method : ' )

def albums(request):
    return render(request, 'music/albums.html', {'title' : 'Albums List'})

def details(request, album_id):
    #return HttpResponse('Details of Album ID: ' + str(album_id))
    '''try:
        album = Album.objects.get(id=album_id)
    except Album.DoesNotExist:
        raise Http404("Album does not exist")'''
    album = get_object_or_404(Album, pk=album_id)
    #songs = Song.objects.filter(album_id = album_id)
    songs = album.song_set.all()
    return render(request, 'music/album_details.html', {'album': album, 'songs' : songs})

class IndexView(generic.ListView):
    template_name = 'music/albums.html'
    context_object_name = 'albums_list'
    
    def get_queryset(self):
        return Album.objects.all()
    
class DetailView(generic.DeleteView):
    template_name = 'music/album_details.html'
    model = Album
    
class AlbumCreate(CreateView):
    model = Album
    fields = ['title','singer','logo']

class UserFormView(View):
    form_class = UserForm
    template_name = 'music/registration_form.html'
    
    def get(self,request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})
    
    def post(self,request):
        form = self.form_class(request.POST)
        
        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(form.cleaned_data['password'])
            user.save()
            
            #authenticate the user with registered credentials
            user = authenticate(username=username, password=password)
            
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('music:index')
                
        return render(request, self.template_name, {'form': form})
    
    
def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                albums = Album.objects.filter(user=request.user)
                return render(request, 'music/index.html', {'albums': albums})
            else:
                return render(request, 'music/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'music/login.html', {'error_message': 'Invalid login'})
    return render(request, 'music/login.html')

def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, 'music/login.html', context)