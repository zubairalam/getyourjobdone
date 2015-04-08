var Skills   = require('../models/skill'),
    data     = require('../config/database'),
    redis    = require('../config/redis');


exports.getSkills = function (req, res) {
	var skills = [];

	redis.lrange('skills', 0, -1, function (err, values) {
		if (values.length === 0) {
			// 'skills' key is not found
			Skills.find({})
				.select('_id name')
				.exec(function (err, results) {

					results.forEach(function (element) {
						redis.lpush('skills', JSON.stringify(element), function (err, value) {

						});
					});

					return res.json({skills: results});

				});
		}

		values.forEach(function (element) {
			skills.push(JSON.parse(element));
		});

		return res.json({skills: skills});
	});
};
