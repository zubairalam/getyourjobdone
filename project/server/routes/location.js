var express = require('express'),
    router = express.Router(),
    sprintf = require("sprintf-js").sprintf,
    geoip = require('geoip-lite'),
    get_ip = require('ipware')().get_ip;

module.exports = (function () {
    router.route('/get_ip')
        .get(function(req,res){
        	// var ip_info = get_ip(req),
        	// 	geo = geoip.lookup(ip_info.clientIp);

        	// this is for testing purpose
        	var ip = "207.97.227.239";
        	var geo = geoip.lookup(ip);
        	 
        	var location = sprintf("%s, %s, %s", geo.city, geo.region, geo.country);
        	return res.json({location_info: location});
        });
    return router;
})();
