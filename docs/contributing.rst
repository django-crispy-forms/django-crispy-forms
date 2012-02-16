============
Contributing
============

Setup
=====

Fork on github
--------------

Before you do anything else, login/signup on Github.com and fork django-crispy-forms from https://github.com/pydanny/django-crispy-forms.

Clone your fork locally
-----------------------

If you have git-scm installed, you now clone your git repo using the following command-line argument where <my-github-name> is your account name on github::

    git clone git@github.com/<my-github-name>/django-crispy-forms.git

Setting up topic branches and generating pull requests
======================================================

While it's handy to provide useful code snippets in an issue, it is better for
you as a developer to submit pull requests. By submitting pull request your
contribution to django-crispy-forms will be recorded by Github. 

In git it is best to isolate each topic or feature into a "topic branch".  While
individual commits allow you control over how small individual changes are made
to the code, branches are a great way to group a set of commits all related to
one feature together, or to isolate different efforts when you might be working
on multiple topics at the same time.

While it takes some experience to get the right feel about how to break up
commits, a topic branch **must** be limited in scope to a single ``issue`` as
submitted to an issue tracker.

Also since github pegs and syncs a pull request to a specific branch, it is the
**ONLY** way that you can submit more than one fix at a time.  If you submit
a pull from your master branch, you can't make any more commits to your master
without those getting added to the pull.

To create a topic branch, its easiest to use the convenient ``-b`` argument to ``git
checkout``::

    git checkout -b fix-broken-thing
    Switched to a new branch 'fix-broken-thing'

You should use a verbose enough name for your branch so it is clear what it is
about. Now you can commit your changes and regularly merge in the upstream
master as described below.

When you are ready to generate a pull request, either for preliminary review,
or for consideration of merging into the project you must first push your local
topic branch back up to github::

    git push origin fix-broken-thing

Now when you go to your fork on github, you will see this branch listed under
the "Source" tab where it says "Switch Branches".  Go ahead and select your
topic branch from this list, and then click the "Pull requst" button.

Here you can add a comment about your branch.  If this in response to
a submitted issue, it is good to put a link to that issue in this initial
comment.  The repo managers will be notified of your pull request and it will
be reviewed (see below for best practices).  Note that you can continue to add
commits to your topic branch (and push them up to github) either if you see
something that needs changing, or in response to a reviewer's comments.  If
a reviewer asks for changes, you do not need to close the pull and reissue it
after making changes. Just make the changes locally, push them to github, then
add a comment to the discussion section of the pull request.

Pull upstream changes into your fork regularly
==================================================

django-crispy-forms is worked on by a lot of people. It is therefore critical that you pull upstream changes from trunk into your fork on a regular basis. Nothing is worse than putting in days of hard work into a pull request only to have it rejected because it has diverged too far from trunk.

To pull in upstream changes::

    git remote add trunk git://github.com/maraujop/django-crispy-forms.git
    git fetch trunk

Check the log to be sure that you actually want the changes, before merging::

    git log ..django-crispy-forms/master

Then merge the changes that you fetched::

    git merge django-crispy-forms/master

For more info, see http://help.github.com/fork-a-repo/

How to get your Pull Request accepted
=====================================

We want your submission. But we also want to provide a stable experience for our users and the community. Follow these rules and you should succeed without a problem!

Run the tests!
--------------

Before you submit a pull request, please run the entire django-crispy-forms test suite via::

    cd crispy_forms/tests
    ./runtests.py

The first thing the core committers will do is run this command. Any pull request that fails this test suite will be **rejected**.

It's always good to add tests!
------------------------------

We've learned the hard way that code without tests is undependable. If your pull request comes with tests, it's got a greater chance to be included. Otherwise the lead will ask you to code them or will help you doing so.

We use the Django Test framework (based on unittest).

Also, keep your tests as simple as possible. Complex tests end up requiring their own tests. We would rather see duplicated assertions across test methods then cunning utility methods that magically determine which assertions are needed at a particular stage. Remember: `Explicit is better than implicit`.

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
