angular.module('mainApp', [
		'ui.bootstrap',
		'elasticsearch',
		'infinite-scroll'
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
	$scope.busy = false;
	$scope.from = 0;

	$scope.getNextRecipes = function () {
		// $scope.recipes = [];
		$scope.busy = true;
		
		client.search({
			index: 'recipes',
			from: $scope.from,
			size: 120,
			fields: ['name'],
			q: $scope.searchTerms
		})
		.then(getRecipes);
	};

	var getRecipes = function (res) {
		
		res.hits.hits.forEach(function (hit) {
			$scope.recipes.push(hit.fields.name[0]);
		});
		$scope.busy = false;
	};
});
