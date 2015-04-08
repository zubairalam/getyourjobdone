angular.module('starter.services', ['ng-cordova'])

/**
 * A simple example service that returns some data.
 */
    .factory('Connections', function () {
        // Might use a resource here that returns a JSON array

        // Some fake testing data
        var connections = [
            {id: 0, name: 'Alvin Luchmun'},
            {id: 1, name: 'Bhavna Pant'},
            {id: 2, name: 'Zubair Alam'},
            {id: 3, name: 'Flora Danes'},
            {id: 4, name: 'Mark Adams'}
        ];

        return {
            all: function () {
                return connections;
            },
            get: function (connectionId) {
                // Simple index lookup
                return connections[connectionId];
            }
        }
    })
    .factory('Jobs', function () {
        // Might use a resource here that returns a JSON array

        // Some fake testing data
        var jobs = [
            {id: 0, name: 'Web Developer in Port Louis'},
            {id: 1, name: 'System Analyst'},
            {id: 2, name: 'Web Designer for a Large Multinational'},
            {id: 3, name: 'Urgent Project Manager Required'}
        ];

        return {
            all: function () {
                return jobs;
            },
            get: function (jobId) {
                // Simple index lookup
                return jobs[jobId];
            }
        }
    });
