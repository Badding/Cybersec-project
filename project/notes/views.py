from django.shortcuts import render, redirect
from .forms import NoteForm, CreateUserForm, LoginForm
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate, login, logout
from .models import Note, User
from django.db import connection

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
    
    if search_query:    
        with connection.cursor() as cursor:
            """
            UNSAFE SQL query,
            for example if user searches for "anything%' OR '1'='1' --"
            the result is all notes from the database
            """

            query = f"SELECT id,content FROM notes_note WHERE content LIKE '%{search_query}%' AND user_id = {request.user.id}"
            cursor.execute(query)
            notes = cursor.fetchall()
                
    else:
        with connection.cursor() as cursor:
            query = f"SELECT id,content FROM notes_note WHERE user_id = {request.user.id}"
            cursor.execute(query)
            notes = cursor.fetchall()

    if request.method == 'POST':
        form = NoteForm(request.POST)
        
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.save()

            return redirect('notes')

    return render(request, 'pages/notes.html', {'form': form, 'notes': notes})

def deleteNote(request, note_id):
    
    # there is a Broken Access Control flaw here, if the user is not the owner of the note, he can still delete it
    note = Note.objects.get(id=note_id)
    note.delete()

    return redirect('notes')

