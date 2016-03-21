from core.models import Comments, User

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseServerError
from django.views.decorators.csrf import csrf_exempt
from django.contrib.sessions.models import Session
from django.contrib.auth.decorators import login_required
import logging
logger = logging.getLogger(__name__)
import redis, json
from django.core import serializers
from .forms import RegistrationForm   
from django.shortcuts import render_to_response
from django.http import HttpResponse , HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.template import RequestContext

@login_required
def home(request):
    comments = Comments.objects.select_related().all().order_by('-id')[:10][::-1]
    user = request.user
    return render(request, 'index.html', locals())

def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/')

def register(request):
    
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')
    else:
        if request.method == 'POST':
            form = RegistrationForm(request.POST)
            if form.is_valid():
                user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'],
                first_name=form.cleaned_data['first_name']
                )
                user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
                logger.debug(user)
                login(request, user)
                return HttpResponseRedirect('/')
        else:
            form = RegistrationForm()
        variables = RequestContext(request, { 'form': form })

        return render_to_response( 'register.html', variables)    
    

 
def login_user(request):

    if request.GET:
        if request.user.is_authenticated():
            return HttpResponseRedirect('/')
        next = request.GET.get('next','/')
        return render_to_response('login.html', { 'next': next}, context_instance=RequestContext(request))



    if request.POST:
        next = request.POST.get('next','/')
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(next)

    return render_to_response('login.html', context_instance=RequestContext(request))
    

@csrf_exempt
def node_api(request):
    try:
        #Get User from sessionid
        session = Session.objects.get(session_key=request.POST.get('sessionid'))
        user_id = session.get_decoded().get('_auth_user_id')
        user = User.objects.get(user_id=user_id) 

        comment = Comments.objects.create(user=user, text=request.POST.get('comment'))
        message_data = json.loads(serializers.serialize("json", [comment,]) )[0]
   
 
        data = {}
        data['user'] = user.get_basic_info()
        data['message'] = message_data['fields']

        #Once comment has been created post it to the chat channel
        r = redis.StrictRedis(host='localhost', port=6379, db=0)
        r.publish('chat', data)
        #r.publish('chat', user.username + ': ' + request.POST.get('comment'))
        
        return HttpResponse("Everything worked :)")
    except Exception, e:
        logger.debug(e)
        return HttpResponseServerError(str(e))