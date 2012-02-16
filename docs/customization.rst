=============
Customization
=============

Some ways to customize the behavior of django-crispy-forms.


Customizations on '*' required fields (optional)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you don't like the use of '*' (asterisk) to denote required fields you have two options:

* Asterisks have an 'asteriskField' class set. So you can hide it using CSS rule::

    .asteriskField {
        display: none;
    }
    
* You can always override templates. Create your own template for ``field.html``.
