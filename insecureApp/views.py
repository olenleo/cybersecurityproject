import logging
logger = logging.getLogger(__name__)
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import HttpResponseRedirect, render, get_object_or_404, redirect
from .models import Message
from .forms import MessageForm
from django.db import connection


def post_message(request):
    """
        This method allows for SQL injections by batched SQL queries. For example if the 'message' parameter is as follows:
            "injection attack", datetime('now'), 1); DROP TABLE insecureApp_message;'
        the entire message database will be removed.

        Solution:
            - Proper string formatting goes a long way! For example replace the sql variable with
            sql = "INSERT INTO insecureApp_message (message_text, pub_date, user_id_id)
                VALUES ("{0}", datetime('now'),{1});".format(message, request.user.id)

        The current method bypasses the models entirely: the method on line #30 onwards uses models and string formatting, providing a safe way to interact with the database.
    """

    with connection.cursor() as cursor:
        message = request.POST.get('message','')
        user_id = request.user.id
        sql = "INSERT INTO insecureApp_message (message_text, pub_date, user_id_id) VALUES (" + message + ", datetime('now'), "+ str(user_id) + "});"
        
        cursor.executescript(sql)   #   Dangerous; executescript allows for batched SQL queries
        # cursor.execute(sql)       #   A more safe solution, allowing for only one query to exist
    return HttpResponseRedirect('/')

def index(request):
    """
        Rows 13-20 provide a safe way of submitting an item to the database
        By using a 'model' object any SQL queries will be formatted to stop any injection attacks.
    """
    if request.method == 'POST':
        form = MessageForm(request.POST)
        logger.warning(form)
        if form.is_valid():
            message = form.save(commit=False)
            message.user_id = request.user
            message.save()
            return HttpResponseRedirect('/', RequestContext(request))
        else:
            return HttpResponseRedirect('/')
    else:
        form = MessageForm()
        entry_list = Message.objects.filter(user_id_id=request.user)
        context = {'latest_question': entry_list, 'form':form}
        return render(request, 'home.html', context)



@login_required
def get_message(request, message_id):
    """
        This method currently allows any user to see any message.
        Fix:
        Remove line 67, uncomment lines 69-72
    """
    message = get_object_or_404(Message, pk=message_id)
    return render(request, 'insecureApp/detail.html', {'message' : message }) # Remove this
    
    #if(message.user_id == request.user):
    #    return render(request, 'insecureApp/detail.html', {'message' : message })
    #else:
    #   return redirect('/')

def register(request):  
    if request.method == 'POST':  
        form = UserCreationForm()  
        if form.is_valid():  
            form.save()  
  
    else:  
        form = UserCreationForm()  
        context = {  
            'form':form  
        }  
    return render(request, 'register.html', context)  

