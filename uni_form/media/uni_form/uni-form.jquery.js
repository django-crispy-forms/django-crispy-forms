// Author: Ilija Studen for the purposes of Uni–Form

jQuery.fn.uniform = function(settings) {
  settings = jQuery.extend({
    valid_class    : 'valid',
    invalid_class  : 'invalid',
    focused_class  : 'focused',
    holder_class   : 'ctrlHolder',
    field_selector : 'input, select, textarea'
  }, settings);
  
  return this.each(function() {
    var form = jQuery(this);
    
    // Focus specific control holder
    var focusControlHolder = function(element) {
      element.parent('div[class~=' + settings.holder_class + ']').addClass(settings.focused_class);
    };
    
    var removeFocusClass = function(){
      form.find('.' + settings.focused_class).removeClass(settings.focused_class);
    };

    // Select form fields and attach them higlighter functionality
    form.find(settings.field_selector).focus(function() {
      removeFocusClass();
      focusControlHolder(jQuery(this));
    }).blur(function() {
      removeFocusClass();
    });
  });
};

// Auto set on page load...
$(document).ready(function() {
  jQuery('form.uniForm').uniform();
});
