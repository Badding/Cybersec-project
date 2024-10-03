from django.shortcuts import render, redirect
from .forms import NoteForm, CreateUserForm, LoginForm
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate, login, logout
from .models import Note, User
from django.db import connection

# Create your views here.

def loginView(request):
    #""" This is more secure way to handle user login. Build in Django authentication system
    form = LoginForm()

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            print(username, password)
            user = User.objects.get(username=username)
            print(user.check_password(password))

            user = authenticate(request, username=username, password=password)

            if user:
                auth.login(request, user)

                return redirect('notes')


    return render(request, 'pages/login.html', {'form': form})
    #"""

def logout_user(request):
    auth.logout(request)
    return redirect('login')

def registerView(request):
    #this is a vulnerable way to handle user registration
    """\
    form = CreateUserForm() #part of the Django authentication system

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if password == password2:
        """


    #""" This is more secure way to handle user registration. Build in Django authentication system
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        
        if form.is_valid():
            form.save()
            return redirect('login')

    return render(request, 'pages/register.html', {'form': form})
    #"""

def notesView(request):

    form = NoteForm()

    """
    fix for the SQL Injection
    also the notes.html template needs to be updated to display the notes correctly
    notes = Note.objects.filter(user=request.user)
    search_query = Note.objects.filter(content__contains=search_query, user=request.user)
    """
    search_query = request.GET.get('search', '')

    with connection.cursor() as cursor:
        query = f"SELECT id,content FROM notes_note WHERE user_id = {request.user.id}"
        cursor.execute(query)
        notes = cursor.fetchall()


    if search_query:
        with connection.cursor() as cursor:
            # for example if user searches for anything%' OR '1'='1' --
            # the result is all notes from any user

            query = f"SELECT id,content FROM notes_note WHERE content LIKE '%{search_query}%' AND user_id = {request.user.id}"
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

    """ adds a check to see if the user is the owner of the note
    if note.user == request.user:
        note.delete()
    """

    return redirect('notes')
