# CHANGELOG for django-crispy-forms

## 1.11.0 (2020-01-30)
* Implemeneted `custom-select` for Select widgets in the Bootstrap4 Template Pack (#1091)
* Fixed `data-parent` in AccodrianGroup (#1091)
* Documentation improvements

See the [1.11.0 Milestone](https://github.com/django-crispy-forms/django-crispy-forms/milestone/13?closed=1) for the full change list

## 1.10.0 (2020-11-18)
* Fixed test causing `SystemCheckError` in some cases. (#1075)
* Radio and Checkbox now respect the field's `disabled` attribute when using the Bootstrap4 template pack. (#1057)
* A number of documentation improvements.

See the [1.10.0 Milestone](https://github.com/django-crispy-forms/django-crispy-forms/milestone/12?closed=1) for the full change list

## 1.9.2 (2020-07-11)
* Fixed FileField UI bug

See the [1.9.2 Milestone](https://github.com/django-crispy-forms/django-crispy-forms/milestone/11?closed=1) for the full change list.

## 1.9.1 (2020-05-16)
* Added Bootstrap 4 styling for clearable file widget.
* Fixed FileField UI bug.
* Project now uses GitHub actions for testing.

See the [1.9.1 Milestone](https://github.com/django-crispy-forms/django-crispy-forms/milestone/10) for the full change list.

## 1.9.0 (2020-02-28)
* Removed support for Python 2.
* Removed support for Django versions prior to 2.2.
* CSS for Column layout object in Bootstrap 4 template pack changed to 'col-md'. Default is now over ridden when another 'col' class is added to css_class.

See the [1.9.0 Milestone](https://github.com/django-crispy-forms/django-crispy-forms/milestone/9) for the full change list.

## 1.8.1 (2019-11-22)

* Fixing FileField UI bug introduced with 1.8.0
* Remove is-valid css class for radio (bug introduced with 1.8.0)
* Various alignment and margin fixes for Bootstrap 4 template pack
* Documentation : using read-the-docs template, documenting how to run test suite, documenting use_custom_control help attributes

See the [1.8.1 Milestone](https://github.com/django-crispy-forms/django-crispy-forms/milestone/8?closed=1) for the full change list.

## 1.8.0 (2019-10-17)

* Updated compatibility for Django 1.11, 2.1, 2.2 and 3.0 in line with Django's
  supported versions policy.
* Numerous improvements to the Bootstrap 4 template pack, which may now be
  considered mature.

  Here are some changes that might affect custom templating you already have in
  place when using Bootstrap 4 :

    * Using [Custom Forms for radio and checkbox](https://www.w3schools.com/bootstrap4/bootstrap_forms_custom.asp).
      You may disable this by setting  `FormHelper.use_custom_control = False`.
    * Using [Bootstrap 4 `"form-row"` class in place of `"row"`](https://getbootstrap.com/docs/4.3/components/forms/#form-row).
    * Fixing [layout hierarchy between input and its label for checkbox and radio](https://getbootstrap.com/docs/4.0/components/forms/#checkboxes-and-radios).

  <small>Links are to the relevant Bootstap 4 docs.</small>

See the [1.8.0 Milestone](https://github.com/django-crispy-forms/django-crispy-forms/milestone/7?closed=1) for the full change list.

Many thanks to all involved in bringing together a great release!

## 1.7.2 (2018-03-09)

* Bugfixes following v1.7.1

See [1.7.1 Milestone](https://github.com/django-crispy-forms/django-crispy-forms/milestone/6?closed=1)
for full issue list.

## 1.7.1 (2018-03-05)

* Bootstrap 4 template pack.

See [1.7.1 Milestone](https://github.com/django-crispy-forms/django-crispy-forms/milestone/5?closed=1)
for full issue list.

## 1.7.0 (2017-10-17)

* Fixes compatibility with Django 2.0
* Various other fixes.

See [1.7 Milestone](https://github.com/django-crispy-forms/django-crispy-forms/milestone/4?closed=1)
for full issue list.

## 1.6.1 (2016-10-17)

  * Updates compatibility for Django 1.10
  * A number of small Bootstrap 4 fixes.

See [1.6.1 Milestone](https://github.com/django-crispy-forms/django-crispy-forms/milestone/3?closed=1)
for full issue list.

## 1.6.0 (2016/1/7)

  * Fixed compatibility with Django 1.9
  * Dropped support for Django 1.7
  * Added Bootstrap 4 template pack
  * Other small fixes.

See [1.6.0 Milestone](https://github.com/maraujop/django-crispy-forms/issues?q=milestone%3A1.6.0+is%3Aclosed) for full issue list.

## 1.5.2 (2015/9/10)

  * Fix: KeyError: u'wrapper_class' when clearing template context. #511, #512
  * Fix: Alignment of stacked checkboxes and radio buttons in Bootstrap 3 #358

See [1.5.2 Milestone](https://github.com/maraujop/django-crispy-forms/issues?utf8=✓&q=milestone%3A1.5.2+) for full issue list.


## 1.5.1 (2015/8/21)

Special thanks in this release to Dmitry Dygalo @Stranger6667 for a marathon effort updating the
test suite and code base.

  * Switched to py.test. Modernised test suite. Enabled tox, code coverage and Travis for all
    supported Python/Django versions. [See list of Merged "Testing/Process" PRs here](https://github.com/maraujop/django-crispy-forms/pulls?q=is%3Apr+is%3Amerged+milestone%3A1.5.1+label%3ATesting%2FProcess)
  * Added compatibility with Python 3.2
  * Fix: Allow LayoutObject & BaseInputs to accept custom template #493


## 1.5.0 (2015/8/16)

Special thanks in this release for all the **<a href="http://flattr.com/thing/512037/django-crispy-forms">supporters and donators</a>**.

 * Fixed compatibility with: Python 3, Django 1.7, Django 1.8 and Django 1.4.16. Merged PR #417, but thanks to PRs #369, #368 and #310. Closes also #383.
 * Updated test suite for compatibility with all supported Django versions 1.4, 1.7, 1.8 and run CI against these and Django `master`. See #451, #455.
 * Bug fix for specifying `template_pack` in `{% crispy %}` tag, `bootstrap3` couldn't be set that way.
 * New doc section for creating custom template packs.
 * Fixed Bootstrap3 checkbox alignment issues with label texts, see #275.
 * First `AccordionGroup` can now be set to `active=False`, see #246.
 * Fixed Bootstrap3 checkbox alignment issues for all device sizes, see #225 and #267.
 * All forms are now rendered with {{ form.media }}, this makes forms containing widgets with `Media` meta class work, see #263.
 * Adjusted `{% specialspaceless %}` to avoid breaking intended spaces and be less aggressive, see #250.
 * Fixed inputs rendering for bootstrap3 and redo `FormActions` layout object bootstrap3 template for correct alignment, see #279.
 * `MultiField` now obeys `form_show_labels`, see #278.
 * Added `wrapper_class` to `bootstrap.InlineRadios`, see #272.
 * Render label for checkboxes within `table_inline_formset.html`, see #262.
 * Removed deprecated layout object `AppendedPrependedText`, replaced by `PrependedAppendedText`.
 * Fixed `PrependedAppendedText` when rendering a select widget, in bootstrap and bootstrap3 template packs, see #258.
 * Added support to `{% crispy_addon %}` tag for `form_show_labels`, see #256.
 * Major cleanup and refactor of the template pack system thanks to @tepez, see #217 and #237:
    - Template packs are now self contained/independent, removing dangerous cross references. If you have a custom template pack this can cause backwards incompatibility, but it will pay in the future to adjust to this changes.
    - `MultiField` cannot be used with `bootstrap` or `bootstrap3` template packs.
    - Added `template_pack` `FormHelper` attribute, so that template packs can be specified at form helper level. This changes layout objects `render` behavior.
 * Default template pack is now `bootstrap3`.
 * Make `CRISPY_TEMPLATE_PACK` setting optional, see #237 and #244.

## 1.4.0 (2013/9/1)

Special thanks in this release to **James Friedman <a href="https://github.com/jamesmfriedman">@jamesmfriedman</a>**, for his amazing support in PR #213, adding initial Bootstrap 3 support.

 * Bootstrap 3 inline forms support and docs for inline forms with Bootstrap 3, see #233.
 * `update_attributes` can now work with a field name, see docs.
 * Adjusted unicode checkings for Python 3, see #231.
 * Adjusted how bootstrap `Tab` layout object attributes are applied to make sense, see #228.
 * Major refactor of testing suite architecture, breaking huge `tests.py` file into several and also splitting tests for different template packs into different tests cases, runners for template packs updated.
 * Added support for horizontal forms in bootstrap3, see #209.
 * Fixed spaces missing when rendering several submit inputs continued, see #211.
 * Fixed checkboxes and radios for Bootstrap3, adjusted multiple inline radios and checkboxes, see #225.
 * Update accordion markup for bootstrap3 compatibility, see #229.
 * Moved `UneditableField` to bootstrap module, place where it should live, no backwards compatible import left behind.
 * Added `bootstrap3` template pack thanks to James Friedman, see #213 and #209.
 * `RadioSelect` and `CheckboxSelectMultiple` widget values and texts were being localized, when they shouldn't bee, see #214.
 * If Django widget attrs where set for `RadioSelect` or `CheckboxSelectMultiple` they were not being rendered by crispy-forms, see #206.
 * `form_show_labels` wasn't working correctly with some layout objects, see #193.

## 1.3.2 (2013/6/23)

 * Labels were not being rendered with `|crispy` filter, see #202.

## 1.3.1 (2013/6/17)

 * Fix default value for `form_show_labels` in case FormHelper doesn't define it, see #199.
 * Added a backported version of `override_settings` for testing django 1.3.7 and adding it to Travis-ci matrix.

## 1.3.0 (2013/6/16)

Special thanks in this release to **Charlie Denton <a href="https://github.com/meshy">@meshy</a>**, for his amazing support in PRs #189 and #190, long due.

 * Deprecated `Tab` and `TabHolder` imports from `layout.py` module, they now live in `bootstrap.py` module.
 * Removed Python 2.5 compatibility.
 * Added `disable_csrf` helper attribute, see docs.
 * Travis-ci support thanks to Charlie Denton, see #190.
 * Python 3 compatibility thanks to Charlie Denton, see #189 and #190.
 * Added a settings variable named `CRISPY_ALLOWED_TEMPLATE_PACKS` for adding easily support for new template packs, see #192.
 * Added `{% crispy_addon %}` tag, see #195.
 * Make `CRISPY_TEMPLATE_PACK` optional for tests
 * Make tests run the same exactly way with `runtests.py` and `manage.py test`, see #183.
 * Bug fix for `wrap_together` when using it with partial slices.
 * Fixes for `KeepContext` context manager, see #180.
 * Added `FormHelper.field_template` attribute, for easily override field template for a specific form/formset, see docs.
 * Added a template for rendering formsets inline within tables named `bootstrap/table_inline_formset.html`, that can be easily used in conjunction with `FormHelper.template`.
 * Added `FormHelper.template` attribute, that easily allows to override form/formset general structure template, see docs.
 * Added `form_show_labels` helper attribute.
 * Redoing filters to use `isinstance` instead of hacky internal name checking, this way subclasses of standard fields will work out of the box with crispy-forms, see #176.

## 1.2.8 (2013/5/10)

 * Bug fix for `KeepContext` context manager, when crispy-forms used with Jingo/Jinja2 templates, see #179.
 * Some formset tests were breaking in some Django versions. Also added a `make test` for easily running project tests, see #178.

## 1.2.7 (2013/5/6)

 * Bug fix for model formsets and inline formsets, when being rendered with a `FormHelper` with a layout set, where some hidden formset management fields would be missing, breaking saving to database.
 * Added `render_hidden_fields` attribute to `FormHelper`, see docs.
 * Added `render_hidden_fields` attribute to `FormHelper`, see docs.

## 1.2.6 (2013/5/1)

 * Fixes to `Container` and `TabHolder`, affecting class variable helpers with layouts containing `TabHolder` or `AccordionGroup` objects, see #172.
 * Bug fix for `KeepContext` context manager, see #172.

## 1.2.5 (2013/4/25)

 * Avoid raising Exceptions in `|as_crispy_field` filter when not in DEBUG mode.
 * Popping `css_id` to avoid having a css-id attribute, see #167.
 * Fixed a bug in dynamic layout API, when wrapping layout objects that had arguments passed after fields. Moving `LayoutSlice` to `layout_slice` module.
 * Fixed test failing when tests runned from manage.py test.
 * Fixed testing name conflict, see #130.

## 1.2.4 (2013/4/13)

 * Added `wrapper_class` kwarg to `Field` layout object, see #163.
 * Added `Accordion` and `AccordionGroup` bootstrap layout objects, see #162.
 * Bug fix in `render_crispy_form` to avoid override existing context, see #153.
 * Use formset iterator instead of `forms` list attribute, see #152.
 * Don't display fieldset legend if empty, see #147 and #155.
 * Bug fix for pickling crispy forms by powderflask, see #107.
 * Switched from `django.form.utils.flatatt` to internal `flatatt` utils implementation, this allows adding data-attrs to `FormActions` and `StrictButton`.
 * `render_field` now uses a context manager to avoid side effects when layout objects update template context. This makes context mutability safe within layout objects.
 * Added `greedy` kwarg to `filter` dynamic API.
 * Fixing error logging on `|as_crispy_field` filter, see #135.
 * Implemented `__delitem__`, `__len__` and `__setitem__` in `LayoutObject` and `DynamicLayoutHandler`, this avoids pylint warnings, see #114.
 * Docs folder no longer included when installing crispy-forms, see #132.
 * Added `wrap_once`, `update_attributes`, `map` and `pre_map` to LayoutSlice.

## 1.2.3 (2012/12/4)

 * Fixed imports to be relative to package, avoiding namespace collisions.
 * Removed circular dependency between `layout` and `bootstrap`, see #129.
 * Bug fix, adapted use of inspect module in `utils.py` to avoid breaking Python 2.5 compatibility.

## 1.2.2 (2012-11-30)

 * Bug fix, reduction of white space in crispy-forms output could mess within tags, see #127, reverting part of this reduction.
 * Renamed `AppendedPrependedText` to `PrependedAppendedText`.
 * Moved `Tab` and `TabHolder` to `bootstrap.py`.

## 1.2.1 (2012-11-28)

 * Bug fix `help_text_inline` set to True, see #117.
 * New fix for the space between buttons problems, see #62.
 * Reduced importantly whitespace in html generated by crispy-forms, forms are now more compact.
 * Added support for specifying a template pack per form, see #66 and #109.
 * Removed `clearfix` class from bootstrap templates, not necessary anymore, see #105.
 * Space cleanup in bootstrap templates, thanks to Si Feng, see #122.
 * Fixed `MultiField` to work with `form_show_errors` helper attribute.
 * Fixed a bug in `MultiField` that set error class when there were form errors, no matter if the fields with errors were contained within, see #120.
 * `FieldWithButtons` now supports `Field` layout object as its first parameter, for setting input attributes.
 * Bug fixes for `FieldWithButtons`, field label, `help_text` or error messages were not being rendered, see #121.
 * Fixed a bug that was making crispy-forms render extra fields with ModelForms that didn't have `Meta.fields` defined, thanks to Jean-Baptiste Juin for reporting it.
 * Fixed a bug that was breaking Django 1.2 compatibility when copying context variables, thanks to Alex Yakovlev for submitting a patch, see #108.
 * Fixed a bug for `AppendedText`, `PrependedText` and `AppendedPrependedText` layout objects, thanks to Bojan Mihelac, see #104.
 * Fixed a bug in appended and prepended text layout objects for respecting hidden fields, thanks to Bojan Mihelac, see #103.
 * Added two new bootstrap layout objects: `FieldWithButtons` and `StrictButton`.
 * Added checks and better error messages for dynamic API.
 * Fixed `get_layout_objects` recursive call for Python2.5 compatibility, thanks to Can Başçıl for reporting it.

## 1.2.0 (2012-9-24)

 * Update prepended and appended templates to respect hidden fields, thanks to Bojan Mihelac, see #GH-103.
 * Added `InlineCheckboxes` to bootstrap layout objects, for rendering checkboxes inline.
 * `BaseInput` subclasses, like `Submit` can now have its value set to a context variable.
 * Rendering inputs added with `add_input` in bootstrap using the right templates, see #GH-95.
 * Improved formsets rendering docs thanks to Samuel Goldszmidt, see #GH-92.
 * Added `Tab` and `TabHolder` layout objects thanks to david-e, see #GH-91.
 * Fixed default bootstrap button default classes thanks to david-e, see #GH-90.
 * Fixed some flaws in new testing structure by Markus Hametner.
 * Added helper attribute `error_text_inline` thanks to Lee Semel for controlling how to render form errors, as a block or inline, see #GH-87.
 * Support `ModelMultipleChoiceField` on `checkboxselectmultiple`, see #GH-86.
 * Redoing testing structure a little bit, to run uni_form and bootstrap tests separately. They share most of the code base, but templates pack are separate and we need to care both have the same quality assurance.
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

## 1.1.4 (2012-5-24)

 * Multithread safety improvements for `BasicNode`.
 * Security fix: Thread safety fixes to `CrispyFieldNode` thanks to Paul Oswald. This avoids leaking information between requests in multithreaded WSGI servers.
 * Added css class `control-label` to `AppendedText` and `PrependedText` layout object's templates.
 * `{% crispy field %}` tag can now pass attrs to `MultiWidget` subclasses by Michal Kuffa. `attrs` are set for sub-widgets. Also `attrs` can now be an iterable for passing different attributes to different sub-widgets. For example,this way MultiWidget's widgets get css classes set correctly.
 * Turning underscores into hyphens for `Field` layout objects.
 * Fix for `ChoiceFields` using non-string choices with radio buttons thanks to Rudy Mutter. See #GH-46, #GH-43 and #GH-35.

## 1.1.3 (2012-4-21)

 * `|crispy` and `|as_crispy_field` filters were not rendering errors. Thanks to @ximi for reporting it and submitting a patch. See issue #GH-28.
 * Fixing a test that was breaking when language was not English. Thanks to @gaftech, see #GH-30.
 * Fixing `radioselect.html` and `checkboxselectmultiple.html` templates. Thanks to Christopher Petrilli for submitting a patch for `radioselect`. See issue #GH-35.
 * HTML attributes can now be set in `BaseInput` subclasses like `Button` by @jamesmfriedman. See #GH-32.
 * Fix for dynamic crispy-forms with Meta classes by Jeroen Vloothuis. See #GH-37.
 * Labels now use `id_for_label` instead of `auto_id` to avoid ids breaking on multiwidgets. by Daniel Izquierdo. See #GH-38.
 * Adding a flatatt custom function in `utils.py` for flatting extra HTML attributes.
 * HTML attributes can now be set in `Div` layout object.
 * Adding tests for new functionality and bugs.

## 1.1.2 (2012-2-29)

 * input name attribute is no longer slugified if only one word is provided, respecting caps.
 * Changes in bootstrap global error templates by David Bennett.
 * Added class `control-label` to labels, for horizontal layout thanks to bitrut.
 * Using `{{ field.html_name }}` instead of `{{ field.name }}` in field templates, so that they work with form prefixes (formwizard) by Patrick Toal.
 * Fixing error rendering in bootstrap AppendedText and PrependedText.
 * Applying `field.css_classes` in bootstrap `field.html` instead of widget classes.
 * Fixes for bootstrap simple checkbox input to be wrapped correctly.

## 1.1.1 (2012-2-17)

 * Fixing a critical bug in bootstrap templates, that was breaking `{% load crispy_forms_tags %}`

## 1.1.0

 * Fixing produced html by a checkbox field, closing label the right way and rendering checkbox in the right place.
 * Passing full context to field rendering, to be consistent and having access in `field.html` template to helper attributes.
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
 * Adding a `help_text_inline` helper attribute, that controls whether to render help texts in bootstrap with "help-inline" or "help-block".
 * Adding a `flat_attrs` variable to the context passed to `field.html` to be able to do all kind of html attributes when rendering a field, using `Field` layout object.
 * Adding a `template` kwarg to `Field` layout object that allows to override template used for rendering a field.
 * Adding a `bootstrap.py` module that holds bootstrap specific layout objects, for higher bootstrap integration.
 * Adding a `AppendedText`, `PrependedText` and `FormActions` bootstrap layout objects. First two based in polyvalent `Field` layout object.

## 1.0.0

 * Using `baseinput.html` template within `whole_uni_form.html`, to be DRY and consistent.
 * `BaseInput` subclasses like `Submit` can now have ids set, using `css_id`
 * Adding a simplified alternative syntax for `{% uni_form %}` tag. We can now do `{% uni_form form %}` for rendering a form using a helper, instead of `{% uni_form form form.helper %}`, if the `FormHelper` attribute attached to the form is named `helper`.
 * Improving `rendered_fields` checking performance.
 * Layouts are now rendered strictly. We don't render fields missed in the layout. If the form has a Meta class with `fields` or `exclude`, then we follow Django standards.
 * Added `Field` layout object. You can wrap name fields within and set all kind of attributes easily or override widget template.
 * Fixed #GH-111 we were not rendering all the classes in `|with_class` filter
 * Moving django-uni-form to django-crispy-forms. Renaming tags, filters and modules. Updating tests and so on. Adding migration instructions.
 * More work on simpler and easier docs.
 * Adding `form_show_errors` helper attribute, that controls whether to render or not `form.errors`
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
 * Moved template code in Layout objects into separate files in `uni_form/layout` directory. Layout objects templates can now be easily overridden, see #GH-37.
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
