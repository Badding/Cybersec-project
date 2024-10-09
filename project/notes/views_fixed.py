from django.shortcuts import render, redirect
from .forms import NoteForm, CreateUserForm, LoginForm
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate, login, logout
from .models import Note, User

# Create your views here.

def loginView(request):
    form = LoginForm()

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user:
                auth.login(request, user)

                return redirect('notes')

    return render(request, 'pages/login.html', {'form': form})

def logout_user(request):
    auth.logout(request)
    return redirect('login')

def registerView(request):

    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        
        if form.is_valid():
            form.save()
            return redirect('login')

    return render(request, 'pages/register.html', {'form': form})

def notesView(request):
    form = NoteForm()
    search_query = request.GET.get('search', '')
    search_query = Note.objects.filter(content__contains=search_query, user=request.user)

    if search_query:
        notes = search_query
    else:
        notes = Note.objects.filter(user=request.user)

    if request.method == 'POST':
        form = NoteForm(request.POST)
        
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.save()

            return redirect('notes')

    return render(request, 'pages/notes.html', {'form': form, 'notes': notes})

def deleteNote(request, note_id):
    note = Note.objects.get(id=note_id)

    if note.user == request.user:
        note.delete()

    return redirect('notes')
