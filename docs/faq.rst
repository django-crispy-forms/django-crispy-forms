===
FAQ
===

How did this all get started?
=============================

In December 2008, while Daniel Greenfeld was working for `NASA's Science Mission Directorate`_, his team began to use Django_ and Pinax_. There was a necessity to make all the forms in Pinax `Section 508`_ compatible, and the thought of going through all of forms and rewriting `{{ form }}` as a block of `{% for field in form %}` with all the template logic seemed like way too much work.

So with the encouragement of Katie Cunningham, `James Tauber`_ and `Jannis Leidel`_ Daniel took the Django docs on forms and combined it with Dragan Babic's excellent Uni-Form css/javascript library and created the ubiquitous `as_uni_form` filter. After that, fixing all the forms in Pinax to be section 508 compliant was trivial.

Not long before PyCon 2009 James Tauber suggested the `{% uni_form form helper %}` API, where one could trivially create forms without writing any HTML.

At PyCon 2009 Jannis Leidel helped Daniel through releasing the 0.3 release of django-uni-form on PyPI. It was also at that PyCon when the project moved from Google Code to Github.

Around January 2011 the project wasn't very active, Github issues and forks were stacking up. At that time Miguel Araujo found django-uni-form and loved the concept behind its architecture. He started working in a fork of the project, trying to gather some old submitted patches. Around march of 2011, after conversations with Daniel, he got commit powers in the project's repository, reactivating dev branch. Releases 0.8.0, 0.9.0 followed and the project more than doubled its watchers in Github.

By the end of 2011, Miguel and Daniel agreed on the necessity of renaming the project. As uni-form CSS framework was not anymore the only option available and the name was confusing the users. Thus django-crispy-forms was borned, named by Audrey Roy. The project is now actively maintained and leaded by Miguel Araujo.


How fast is django-crispy-forms
===============================

Performance in form rendering is normally a nigh moot issue in Django, because the majority of speed issues are fixable via appropriate use of Django's cache engine. Templates and especially form rendering are usually the last things to worry about when you try to increase performance.

However, because we do care about producing lean and fast code, work is being done to speed up and measure performance of this library. These are the average times of rendering 1000 forms with the latest django-crispy-forms code in Dell Latitude E6500 Intel Core 2 Duo @ 2.53GHz:

===================================== ============================= ==========================
Method                                Time without template caching Time with template caching
===================================== ============================= ==========================
Plain Django                          0.921598911285 sec            0.915469169617 sec
Django-uni-form `|as_uni_form` filter 4.37760996819 sec             4.23220916295 sec
Django-uni-form `{% uni_form %}` tag  5.63008499146 sec             4.53284406662 sec
===================================== ============================= ==========================

Version 0.9.0 added an important performance boost that makes times with and without caching very close to each other.


Which versions of Python does this support?
=============================================

Versions supported include Python 2.5.4, 2.6.x, and 2.7.x. If you need greater backwards compatibility django-uni-form 0.7.0 supports Python 2.4.x.


Which versions of Django does this support?
=============================================

Versions supported include Django 1.2.x and Django 1.3.x. If you need greater backwards compatibility django-uni-form 0.7.0 supports Django 1.1.x.

.. _Django: http://djangoproject.com
.. _Pinax: http://pinaxproject.com
.. _`NASA's Science Mission Directorate`: http://science.nasa.gov
.. _`Section 508`: http://en.wikipedia.org/wiki/Section_508
.. _`James Tauber`: http://jtauber.com/
.. _`Jannis Leidel`: http://twitter.com/jezdez
