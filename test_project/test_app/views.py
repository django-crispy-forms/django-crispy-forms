# Create your views here.
from django.shortcuts import render_to_response
from django.template import RequestContext

from uni_form.helpers import FormHelper, Submit, Reset, Hidden

from test_app.forms import TestForm, HelperTestForm, LayoutTestForm, MessageResponseForm

def basic_test(request):
    if request.method == "POST":
        form = TestForm(request.POST)
    else:
        form = TestForm()
    
    return render_to_response('test_app/test_template.html', {
        'form': form
    }, context_instance=RequestContext(request))    
    
def view_helper(request):
    # Create the form
    if request.method == "POST":
        form = TestForm(request.POST)
    else:
        form = TestForm()

    # create a formHelper
    helper = FormHelper()

    # Add in a class and id
    helper.form_id = 'this-form-rocks'
    helper.form_class = 'search'

    # add in a submit and reset button
    submit = Submit('search','search this site')
    helper.add_input(submit)
    reset = Reset('reset','reset button')
    helper.add_input(reset)
    hidden = Hidden('not-seen','hidden value stored here')
    helper.add_input(hidden)


    # create the response dictionary
    response_dictionary = {'form':form, 'helper': helper}
    
    return render_to_response('test_app/view_helper.html', 
        response_dictionary, 
        context_instance=RequestContext(request))   
        
def view_helper_set_action(request):

    # Create the form
    form = TestForm()

    # create a formHelper
    helper = FormHelper()

    # add in a submit and reset button
    submit = Submit('send-away','Send to other page')
    helper.add_input(submit)
    
    helper.form_action = 'view_helper'
    helper.form_method = 'GET'    

    # create the response dictionary
    response_dictionary = {'form':form, 'helper': helper}
    
    return render_to_response('test_app/view_helper.html', 
        response_dictionary, 
        context_instance=RequestContext(request))   
    
def form_helper(request):
    if request.method == "POST":
        form = HelperTestForm(request.POST)
    else:
        form = HelperTestForm()
    
    return render_to_response('test_app/form_helper.html', {
        'form': form
    }, context_instance=RequestContext(request))
    
def layout_test(request):
    if request.method == "POST":
        form = LayoutTestForm(request.POST)
    else:
        form = LayoutTestForm()
        
    return render_to_response('test_app/form_helper.html', {
        'form': form
    }, context_instance=RequestContext(request))
    
def lacking_form_tag(request):
    # Create the form
    if request.method == "POST":
        form = TestForm(request.POST)
    else:
        form = TestForm()

    # create a formHelper
    helper = FormHelper()

    # remove the form tag
    helper.form_tag = False

    # create the response dictionary
    response_dictionary = {'form':form, 'helper': helper, 'title':'Lacking Form Tag Test'}
    
    return render_to_response('test_app/generic_form_test.html', 
        response_dictionary, 
        context_instance=RequestContext(request))   
    
def message_response(request):
    
    if request.method == "POST":
        form = MessageResponseForm(request.POST)
    else:
        form = MessageResponseForm()
    
    # create a formHelper
    helper = FormHelper()
    
    # add in a error and success button
    error = Submit('generate-result','Generate Error')
    helper.add_input(error)
        
    # add in a submit and reset button
    success = Submit('generate-result','Generate Success')
    helper.add_input(success)    
    
    # create the response dictionary
    response_dictionary = {'form':form, 'helper': helper, 'title':'Message response test'}
    
    return render_to_response('test_app/generic_form_test.html', 
        response_dictionary, 
        context_instance=RequestContext(request))
        
def csrf_token_test(request):
    
    # Create the form
    if request.method == "POST":
        form = TestForm(request.POST)
    else:
        form = TestForm()
        
    helper = FormHelper()                
    helper.use_csrf_protection = True

    # create the response dictionary
    response_dictionary = {'form':form, 'helper': helper, 'title':'CSRF token test'}
    
    return render_to_response('test_app/generic_form_test.html', 
        response_dictionary, 
        context_instance=RequestContext(request))    