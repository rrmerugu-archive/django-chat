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

@login_required
def home(request):
    comments = Comments.objects.select_related().all().order_by('-id')[:10][::-1]
    return render(request, 'index.html', locals())

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