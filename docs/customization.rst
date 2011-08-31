=============
Customization
=============

Some ways to customize the behavior of django-uni-form.


Customizations on '*' required fields (optional)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you don't like the use of '*' (asterisk) to denote required fields you can simply overrride the django-uni-form field.html. In your Django project's templates directory create a new directory called `uni_form`. Copy the django-uni-form field.html file to that directory and make the desired changes. For example::

    cd ~/<my-projects>/<my-awesome-django-project>/templates/
    mkdir uni_form
    cd uni_form/
    cp <my-site-packages>/Django-uni-form/uni_form/templates/uni_form/field.html .
    
Now you could change the asterisk to any other character, an image icon, or whatever else you want.

Using Uni-Form strict fields
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

django-uni-form implements form fields in html differently than the standard Uni-Form. If you want to adhere to the strict definition of django-uni-form replace the field.html file with field.strict.html. You can just follow these instructions::

    cd ~/<my-projects>/<my-awesome-django-project>/templates/
    mkdir uni_form
    cd uni_form/
    cp <my-site-packages>/Django-uni-form/uni_form/templates/field.strict.html field.html
