angular.module('mainApp', [
		'ui.bootstrap',
		'elasticsearch',
		])

.service('client', function (esFactory) {
	return esFactory({
		host: 'localhost:9200'
	});
})

.filter('range', function () {
	return function (totalButtons, range) {
		var range = parseInt(range);
		for (var i=0; i<range; i+=1) {
			totalButtons.push(i+1);
		}
		return totalButtons;
	}
})

.controller('recipeCtrl', function ($scope, client, esFactory) {
	$scope.recipes = [];
	$scope.searchTerms = '';
	$scope.totalPages = 0;

	$scope.getNextRecipes = function () {
		$scope.recipes = [];
		client.search({
			index: 'recipes',
			from: 0,
			size: 20,
			fields: ['name'],
			q: $scope.searchTerms
		})
		.then(getRecipes);	
	};

	var getRecipes = function (res) {
		res.hits.hits.forEach(function (hit) {
			$scope.recipes.push(hit.fields.name[0]);
		});
		if (undefined != res) {
			var totalResults = res.hits.total || 0;
			var totalPages = parseInt(totalResults/20) + ((totalResults%20)?1:0);
			$scope.totalPages = totalPages>10?10:totalPages;
		}
	};

	$scope.getPage = function (page) {
		var page = parseInt(page) || 0;
		if (page === 0) {
			return page;
		}
		var start = (page-1)*20;
		var end = (page)*20;
		console.log(start,end);
		$scope.recipes = [];
		client.search({
			index: 'recipes',
			from: start,
			size: 20,
			fields: ['name'],
			q: $scope.searchTerms
		})
		.then(getRecipes);	
	} 
});
