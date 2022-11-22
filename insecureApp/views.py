import logging
logger = logging.getLogger(__name__)
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import HttpResponseRedirect, render, get_object_or_404, redirect
from .models import Message
from .forms import MessageForm

def index(request):
    user = request.user
    form = MessageForm(request.POST or None)
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = MessageForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            message = form.save(commit=False)
            message.user_id = request.user
            message.save()
            return HttpResponseRedirect('/', RequestContext(request))
        else:
            return HttpResponseRedirect('/')
    # if a GET (or any other method) we'll create a blank form
    else:
        form = MessageForm()
        entry_list = Message.objects.filter(user_id_id=request.user)
        context = {'latest_question': entry_list, 'form':form}
        return render(request, 'home.html', context)


# This method currently allows any user to see any message.
# Fix by: 
# Remove line 18, uncomment lines 20-23
@login_required
def get_message(request, message_id):
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
            messages.success(request, 'Account created successfully')  
  
    else:  
        form = UserCreationForm()  
        context = {  
            'form':form  
        }  
    return render(request, 'register.html', context)  

