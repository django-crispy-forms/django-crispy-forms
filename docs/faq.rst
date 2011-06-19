===
FAQ
===

How did this all get started?
=============================

In December 2008, while working for `NASA's Science Mission Directorate`_, my team began to use Django_ and Pinax_. We needed to make all the forms in Pinax `Section 508`_ compatible, and the thought of going through all of 30+ forms and rewriting `{{ form }}` as a block of `{% for field in form %}` with all the template logic seemed like way too much work.

So with the encouragement of Katie Cunningham, `James Tauber`_ and `Jannis Leidel`_ I took the Django docs on forms and combined it with Dragan Babic's excellent Uni-Form css/javascript library and created the ubiquitous `as_uni_form` filter. After that, fixing all the forms in Pinax to be section 508 compliant was trivial.

Not long before PyCon 2009 James Tauber suggested the `{% uni_form form helper %}` API, where one could trivially create forms without writing any HTML.

At PyCon 2009 Jannis Leidel helped me through releasing the 0.3 release of django-uni-form on PyPI. It was also at that PyCon that I believe I switched the library from Google Project Hosting to Github.

How fast is django-uni-form?
============================

Performance in form rendering is normally a nigh moot issue in Django, because the majority of speed issues are fixable via appropriate use of Django's cache engine. Template and especially form rendering are usually the last thing to worry about when you try to increase performance.

However, because we do care about producing lean and fast code, work is being done to speed up and measure performance of this library. These are the results of rendering 1000 forms using the cached template loader with the latest django-uni-form code::

    # Using cached template loader with the improved version:
    Plain Django: 1.52724218369
    Django-uni-form |as_uni_form filter: 3.98601007462
    Django-uni-form {% uni_form %} tag: 4.8678791523

.. _Django: http://djangoproject.com
.. _Pinax: http://pinaxproject.com
.. _`NASA's Science Mission Directorate`: http://science.nasa.gov
.. _`Section 508`: http://en.wikipedia.org/wiki/Section_508
.. _`James Tauber`: http://jtauber.com/
.. _`Jannis Leidel`: http://twitter.com/jezdez
