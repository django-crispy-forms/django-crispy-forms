# Create your views here.
from django.shortcuts import render_to_response
from django.template import RequestContext

def test_me(request):
    
    return render_to_response('test_app/test_template.html', {

    }, context_instance=RequestContext(request))    