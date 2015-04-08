exports.getHome = function (req, res) {
    res.render('generic/home', {
        title: 'Home',
        heading: 'Welcome'
    });
};

