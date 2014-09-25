from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib import messages
def create_palylist(request,songs):
    # creat playlist here.
    #request.user.message_set.create(message="Your playlist was added successfully.")
    messages.add_message(request, messages.INFO, 'Your playlist was added successfully') 
    return render_to_response("user_message.html", \
                              {"songs":songs}, \
                              context_instance=RequestContext(request))
    
