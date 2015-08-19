.. _faq:

==========================
Frequently Asked Questions
==========================

.. contents::
    :local:

.. _faq-technical:


Technical
=========

.. _faq-columns:

Displaying columns in a bootstrap Layout
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Of course you can display form fields within columns, the same way you would do it in a standard bootstrap form, you can do it in a bootstrap layout, see an `example`_.

.. _`example`: http://stackoverflow.com/questions/12144475/displaying-multiple-rows-and-columns-in-django-crispy-forms


.. _faq-general:

General
=======

.. _faq-why-use-it:

Why use django-crispy-forms and not other app
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Well, I'm obviously biased for answering this question. But I once `answered it at StackOverflow`_.

.. _`answered it at StackOverflow`: http://stackoverflow.com/questions/11749860/how-to-render-django-forms-choicefield-as-twitter-bootstrap-dropdown

.. _faq-when-started:

How did this all get started?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In December 2008, while `Daniel Greenfeld`_ was working for `NASA's Science Mission Directorate`_, his team began to use Django_ and Pinax_. There was a necessity to make all the forms in Pinax `Section 508`_ compatible, and the thought of going through all of forms and rewriting ``{{ form }}`` as a block of ``{% for field in form %}`` with all the template logic seemed like way too much work.

So with the encouragement of `Katie Cunningham`_, `James Tauber`_ and `Jannis Leidel`_ Daniel took the Django docs on forms and combined it with Dragan Babic's excellent Uni-Form css/javascript library and created the ubiquitous ``as_uni_form`` filter. After that, fixing all the forms in Pinax to be section 508 compliant was trivial.

Not long before PyCon 2009 James Tauber suggested the ``{% uni_form form helper %}`` API, where one could trivially create forms without writing any HTML.

At PyCon 2009 Jannis Leidel helped Daniel through releasing the 0.3 release of django-uni-form on PyPI. It was also at that PyCon when the project moved from Google Code to Github.

Around January 2011 the project wasn't very active, Github issues and forks were stacking up. At that time `Miguel Araujo`_ found django-uni-form and loved the concept behind its architecture. He started working in a fork of the project, trying to gather some old submitted patches. Around march of 2011, after conversations with Daniel, he got commit powers in the project's repository, reactivating dev branch. Releases 0.8.0, 0.9.0 followed and the project more than doubled its watchers in Github.

By the end of 2011, Miguel and Daniel agreed on the necessity of renaming the project. As uni-form CSS framework was not anymore the only option available and the name was confusing the users. Thus django-crispy-forms was born, named by `Audrey Roy`_. The project is now actively maintained and leaded by `Miguel Araujo`_.

.. _faq-how-fast:

How fast is django-crispy-forms
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Performance in form rendering is normally a nigh moot issue in Django, because the majority of speed issues are fixable via appropriate use of Django's cache engine. Templates and especially form rendering are usually the last things to worry about when you try to increase performance.

However, because we do care about producing lean and fast code, work is being done to speed up and measure performance of this library. These are the average times of rendering 1000 forms with the latest django-crispy-forms code in Dell Latitude E6500 Intel Core 2 Duo @ 2.53GHz.

In production environments, you will want to activate template caching, see :ref:`install`.

=====================================  ==========================
Method                                 Time with template caching
=====================================  ==========================
Plain Django                           0.915469169617 sec
``|crispy`` filter                     4.23220916295 sec
``{% crispy %}`` tag                   4.53284406662 sec
=====================================  ==========================

.. _faq-python-versions:

Which versions of Python does this support?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Versions supported include Python 2.6.x, 2.7.x, Python 3.3.x. If you need greater backwards compatibility, django-crispy-forms below 1.3 supports 2.5.x, and django-uni-form 0.7.0 supports Python 2.4.x.

.. _faq-django-versions:

Which versions of Django does this support?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Versions supported include Django 1.3 or higher. Versions of django-crispy-forms below 1.3 support Django 1.2.x. If you need to support earlier versions you will need to use django-uni-form 0.7.0.

.. _`Daniel Greenfeld`: http://twitter.com/pydanny
.. _`Miguel Araujo`: http://twitter.com/maraujop
.. _`Audrey Roy`: http://twitter.com/audreyr
.. _`Katie Cunningham`: http://twitter.com/kcunning
.. _Django: http://djangoproject.com
.. _Pinax: http://pinaxproject.com
.. _`NASA's Science Mission Directorate`: http://science.nasa.gov
.. _`Section 508`: http://en.wikipedia.org/wiki/Section_508
.. _`James Tauber`: http://jtauber.com/
.. _`Jannis Leidel`: http://twitter.com/jezdez
