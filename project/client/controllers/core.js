exports.homeController = function (req, res) {
    res.render('core/home', { title: 'Hey', message: 'Hello there!'});
};
