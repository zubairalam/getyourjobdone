/*
 this will read skills from mongo to redis
 read skills collections
    do this commandline/ in a separate script file
 convert it to json
 store it into redis
*/

var Skills   = require('../models/skill'),
    data     = require('../config/database'),
    redis    = require('../config/redis'),
    async    = require('async');


var readSkillsFromMongo = function (req, res, next) {
    "use strict";


    Skills.find({})
        .select('_id name')
        .exec(function (err, results) {
            if (err) {
                // either no skills is loaded into mongo or some unknown error occurred
                // return empty list like []
                console.log(err);
            }

            // [ {_id: 'lsdkfslfj', name: 'PHPCake'}, {_id: 'lsjflskjf', name: 'Javascript'} ]

            var skills_list = [];

            async.series([
                    function (callback) {
                        redis.del('skills', function (err, value) {
                            if (err) return callback(err);
                            callback(null, 'one');
                        });
                    },
                    function (callback) {
                        results.forEach(function (element, index, array) {
                            // write each to hash skills
                            redis.lpush('skills', JSON.stringify(element), function (err, value) {
                            });
                        });
                        if (err) return callback(err);
                        callback(null, 'two');
                    },
                    function (callback) {
                        // read skills list of json from redis
                        redis.lrange('skills', 0, -1, function (err, results) {
                            if (err) return callback(err);
                            results.forEach(function (value) {
                                skills_list.push(JSON.parse(value));
                            });
                            console.log(skills_list, 'read from redis');
                            callback(null, 'three');
                        });
                    }
                ],
                 function (err, results) {
                    if (err) return next(err);
                    console.log('final');
                    return res.json({skills: skills_list});
                 });
        });
};

module.exports.getSkills = readSkillsFromMongo;

//readSkillsFromMongo();
