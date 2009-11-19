# Create your views here.
from django.shortcuts import render_to_response
from django.template import RequestContext

from uni_form.helpers import FormHelper, Submit, Reset, Hidden

from test_app.forms import TestForm, HelperTestForm, LayoutTestForm

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
    