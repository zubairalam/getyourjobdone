// crawls a particular job portal
// stores jobs in mongo and at the same time index that job inside elasticsearch
// done!!
// do above using schedule job of celery

var request = require('request')
    , $ = require('cheerio')
    , RSVP = require('rsvp')
    , _ = require('lodash')
    , tough = require('tough-cookie')
    , xpath = require('xpath')
    , dom = require('xmldom').DOMParser
    ;

request = request.defaults({
    headers: {
      'jar': true,
      'Referer' : 'http://www.thomasnet.com/browse',
      'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.115 Safari/537.36'
    }
});


var stripHTML = function (text) {
    return text.replace(/(<([^>]+)>)/ig,"");
}

var requestPromise = function (link) {
    return new RSVP.Promise(function (resolve, reject) {
        request.get(link)
            .on('error', function (error) {
                return reject(error);
            })
            .on('response', function (response) {
                var body = '';
                response.on('data', function (chunk) {
                    body += chunk;
                });
                response.on('end', function () {
                    console.log('here')
                    resolve({body: body, response: response});
                });
            });
    });
};

var stripHTML = function (text) {
    return text.replace(/(<([^>]+)>)/ig,"");
}

var store_jobpages = function (response) {
    var body = $.load(response);
    var rows = body(".srp_container div[type='tuple'].row");
    var jobs = [];
    rows.map(function (index, row) {
        var job = {};
        job['href'] = $(row).find('a[count].content').attr('href') || '';
        job['title'] = $(row).find('a[count].content span.desig').text() || '';
        job['org'] = $(row).find('a[count].content span.org').text() || '';
        job['exp'] = stripHTML($(row).find('a[count].content span.exp').text()) || '';
        job['loc'] = stripHTML($(row).find('a[count].content span.loc').text()) || '';
        job['skills'] = stripHTML($(row).find('a[count].content span.skill').text()) || '';
        job['desc'] = stripHTML($(row).find('a[count].content span.desc').text()) || '';
        jobs.push(job);
    });

    return jobs;
}

var getSubPages = function (response) {
    var body = $.load(response);
    var text = body("h1 span.cnt[title]").text();
    var pattern = /\d+/g;
    var nums = text.match(pattern);
    
}

var fetchJobUrls = function () {
    return new RSVP.Promise(function (resolve, reject) {
        requestPromise('http://jobsearch.naukri.com/networking-jobs')
            .then(function (obj) {
                
                if (!obj.body || obj.response.statusCode!=200) {
                    return reject({message: 'not found'});
                }
                
                var jobs = store_jobpages(obj.body);
                
                // save these to db


            })
    })
};

fetchJobUrls()
    .then(function(result){
        console.log('ended');
    }, function (error) {
        console.log(error);
    });
