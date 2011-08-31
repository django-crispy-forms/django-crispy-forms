========
Concepts
========

Form Helpers
-------------

The biggest advantage of this library are :ref:`form helpers` and layouts. The advantage of these tools is that they let you build forms with most of the coding done in Python, rather than HTML. We **strongly** suggest you study and learn the examples in the :ref:`form helpers` documentation.

Don't Repeat Yourself
---------------------

It has been written that if you do anything twice in code, you should wrap it up
in a function or method. This project was born out of the desire to not have to
rewrite similar forms multiple times over the same project. Just like we use the
Django ORM to avoid writing simple queries again and again, it is advantageous to
our sanity and code quality to not have to write `<form></form>` 30 times across a project.

The problem with building a form this way multiple times is that it is ripe for error. What about hidden fields? What if you forget the `{% csrf_token %}` token?
What if you don't set the form method correctly?

Think of django-uni-form like an ORM, it handles the small details so you can
focus on the big picture of your project - the business logic that drives your
site and is probably a lot more fun to deal with than the tiny particularities of
forms.

Section 508
-----------

Some years ago the United States congress defined `Section 508`_ as a means to provide enforcement for technology provided or purchased for the government that met a set of specifications so that those with disabilities could use said technologies. Unfortunately, the specification does not normally apply to commercial products not used by the US Government and many US Government projects weasel out of the specification.

However, following Section 508 (and the World Wide Web Consortium's (W3C) `Web Accessibility Initiative`_ (WAI) is the right thing to do. It doesn't hurt to familiarize yourself with these specifications.

In the meantime, django-uni-form provides a means to easily render Section 508 compliant forms. How awesome is that?

.. _`Section 508`: http://en.wikipedia.org/wiki/Section_508
.. _`Web Accessibility Initiative`: http://en.wikipedia.org/wiki/Web_Accessibility_Initiative
