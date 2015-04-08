var restClient = require('node-rest-client').Client,
	restcli = new restClient(),
	underscore = require('underscore');


exports.injectSetting = function ( req, res, view, locals ) {
	// don't we need some sort of caching here? - Mark

	restcli.get("http://localhost:5000/api/v1/settings/", function (data, response) {
		module.exports.data = underscore.extend(locals, JSON.parse(data));
		console.log(module.exports.data);
		res.render(view, module.exports.data);
	});
};
