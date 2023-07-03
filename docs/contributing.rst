============
Contributing
============

Setup
=====

Fork on GitHub
--------------

Before you do anything else, login/signup on GitHub.com and fork django-crispy-forms from https://github.com/django-crispy-forms/django-crispy-forms.

Clone your fork locally
-----------------------

If you have git-scm installed, you now clone your git repository using the following command-line argument where <my-github-name> is your account name on GitHub::

    git clone git@github.com/<my-github-name>/django-crispy-forms.git

Install requirements
--------------------

Install dependencies for development by **cd**-ing into the crispy-forms folder and then running:: 

    pip install -r requirements.txt

In addition to these requirements you will also need to install Django itself. To install the current version of Django::
    
    pip install django

Django-crispy-forms comes with git hook scripts. These can be installed by running::

    pre-commit install
    
Pre-commit will now run automatically on git-commit and check adherence to the style guide (black, isort & flake8).

Build the documentation locally
===============================

If you make documentation changes they can be seen locally.
In the directory where you cloned ``django-crispy-forms``::

    cd docs
    pip install -r requirements.txt
    make html

You can open the file ``_build/html/index.html`` and verify the changes.

Setting up topic branches and generating pull requests
======================================================

While it's handy to provide useful code snippets in an issue, it is better for
you as a developer to submit pull requests. By submitting pull request your
contribution to django-crispy-forms will be recorded by GitHub. 

In git it is best to isolate each topic or feature into a "topic branch".  While
individual commits allow you control over how small individual changes are made
to the code, branches are a great way to group a set of commits all related to
one feature together, or to isolate different efforts when you might be working
on multiple topics at the same time.

While it takes some experience to get the right feel about how to break up
commits, a topic branch **must** be limited in scope to a single ``issue`` as
submitted to an issue tracker.

Also since GitHub pegs and syncs a pull request to a specific branch, it is the
**ONLY** way that you can submit more than one fix at a time.  If you submit
a pull from your main branch, you can't make any more commits to your main branch
without those getting added to the pull.

To create a topic branch, its easiest to use the convenient ``-b`` argument to ``git
checkout``::

    git checkout -b fix-broken-thing
    Switched to a new branch 'fix-broken-thing'

You should use a verbose enough name for your branch so it is clear what it is
about. Now you can commit your changes and regularly merge in the upstream
main branch as described below.

When you are ready to generate a pull request, either for preliminary review,
or for consideration of merging into the project you must first push your local
topic branch back up to GitHub::

    git push origin fix-broken-thing

Now when you go to your fork on GitHub, you will see this branch listed under
the "Source" tab where it says "Switch Branches".  Go ahead and select your
topic branch from this list, and then click the "Pull request" button.

Here you can add a comment about your branch.  If this in response to
a submitted issue, it is good to put a link to that issue in this initial
comment.  The repo managers will be notified of your pull request and it will
be reviewed (see below for best practices).  Note that you can continue to add
commits to your topic branch (and push them up to GitHub) either if you see
something that needs changing, or in response to a reviewer's comments.  If
a reviewer asks for changes, you do not need to close the pull and reissue it
after making changes. Just make the changes locally, push them to GitHub, then
add a comment to the discussion section of the pull request.

Pull upstream changes into your fork regularly
==================================================

django-crispy-forms is worked on by a lot of people. It is therefore critical that you pull upstream changes from the main branch into your fork on a regular basis. Nothing is worse than putting in days of hard work into a pull request only to have it rejected because it has diverged too far from main.

To pull in upstream changes::

    git remote add upstream git://github.com/django-crispy-forms/django-crispy-forms.git
    git fetch upstream

Check the log to be sure that you actually want the changes, before merging::

    git log ..django-crispy-forms/main

Then merge the changes that you fetched::

    git merge django-crispy-forms/main

For more info, see https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/about-forks

How to get your Pull Request accepted
=====================================

We want your submission. But we also want to provide a stable experience for our users and the community. Follow these rules and you should succeed without a problem!

Run the tests!
--------------

Before you submit a pull request, please run the entire django-crispy-forms test suite via::

    make test

If you don't have ``make`` installed the test suite can also be run via::

    pytest --ds=tests.test_settings --cov=crispy_forms

The first thing the core committers will do is run this command. Any pull request that fails this test suite will be **rejected**.

It's always good to add tests!
------------------------------

We've learned the hard way that code without tests is undependable. If your pull request comes with tests, it's got a greater chance to be included. Otherwise the lead will ask you to code them or will help you doing so.

We use the py.test.

Also, keep your tests as simple as possible. Complex tests end up requiring their own tests. We would rather see duplicated assertions across test methods than cunning utility methods that magically determine which assertions are needed at a particular stage. Remember: `Explicit is better than implicit`.

Don't mix code changes with whitespace cleanup
----------------------------------------------

If you change two lines of code and correct 200 lines of whitespace issues in a file the diff on that pull request is functionally unreadable and will be **rejected**. Whitespace cleanups need to be in their own pull request.

Keep your pull requests limited to a single issue
--------------------------------------------------

django-crispy-forms pull requests should be as small/atomic as possible. Large, wide-sweeping changes in a pull request will be **rejected**, with comments to isolate the specific code in your pull request. Some examples:

#. If you are fixing a bug in one helper class don't '*cleanup*' unrelated helpers. That cleanup belongs in another pull request.
#. Changing permissions on a file should be in its own pull request with explicit reasons why.

Keep your code simple!
----------------------

Memorize the Zen of Python::

    >>> python -c 'import this'

Please keep your code as clean and straightforward as possible. When we see more than one or two functions/methods starting with `_my_special_function` or things like `__builtins__.object = str` we start to get worried. Rather than try and figure out your brilliant work we'll just **reject** it and send along a request for simplification.

Furthermore, the pixel shortage is over. We want to see:

* `helper` instead of `hpr`
* `django-crispy-forms` instead of `dcf`
* `my_function_that_does_things` instead of `mftdt`
