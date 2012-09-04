# CHANGELOG for django-crispy-forms

## 1.2.0

 * Redoing testing structure a litte bit, to run uni_form and bootstrap tests separately. They share most of the code base, but templates pack are separate and we need to care both have the same quality assurance.
 * `AppendedText`, `PrependedText` and `AppendedPrependedText` were not respecting `form_show_errors` helper attribute, see #GH-77.
 * Added a version string to the app under root __init__, see #GH-76.
 * Added `html5_required` helper attribute for rendering required fields using HTML5 required attribute within the input, see #GH-72. Thanks to Lloyd Philbrook.
 * Some docs typos and errors fixed, also a major upgrade to docs covering the new functionality.
 * Adding a `utils.render_crispy_form` function, that renders a form the crispy way in Python code. This might be useful with AJAX, testing or text generation/manipulation, see #GH-64.
 * Tiny cosmetic fix, that adds an space after a button, see #GH-62.
 * `MultiField` and `Fieldset` layout objects can now have any kind of attribute defined, thanks to Lloyd Philbrook, see #GH-71.
 * Making `Fieldset`, `MultiField` & `HTML` contents lazy translatable thanks to Rivo Laks, see #GH-69.
 * Fixing `radioselect` checked status when used for a FK in a ModelForm, see #GH-68.
 * Fixing `form.Meta` usage, using instance `fields` instead of static `Meta` definition, so that it works when updating forms on the go, see #GH-59.
 * Added a low level manipulation API for layout and layout objects. Added a `LayoutObject` base class that creates an interface. This allows to access nested fields easily and use list methods without know internals of the system.
 * Added a `|classes` filter that returns field's classes.
 * Now `FormHelper` can accept a form instance as an optional first argument, from which it can build a default layout.
 * Added an API for manipulating dynamic layouts and programmatic layout building.
 * Added `UneditableField` bootstrap layout object for uneditable fields.
 * Support for hiding fields using `Field('field_name', type="hidden")`, see #GH-55.
 * Avoid template context pollution of variable `form` after using {% crispy %} tag, see #GH-54.
 * Added an `attrs` helper attribute, for more flexible form attributes, see #GH-48.
 * New `AppendedPrependedText` layout object thanks to Samuel Goldszmidt, see #GH-45.
 * Removal of some whitespace in crispy form's HTML generated, see #GH-42.
 * New `MultiWidgetField` layout object by Michal Kuffa, see #GH-39.

## 1.1.4 (2012/5/24)

 * Multithread safety improvements for `BasicNode`.
 * Security fix: Thread safety fixes to `CrispyFieldNode` thanks to Paul Oswald. This avoids leaking information between requests in multithreaded WSGI servers.
 * Added css class `control-label` to `AppendedText` and `PrependedText` layout object's templates.
 * `{% crispy field %}` tag can now pass attrs to `MultiWidget` subclasses by Michal Kuffa. `attrs` are set for sub-widgets. Also `attrs` can now be an iterable for passing different attributes to different sub-widgets. For example,this way MultiWidget's widgets get css classes set correctly.
 * Turning underscores into hyphens for `Field` layout objects.
 * Fix for `ChoiceFields` using non-string choices with radio buttons thanks to Rudy Mutter. See #GH-46, #GH-43 and #GH-35.

## 1.1.3 (2012/4/21)

 * `|crispy` and `|as_crispy_field` filters were not rendering errors. Thanks to @ximi for reporting it and submitting a patch. See issue #GH-28.
 * Fixing a test that was breaking when language was not English. Thanks to @gaftech, see #GH-30.
 * Fixing `radioselect.html` and `checkboxselectmultiple.html` templates. Thanks to Christopher Petrilli for submitting a patch for `radioselect`. See issue #GH-35.
 * HTML attributes can now be set in `BaseInput` subclasses like `Button` by @jamesmfriedman. See #GH-32.
 * Fix for dynamic crispy-forms with Meta classes by Jeroen Vloothuis. See #GH-37.
 * Labels now use `id_for_label` instead of `auto_id` to avoid ids breaking on multiwidgets. by Daniel Izquierdo. See #GH-38.
 * Adding a flatatt custom function in `utils.py` for flatting extra HTML attributes.
 * HTML attributes can now be set in `Div` layout object.
 * Adding tests for new functionality and bugs.

## 1.1.2 (2012/2/29)

 * input name attribute is no longer slugified if only one word is provided, respecting caps.
 * Changes in bootstrap global error templates by David Bennett.
 * Added class `control-label` to labels, for horizontal layout thanks to bitrut.
 * Using `{{ field.html_name }}` instead of `{{ field.name }}` in field templates, so that they work with form prefixes (formwizard) by Patrick Toal.
 * Fixing error rendering in bootstrap AppendedText and PrependedText.
 * Applying `field.css_classes` in bootstrap `field.html` instead of widget classes.
 * Fixes for bootstrap simple checkbox input to be wrapped correctly.

## 1.1.1 (2012/2/17)

 * Fixing a critical bug in bootstrap templates, that was breaking `{% load crispy_forms_tags %}`

## 1.1.0

 * Fixing produced html by a checkbox field, closing label the right way and rendering checkbox in the right place.
 * Passing full context to field rendering, to be consistent and having acess in `field.html` template to helper attributes.
 * Custom helper attributes can now be set and will be part of templates context, this way you can define custom specific behavior.
 * Adding @kennethlove bootstrap template pack into django-crispy-forms core.
 * Adding `CRISPY_TEMPLATE_PACK` setting variable to easily switch between different template packs. Default template pack is now bootstrap.
 * Upgrading bootstrap templates, fixing some bugs and redoing the hierarchy.
 * Upgrading tests for multiple template packs. 
 * Renaming `UNIFORM_FAIL_SILENTLY` setting variable to `CRISPY_FAIL_SILENTLY`, upgrading migration instructions.
 * Redoing bootstrap `field.html` template to render `radioselect` and `checkboxselectmultiple` Django widgets a la bootstrap.
 * Adding a `render_unmentioned_fields` helper attribute, that renders all fields in a form, no matter what the layout is. Default is `False`.
 * Adding a `|css_class` filter that renders field classes in an elegant way.
 * Turning `|with_class` filter into `{% crispy_field %}` tag, so that parameters for rendering the field can be passed.
 * Adding a `help_text_inline` helper attribute, that controls wether to render help texts in bootstrap with "help-inline" or "help-block".
 * Adding a `flat_attrs` variable to the context passed to `field.html` to be able to do all kind of html attributes when rendering a field, using `Field` layout object.
 * Adding a `template` kwarg to `Field` layout object that allows to override template used for rendering a field.
 * Adding a `bootstrap.py` module that holds bootstrap specific layout objects, for higher bootstrap integration.
 * Adding a `AppendedText`, `PrependedText` and `FormActions` bootstrap layout objects. First two based in polyvalent `Field` layout object.

## 1.0.0

 * Using `baseinput.html` template within `whole_uni_form.html`, to be DRY and consistent.
 * `BaseInput` subclasses like `Submit` can now have ids set, ussing `css_id`
 * Adding a simplified alternative syntax for `{% uni_form %}` tag. We can now do `{% uni_form form %}` for rendering a form using a helper, instead of `{% uni_form form form.helper %}`, if the `FormHelper` attribute attached to the form is named `helper`.
 * Improving `rendered_fields` checking performance.
 * Layouts are now rendered strictly. We don't render fields missed in the layout. If the form has a Meta class with `fields` or `exclude`, then we follow Django standards.
 * Added `Field` layout object. You can wrap name fields within and set all kind of attributes easily or override widget template.
 * Fixed #GH-111 we were not rendering all the classes in `|with_class` filter
 * Moving django-uni-form to django-crispy-forms. Renaming tags, filters and modules. Updating tests and so on. Adding migration instructions.
 * More work on simpler and easier docs.
 * Adding `form_show_errors` helper attribute, that controls wether to render or not `form.errors`
 * Improving template hierarchy for more template code reusability.

# CHANGELOG for django-uni-form

## 0.9.0

You can read on how to use new features included in this version at:
http://tothinkornottothink.com/post/10398684502/django-uni-form-0-9-0-is-out-security-fix

 * Fixed a bug in `|with_class` filter so that it supports `show_hidden_initial`, see #GH-95 to not break.
 * Fixed a problem on Fieldset's legends internationalization. Thanks to Bojan Mihelac, see #GH-90.
 * Fixed XSS bug thanks to Charlie Denton, see #GH-98. Errors cannot be rendered safe, because field's input can be part of the error message, that would mean XSS.
 * Updating and improving docs, adding more use case examples.
 * Split `helpers.py` file into `helper.py`, `layout.py` and `utils.py`. Added a deprecation warning. 
 * Improved testing coverage, specially for formsets and i18n.
 * Improved rendering performance of `{% uni_form %}` tag and `|as_uni_form` filter avoiding reloading templates every time, see #GH-81.
 * Added support for Django `Form.error_css_class` and `Form.required_css_class` custom CSS classes, see #GH-87.
 * Moved template code in Layout objects into separate files in `uni_form/layout` directory. Layout objects templates can now be easily overriden, see #GH-37.
 * `form_style` can now be used without having to set a helper Layout, see #GH-85.
 * `form_action` is not lowered anymore and `form_action` is set to "" by default instead of "." thanks to Jianbo Guo, see #GH-84.
 * `Multifield` field template `multifield.html` markup fixed, adding `help_text` support and removing `labelclass` from labels.
 * Fixed testing suite, when run not using `DjangoTestSuiteRunner` provided, thanks to Narsil #GH-82.
 * Removed test_project from the project.
 * Improved `MultiField` performance avoiding instantiating BoundFields twice.
 * Fixed a bug in `MultiField` that raised an exception when internal fields had errors, because of `self.css` not existing.
 * Added an extra optional parameter to `render_field` called `layout_object`, used for storing in it a list of bound fields.
 * Refactor all Layout objects to use templates and not having hardcoded HTML in the code, based on Jonas Obrist work. Resolves Issue #GH-37 
 * Added a Layout object called `Div`. `Row` and `Column` both inherit from `Div`
 * `Layout` can now be a child of `Layout`, see issue #GH-76.

## 0.8.0

You can read on how to use new features included in this version at:
http://tothinkornottothink.com/post/7339670508/new-kung-fu-in-django-uni-form-0-8-0

 * Elevated Miguel Araujo to project lead!
 * Added a forloop simulator for formset forms rendering.
 * `ButtonHolder` Layout object added for holding `HTML` and buttons: `Submit`, `Reset`, `Button`.
 * Turned BaseInput inherited objects like: `Submit`, `Reset`, `Hidden` and `Button` into Layout objects.
 * Fixed a bug with `rendered_fields` when no fields where in the Layout.
 * `Fieldset` legends are now templates full context aware.
 * Based on @issackelly's and @johnthedebs's work a template called `betterform` has been added for supporting @carljm's form-utils BetterForms.
 * `FormHelper` method `get_attr` has been renamed to `get_attributes`
 * `uni_form_tags` has been split into two different files: `uni_form_tags` and `uni_form_filters`.
 * Removing i18n tags from the templates, as they are not necessary anymore.
 * Removed all the internationalized hardcoded text, in favor of template variables: `form_error_title` and `formset_error_title`, both can be set as helper's attributes.
 * `as_uni_errors` filter can now render formset's `non_form_errors` uni-form way.
 * Moved `{% uni_form_setup %}` tag to use STATIC_URL instead of MEDIA_URL
 * Added the possibility to specify a helper for formsets too.
 * Renamed media directory to static, to be compatible with Django 1.3 staticfiles.
 * Added a `form_style` FormHelper attribute for setting global style of a form: inline or default.
 * Turning `HTML` into a full context aware django template field, having access to the whole context of the template in which the form is rendered.
 * Turning `Layout` and `Fieldset` fields attributes into lists, so that they can be changed dynamically.
 * Changing formHints from paragraphs to divs, so ul or ol can be placed within.
 * Removing slugify filter from form ids, so they can be set as user's preferences.
 * Added CSS class 'asteriskField' for asterisks. Added CSS class 'fieldRequired' for required input labels. 
 * `UNIFORM_FAIL_SILENTLY` variable setting has been added for making django-uni-form log errors and fail silently, based on Adam Cupiał's work.
 * Several bug fixes in `MultiField`.
 * Added unicode support for layout field names and improved error handling.
 * Refactored testing system and raised testing coverage.
 * Clean part of the code base and comments. All old CSRF code for supporting old versions of Django has been removed.
 * Refactored BasicNode for better readability and reducing lines of code. 
 * Added formsets support based on Victor Nagy's (nagyv) and Antti Kaihola's (akahiola) work.
 * Bug fix in `{% uni_form %}` tag that didn't work without a helper and it was meant to be optional.
 * CSS classes can be set in Submit buttons.
 * Thanks to J. Javier Maestro (jjmaestro) now we can set ids and classes for `Fieldset`, `MultiField`, `Row` and `Column`.
 * Thanks to Richard Marko (sorki) changed CSS class of PasswordInput widget.
 * Removing `Toggle` class as it wasn't being used anywhere.
 * Moved `BaseInput` to helpers and removed `util.py` file.
 * Removed `{% uni_form_jquery %}` tag
 * Removed `namify` function from tags, as It wasn't being used anywhere.

 * Improved internal documentation
 * form methods generated by FormHelper are in lowercase (http://github.com/pydanny/django-uni-form/issues#issue/20)
 * Thanks to Nagy Viktor added form_tag attribute to FormHelper. Now you can use the uni_form tag without the leading and trailing form tags.
 * Thanks for Alison Rowland for giving django-uni-form sphinx docs
 * Incorporated uni-form 1.4 by Dragan Babic
 * Provide better adherence to uni-form specification of error messages
 * mirumee provided some great work for making FormHelper more subclassable.
 * django-uni-form 0.8 and higher lays out the HTML for the uni_form tag differently. The errorMsg div is now outside the fieldset as it should be.
 * Thanks to Casper S. Jensen django-uni-form now supports 1.2 style csrf_token.
 * csrf_token does not break earlier versions of Django. This will change when no version of django does not support csrf_token.
 * Thanks to j0hnsmith changed {{ error }} to {{ error|safe }} so that html (eg links) can be added to error messages.
 * Thanks to j0hnsmith changed {{ field.label }} to {{ field.label|safe }} so that html (eg  links) can be added to field labels
 * Kudos to Stepan Rakhimov fixed an admin datetime issue.
 * Thanks to patrys (Patryk Zawadzki) FormHelper class is now easily subclass-able.
 * Sorki (Richard Marko) made it so things work better in direct_to_template.

## 0.7.0

 * Removed a <hr /> from the layout module.
 * Changed templatetags/uni_form.py to templatetags/uni_form_tags.py. Yes, this breaks backwards compatibility but fixes a namespace problems in Django with naming a templatetag library after the parent application.
 * Changed form_action attribute to accept not just named URLs but also any old URL.
 * Added in uni_form_setup tag.
 * Added tests
 * Added several new contributors including Dragan Babic
 * Added Danish language translation
