exports.homeController = function (req, res) {
    //res.render('core/home', { title: 'Hey', message: 'Hello there!'});
    res.render('reactComponents/index', { title: 'Hey', message: 'Hello there!'});
};

exports.CommentsController = function (req, res) {
    var data = [
        {author: "Pete Hunt", text: "This is one comment"},
        {author: "Zubair Alam", text: "Let's see how react is reactive"},
        {author: 'Anonymous', text: 'World is temporary.'},
        {author: 'Nodeman', text: 'Working superb'},
        {author: 'ABC', text: 'some random text'},
        {author: "Jordan Walke", text: "This is *another* comment"}
    ];
    res.json({data: data});
};

