if (!$) {
    $ = django.jQuery;
}
function overrideTimeOptions() {
    $("ul.timelist").each(function () {
        entries = $(this).children("li");
        baseEntry = entries.first();
        baseHref = baseEntry.find("a").attr("href");
        entries.remove();
        clock_1am = '<li><a href="' + baseHref.replace(/Date\([^\)]*\)/g, "Date(1970,1,1,1,0,0,0)") + '">01:00</a></li>';
        clock_2am = '<li><a href="' + baseHref.replace(/Date\([^\)]*\)/g, "Date(1970,1,1,2,0,0,0)") + '">02:00</a></li>';
        clock_3am = '<li><a href="' + baseHref.replace(/Date\([^\)]*\)/g, "Date(1970,1,1,3,0,0,0)") + '">03:00</a></li>';
        clock_4am = '<li><a href="' + baseHref.replace(/Date\([^\)]*\)/g, "Date(1970,1,1,4,0,0,0)") + '">04:00</a></li>';
        clock_5am = '<li><a href="' + baseHref.replace(/Date\([^\)]*\)/g, "Date(1970,1,1,5,0,0,0)") + '">05:00</a></li>';
        clock_6am = '<li><a href="' + baseHref.replace(/Date\([^\)]*\)/g, "Date(1970,1,1,6,0,0,0)") + '">06:00</a></li>';
        clock_7am = '<li><a href="' + baseHref.replace(/Date\([^\)]*\)/g, "Date(1970,1,1,7,0,0,0)") + '">07:00</a></li>';
        clock_8am = '<li><a href="' + baseHref.replace(/Date\([^\)]*\)/g, "Date(1970,1,1,8,0,0,0)") + '">08:00</a></li>';
        clock_9am = '<li><a href="' + baseHref.replace(/Date\([^\)]*\)/g, "Date(1970,1,1,9,0,0,0)") + '">09:00</a></li>';
        clock_10am = '<li><a href="' + baseHref.replace(/Date\([^\)]*\)/g, "Date(1970,1,1,10,0,0,0)") + '">10:00</a></li>';
        clock_11am = '<li><a href="' + baseHref.replace(/Date\([^\)]*\)/g, "Date(1970,1,1,11,0,0,0)") + '">11:00</a></li>';
        clock_12am = '<li><a href="' + baseHref.replace(/Date\([^\)]*\)/g, "Date(1970,1,1,12,0,0,0)") + '">12:00</a></li>';
        clock_13pm = '<li><a href="' + baseHref.replace(/Date\([^\)]*\)/g, "Date(1970,1,1,13,0,0,0)") + '">13:00</a></li>';
        clock_14pm = '<li><a href="' + baseHref.replace(/Date\([^\)]*\)/g, "Date(1970,1,1,14,0,0,0)") + '">14:00</a></li>';
        clock_15pm = '<li><a href="' + baseHref.replace(/Date\([^\)]*\)/g, "Date(1970,1,1,15,0,0,0)") + '">15:00</a></li>';
        clock_16pm = '<li><a href="' + baseHref.replace(/Date\([^\)]*\)/g, "Date(1970,1,1,16,0,0,0)") + '">16:00</a></li>';
        clock_17pm = '<li><a href="' + baseHref.replace(/Date\([^\)]*\)/g, "Date(1970,1,1,17,0,0,0)") + '">17:00</a></li>';
        clock_18pm = '<li><a href="' + baseHref.replace(/Date\([^\)]*\)/g, "Date(1970,1,1,18,0,0,0)") + '">18:00</a></li>';
        clock_19pm = '<li><a href="' + baseHref.replace(/Date\([^\)]*\)/g, "Date(1970,1,1,19,0,0,0)") + '">19:00</a></li>';
        clock_20pm = '<li><a href="' + baseHref.replace(/Date\([^\)]*\)/g, "Date(1970,1,1,20,0,0,0)") + '">20:00</a></li>';
        clock_21pm = '<li><a href="' + baseHref.replace(/Date\([^\)]*\)/g, "Date(1970,1,1,21,0,0,0)") + '">21:00</a></li>';
        clock_22pm = '<li><a href="' + baseHref.replace(/Date\([^\)]*\)/g, "Date(1970,1,1,22,0,0,0)") + '">22:00</a></li>';
        clock_23pm = '<li><a href="' + baseHref.replace(/Date\([^\)]*\)/g, "Date(1970,1,1,23,0,0,0)") + '">23:00</a></li>';
        clock_24pm = '<li><a href="' + baseHref.replace(/Date\([^\)]*\)/g, "Date(1970,1,1,0,0,0,0)") + '">00:00</a></li>';

        $(this).append(clock_1am);
        $(this).append(clock_2am);
        $(this).append(clock_3am);
        $(this).append(clock_4am);
        $(this).append(clock_5am);
        $(this).append(clock_6am);
        $(this).append(clock_7am);
        $(this).append(clock_8am);
        $(this).append(clock_9am);
        $(this).append(clock_10am);
        $(this).append(clock_11am);
        $(this).append(clock_12am);
        $(this).append(clock_13pm);
        $(this).append(clock_14pm);
        $(this).append(clock_15pm);
        $(this).append(clock_16pm);
        $(this).append(clock_17pm);
        $(this).append(clock_18pm);
        $(this).append(clock_19pm);
        $(this).append(clock_20pm);
        $(this).append(clock_21pm);
        $(this).append(clock_22pm);
        $(this).append(clock_23pm);
        $(this).append(clock_24pm);

    });
}
setTimeout(function () {
    overrideTimeOptions()
}, 500);