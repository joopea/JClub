(function (d, $) {
    'use strict';

    $.validator = (new function Validator () {

        var $defaultContext = $('body');

        this.errorTemplate = function (error) {
            return '<li>' + error.message + '</li>';
        };

        this.errorWarpperTemplate = function (errors) {
            return '<ul class="errorlist mm-listview">' + errors + '</ul>';
        };

        this.createErrors = function (errors) {
            var messages = errors.map(this.errorTemplate).join('');
            return $(this.errorWarpperTemplate(messages));
        };

        this.addError = function (field, errors, context) {
            var messages = this.createErrors(errors);
            var $field = $('[name="' + field + '"]', context);
            $field.prev('.errorlist').remove();
            $(messages).insertBefore($field);
        };

        this.removeError = function (field) {
            var $field = $('[name="' + field + '"]');
            $field.prev('.errorlist').remove();
        };

        this.validate = function (errors, context) {
            context = context || $defaultContext;

            var i, l, keys = Object.keys(errors);

            $('.errorlist').remove();

            for (i=0, l=keys.length; i<l; ++i) {
                this.addError(keys[i], errors[keys[i]], context);
            }

        };

    }());

}(document, jQuery));
