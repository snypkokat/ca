from django.shortcuts import render
from django.http import HttpResponseRedirect, FileResponse
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from .models import Posts
import xml.etree.ElementTree as ET

# ГЛАВНАЯ
def index(request):
    return render(request, 'home.html', {'user': request.user})

# ПРОФИЛЬ
def profile(request):
    return render(request, 'profile.html')

# POSTS
def posts(request):
    print('user: ', request.user)
    posts = Posts.objects.all()
    return render(request, 'posts.html', {'posts': posts})

# NEWPOST
def newpost(request):
    title = request.POST.get('title')
    text = request.POST.get('text')
    file = request.FILES['file']
    fss = FileSystemStorage('appshop/static/images/')
    saved_file = fss.save(file.name, file)
    
    post = Posts()
    post.title = title
    post.text = text
    post.image = file.name
    post.save()
    return HttpResponseRedirect('/posts')

# POST INFO
def post(request, id):
    post = Posts.objects.get(id=id)
    return render(request, 'post.html', {'post': post})

# EDIT POST
def editpost(request, id):
    post = Posts.objects.get(id=id)
    return render(request, 'editpost.html', {'post': post})

# SAVE EDIT POST
def saveeditpost(request, id):
    post = Posts.objects.get(id=id)
    title = request.POST.get('title')
    text = request.POST.get('text')
    if 'file' in request.FILES:
        file = request.FILES['file']
        fss = FileSystemStorage('appshop/static/images/')
        saved_file = fss.save(file.name, file)
        post.image = file.name
    
    
    post.title = title
    post.text = text
    
    
    post.save()

    return HttpResponseRedirect('/posts')

# DELETE POST
def deletepost(request, id):
    post = Posts.objects.get(id=id)
    post.delete()
    return HttpResponseRedirect('/posts')

#EXPORT
def export(request):
    posts = Posts.objects.all()
    data = ET.Element('data')
    for post in posts:
        element = ET.SubElement(data, 'post')
        element.set('title', post.title)
    
    ET.ElementTree(data).write("posts.xml", encoding='UTF-8')

    return HttpResponseRedirect('/posts')


def download(request):
    f = open('posts.xml', 'rb')
    return FileResponse(f, as_attachment=True)

def registration(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = User.objects.create_user(name, email, password)
        user.save()
        return HttpResponseRedirect('/')
    else:
        return render(request, 'registration.html')

def login_user(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        password = request.POST.get('password')

        user = authenticate(username=name, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/') 
        else:
            print('error')
            return HttpResponseRedirect('/login')

        
    else:
        return render(request, 'login.html')


def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/') 
