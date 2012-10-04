// Avoid `console` errors in browsers that lack a console.
if (!(window.console && console.log)) {
    (function() {
        var noop = function() {};
        var methods = ['assert', 'clear', 'count', 'debug', 'dir', 'dirxml', 'error', 'exception', 'group', 'groupCollapsed', 'groupEnd', 'info', 'log', 'markTimeline', 'profile', 'profileEnd', 'markTimeline', 'table', 'time', 'timeEnd', 'timeStamp', 'trace', 'warn'];
        var length = methods.length;
        var console = window.console = {};
        while (length--) {
            console[methods[length]] = noop;
        }
    }());
}

// Place any jQuery/helper plugins in here.
$(function(){
    if ($.fn.datepicker) {
        $('[data-datepicker=datepicker]').datepicker({
            dateFormat: "yy-mm-dd"
        });
    }
});


(function ($) {
    $.fn.extend({
        autocompleteNames:function (options) {
            this.defaultOptions = {};

            var settings = $.extend({}, this.defaultOptions, options);

            return this.each(function () {
                var $this = $(this), cache = {}, lastXhr;
                $this.autocomplete({
                    minLength:2,
                    source:function (request, response) {
                        var term = request.term;
                        if (term in cache) {
                            response(cache[term]);
                            return;
                        }

                        lastXhr = $.getJSON(settings.url,
                            request,
                            function (data, status, xhr) {
                                cache[ term ] = data;
                                if (xhr === lastXhr) {
                                    response(data);
                                }
                            }
                        );
                    }
                });
            });
        }
    });
})(jQuery);