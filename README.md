# Note Taking App for Cyber Security 2024 MOOC

## Introduction
This is a simple note-taking application built with Django. It allows users to create, read, update, and delete notes.
The app is project for Cyber Security 2024 MOOC

## Features
- User authentication
- Create, read, update, and delete notes
- Purposefully made security flaws for Syber security Course project
- fixes for the security flaws in separate files

## Requirements
- Python 3.x
- Django 5.1.1

## Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/Badding/Cybersec-project.git
    cd Cybersec-project/project
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
8. Or Access Django admin panel from `http://127.0.0.1:8000/admin`

## Usage
- Register or log in to start creating notes.
- Once logged in user can create, search and delete notes.
- Logout using logout button

### Flaw 1: A01:2021 Broken Access Control
**Source:** `views.py` line 84  
[Link to code](https://github.com/Badding/Cybersec-project/blob/28f42f018174bd97b4a877925aaad4eff68761be/project/notes/views.py#L84)

**Description:**  
Access control mechanisms are important to ensure that users can only perform actions within their intended permissions. In this application, broken access control allows unauthorized users to delete notes created by other users. This flaw is caused by users' ability to modify the URL parameter that references a note not owned by the current user. When the application queries the database for the note, it is deleted without first checking the ownership of the note, resulting in unauthorized action.

**Fix:**  
The vulnerability is fixed by updating the `deleteNote` function in `views.py` to include a verification of ownership step. The note will only be deleted if the current user matches the owner of the note. If the check fails, nothing happens, preventing unauthorized deletions.

`Fix found in views_fixed.py`

### Flaw 2: A03:2021 Injection
**Source:** `views.py` line 58  
[Link to code](https://github.com/Badding/Cybersec-project/blob/28f42f018174bd97b4a877925aaad4eff68761be/project/notes/views.py#L58)

**Description:**  
This common security vulnerability exposes the application to SQL injection attacks due to improper handling of user input in raw SQL queries. For instance, a commented-out search on line 54 allows unauthorized users to view all the notes in the database, regardless of ownership. This flaw was caused by using non-parameterized calls during dynamic search for notes in the database. This vulnerability further opens the application by letting attackers utilize SQL union statements to retrieve data from any table in the database, which is a significant risk to the integrity and confidentiality of the application.

**Fix:**  
The application is fixed by utilizing Django’s Object-Relational Mapping (ORM) system, which simplifies database interactions while enhancing security. The ORM automatically parameterizes queries and sanitizes user inputs, effectively preventing SQL injection attacks. On line 60 of `views.py`, there is a query made using ORM to query the database for `Note` objects. The `Note.objects.filter()` method is used to filter based on specific criteria; in this case, the note content must include the search parameter. The method returns a QuerySet containing all the objects that match the parameters. The `notes.html` file also needs to be modified as the QuerySet items are used differently.

`Fix found in views_fixed.py and notes_fixed.html`

### Flaw 3: A05:2021 Security Misconfiguration
**Source:** `settings.py` Line 27  
[Link to code](https://github.com/Badding/Cybersec-project/blob/28f42f018174bd97b4a877925aaad4eff68761be/project/project/settings.py#L27)

**Description:**  
In a Django application, the `DEBUG` setting in the `settings.py` file controls how errors and exceptions are displayed. By default, this setting is set to `True` when starting a new project, allowing developers to easily see stack traces and detailed exception information directly in the browser. While this is incredibly valuable when the application is in development, leaving `DEBUG` enabled in a production environment will expose overly detailed messages to users, potentially aiding attackers in finding vulnerabilities to exploit.

**Fix:**  
The solution for this issue is straightforward: always set `DEBUG` to `False` when the application is deployed to production. This change ensures that only generic error messages are shown to users when an error occurs, hiding unnecessary data from users. To maintain effective error monitoring without compromising security, developers should implement a logging system to collect error messages for debugging the application. The fix for flaw 5 was a logging system that also logs Django messages labeled warning and above.

### Flaw 4: A07:2021 Identification and Authentication Failures
**Source:** Missing feature

**Description:**  
Identification and Authentication failures pose a security risk in web applications, particularly when weak password policies and insufficient account lockout systems are implemented. Without limitation on failed login attempts, the website becomes vulnerable to brute force attacks, allowing malicious users to try gaining unauthorized access.

**Fix:** 
- [requirement.txt](project/requirement.txt) django-axes 7.0.0 added to the project
- [settings.py Line 98](project/project/settings.py#L98) drango-axes settings in `settings.py`

Django does not include built-in protection against these kinds of attacks. Therefore, to mitigate the security risks, Django Axes is integrated into this application. It is a third-party plugin that keeps track of login attempts and blocks brute-force attacks by locking the account after a specified number of unsuccessful attempts has been reached and disables the account temporarily. The plugin monitors suspicious login activities and logs relevant information to the Django administration panel, which is accessible to superusers. For this demonstration, it is configured to only track usernames and to ignore IP-address lockouts. The lockout time is set to only three minutes. Django Axes is quick and easy to set up and, when combined with a strong password policy, significantly reduces risks of identification and authentication failures, protecting user accounts from being compromised.

### Flaw 5: A09:2021 Security Logging and Monitoring Failures
**Source:** Missing feature

**Description:**  
Effective security logging and monitoring are crucial for detecting and responding to active breaches and for retaining alerts and forensic data for post-incident analysis. Without proper logging of important auditable events, such as user logins, failed login attempts, and warning messages, organizations may face big challenges in identifying vulnerabilities and responding to security incidents without having these systems in place.

**Fix:**
- [settings.py Line 104](project/project/settings.py#L104) line 104 added logging settings
- [signals.py](project/notes/signals.py) Added handelers and to retrieve the IP address of the logging attempt.

To address this security risk, a basic logging system was implemented in the application before integrating Django Axes, resulting in some overlap between these two systems. In the `settings.py` file, lines 104-137 contain the configuration of Django’s logging framework, specifying log formatting, and setting up an `audit.log` file in the project root directory to save the logging and Django event data. The `signals.py` file sets up the handlers for user login, logout, and failed login events. Additionally, a helper function, `get_client_ip`, is used for extracting the user’s IP address from the request object. This simple logging system demonstrates the basic capabilities of logging events in a web application. However, in an actual production environment, it is important to incorporate an active mechanism for alerting admins to suspicious activity for quick incident response time.
