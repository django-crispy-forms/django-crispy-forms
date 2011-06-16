========
Concepts
========

Don't Repeat Yourself
---------------------

It has been written that if you do anything twice in code, you should wrap it up
in a function or method. This project was born out of the desire to not have to
rewrite similar forms multiple times over the same project. Just like we use the
Django ORM to avoid writing simple queries again and again, it is advantageous to
our sanity and code quality to not have to write this many times::

    <form method="post" action="/blah" class="blah">
        {% csrf_token %}
        {% for field in form %}
            <div>{{ field }}</div>
        {% endfor %}
    </form>

The problem with building a form this way multiple times is that it is ripe for error. What about hidden fields? What if you forget the `{% csrf_token %}` token?
What if you don't set the form method correctly?

Think of django-uni-form like an ORM, it handles the small details so you can
focus on the big picture of your project - the business logic that drives your
site and is probably a lot more fun to deal with then the tiny particulars of
forms.

section 508
-----------

Blah blah blah

helpers
-----------

Blah blah blah

layouts
-----------

Blah blah blah