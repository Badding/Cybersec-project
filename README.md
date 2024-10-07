# Django Note Taking App for Cyber Security 2024 MOOC

## Introduction
This is a simple note-taking application built with Django. It allows users to create, read, update, and delete notes.
The app is project for Cyber Security 2024 MOOC

## Features
- User authentication
- Create, read, update, and delete notes
- Purposefully made security flaws for Syber security Course project

## Requirements
- Python 3.x
- Django 5.1.1

## Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/Badding/Cybersec-project.git
    cd django-note-app
    ```

2. Create a virtual environment and activate it:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Apply migrations:
    ```bash
    python manage.py migrate
    ```

5. Create a superuser:
    ```bash
    python manage.py createsuperuser
    ```

6. Run the development server:
    ```bash
    python manage.py runserver
    ```

7. Open your browser and go to `http://127.0.0.1:8000`.

## Usage
- Register or log in to start creating notes.
- Once logged in user can create, search and delete notes.
- Logout using logout button
