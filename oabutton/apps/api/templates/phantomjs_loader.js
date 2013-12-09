var page = require('webpage').create();
page.settings.resourceTimeout = 10000; // 10 seconds
page.onResourceTimeout = function(e) {
    console.log(e.errorCode);   // it'll probably be 408 
    console.log(e.errorString); // it'll probably be 'Network timeout on resource'
    console.log(e.url);         // the url whose request timed out
    phantom.exit(1);
};

var url = '{{ url }}';
page.open(url, function (status) {
    // Just run javascript on the page without doing anything.  A lot
    // of pages will have javascript 
    page.evaluate(function () {});
    console.log(page.content);
    phantom.exit();
});
