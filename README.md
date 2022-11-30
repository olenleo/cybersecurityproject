## Cybersecurity Base Course Project 

This web application allows users to overcome any social media anxiety by practising publishing tweets. These tweets should be completely private so no one will be able to read them!

This repository consists of the course project for the [Cyber Security Base](https://cybersecuritybase.mooc.fi/) course at the University of Helsinki.

# Instructions
The project can be started with the following command: 
```$ python manage.py runserver```
The application will run at localhost:8000/ 

The application contains two users:
```
user admin, password null 
user hacker, password malignant 
```
# Description
A Django application built using the tutorial at (link to first django app) provides quite the solid base for a secure web application. I chose five flaws from the OWASP top 10 2021 list. Several of these required me to put in some work and thought to expose some vulnerabilities!

1. [Insecure design](https://owasp.org/Top10/A04_2021-Insecure_Design/)

FLAW:
The ‘register new user’ (/messages/register/) form provides these following fields: 
	Create user: 
		- Username
		- Password
		- Security Question: What is your favourite Linux distribution?

This implementation is but a quick mockup of a create user form view. I did not implement the actual functionality for question- and answer-based identification. 

DESCRIPTION: 
The question and answer -method is not a valid or trustworthy method of identification. 

HOW TO FIX IT: 
This code should according to OWASP simply be removed in favour of a more robust password recovery method. On a further note, two-factor authentication should be used along a username/password to greatly improve security with regards to identification. This comes however with a trade-off in usability. Developers and the product owner should make an informed decision with regard to this. 

Flaw 2: [Identification and Authentication Failures](https://owasp.org/Top10/A07_2021-Identification_and_Authentication_Failures/) 

FLAW: 
Password creation does not check for common, short and numerical values. (https://github.com/olenleo/cybersecurityproject/blob/main/cybersecurityproject/settings.py#L85)

DESCRIPTION: 
Passwords should be unique, long and not too common. By identifying some usual password (such as ‘Password’ or ‘1234’) the attacker might obtain information about the password hashing patterns, opening up further avenues of attack. It is worth to note that this kind of password validation does not prevent the user from using the same password and username on multiple websites, which might lead to identity theft and open up possibilities to social engineering attacks. 

HOW TO FIX IT: 
Django offers a easy-to-implement solution for preventing the user from using such common values in settings.py: AUTH_PASSWORD_VALIDATORS. (https://github.com/olenleo/cybersecurityproject/blob/main/cybersecurityproject/settings.py#L85)

By removing the commented fields, and thus implementing the validators, the user passwords are checked against a minimum length of 9 characters, that they do not contain only numbers, the similarity of the username, email, first name and last name fields* against a factor of 0.1 – 1, where the ‘1’ setting only checks for identical values, that the password is not included amongst the 20 000 most common passwords and so forth. 

* the latter two fields are not in use in this application

3. [SQL Injection](https://owasp.org/Top10/A03_2021-Injection/)

FLAW: 
User-supplied data is not validated, filtered, or sanitized by the application. Direct access to the database allows the attacker to perform SQL queries, thus compromising secret information and allowing information removal. Flaw can be found [here](https://github.com/olenleo/cybersecurityproject/blob/main/insecureApp/views.py#L12) 

DESCRIPTION: 
In this case, submitting a message provides direct access to the database, circumventing the model layer entirely. This can be observed in the [post_injection_message() method:](https://github.com/olenleo/cybersecurityproject/blob/main/insecureApp/views.py#L12). Examples can be found in the method docstring.
To expose this vulnerability, I had to take the following steps: 
1) Bypass the model layer by creating a [raw SQL query function](https://docs.djangoproject.com/en/3.1/topics/db/sql/#executing-custom-sql-directly)
2) The SQL query function can not format the query string
3) Replace cursor.execute with cursor.executescript to allow for batched SQL queries – cursor.execute would not allow the second query in the above example, resulting in an error message.

HOW TO FIX: 
I would use the Django ORM layer to handle database access. In cases where direct database access is necessary [proper string formatting](https://github.com/olenleo/cybersecurityproject/blob/main/insecureApp/views.py#L42) should be used. 

4. [Broken Access Control](https://owasp.org/Top10/A01_2021-Broken_Access_Control/)

FLAW: 
The application uses unverified data in a SQL call that is accessing account information when the user attempts to [access messages](https://github.com/olenleo/cybersecurityproject/blob/main/insecureApp/views.py#L63)

DESCRIPTION:
An attacker can simply modifiy the browser's 'message_id' parameter to whatever message_id they want. As the message_id is not correctly verified, the attacker can read any user message. To try this out, log in as the user hacker with password malignant. The hacker can read some compromising information about the application admin by accessing the urls /messages/1 and /messages/2. 
HOW TO FIX: 
This security issue is easily fixed by asserting that the ‘user_id’ field with the session.user id are equal. This can be done by commenting following these [instructions](https://github.com/olenleo/cybersecurityproject/blob/main/insecureApp/views.py#L73). 

5. [Security Misconfiguration & Security Logging And Monitoring Failures](https://owasp.org/Top10/A09_2021-Security_Logging_and_Monitoring_Failures/)

FLAW: 
The application prints out excessive information the console and to [‘../log_file1.log’](https://github.com/olenleo/cybersecurityproject/blob/main/cybersecurityproject/settings.py#L133).

DESCRIPTION:
The log in question consists of messages at the ‘debug’ level; this exposes a wealth of information, inclucing information about the database queries. A end user does not generally need to access complete stack traces; and even if they were deemed to be of value for end users they should filter out anything that would compromise application security. Note that this file exists outside the application root folder; it might turn out to be suspectible to a Path Traversal attack (https://owasp.org/www-community/attacks/Path_Traversal) in further development. 

OWASP notes that security logging and monitoring failures are [difficult to test ](https://owasp.org/Top10/A09_2021-Security_Logging_and_Monitoring_Failures/). Logging and monitoring is, however, necessary for being able to detect intrusions. Access to log files should be granted only via proper authentication, log files should be formatted so that they can be useful later on and so forth. This is, however, outside the scope of this assignment. 

HOW TO FIX: 
Django logger settings can be managed in [settings.py](https://github.com/olenleo/cybersecurityproject/blob/main/cybersecurityproject/settings.py#L133). The current version is a very quick and crude implementation recording most events. The log file should be kept safe, with limited access and not only on a local machine. Logs should be formatted. Perhaps logging at ‘debug’ level only in a ‘test’, ‘staging’ or ‘local’ enviroment should be considered.