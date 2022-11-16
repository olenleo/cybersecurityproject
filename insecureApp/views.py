from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, get_object_or_404, redirect
from .models import Message

def index(request):
    entry_list = Message.objects.filter(user_id_id=request.user)
    context = {'latest_question': entry_list}
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
    if request.POST == 'POST':  
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