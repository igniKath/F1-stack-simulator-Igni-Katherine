// Optional interface help only. No JavaScript stack or click handlers.
if (window.jQuery) {
    jQuery(function ($) {
        $('#st_data').trigger('focus');
        $('#stack .stack-item.peek').hide().fadeIn(1000);
        // TODO J1 during the demo: animate the top item marked by Jinja after Peek.
    });
}
