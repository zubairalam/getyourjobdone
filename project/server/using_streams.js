var liner = require('./liner'),
    fs = require('fs'),
    source = fs.createReadStream('./recipeitems-latest.json'),
    elasticsearch = require('elasticsearch'),
    esClient = elasticsearch.Client({
        host: 'localhost:9200'
    });

source.pipe(liner);
var recipes = [];

liner.on('readable', function () {
    var line;
    var counter = 0;
    while (line = liner.read()) {
        line = JSON.parse(line);
        recipe = {
            id: line._id.$oid, // Was originally a mongodb entry
            name: line.name,
            source: line.source,
            url: line.url,
            recipeYield: line.recipeYield,
            ingredients: line.ingredients.split('\n'),
            prepTime: line.prepTime,
            cookTime: line.cookTime,
            datePublished: line.datePublished,
            description: line.description
        };

        recipes.push({index: {_index: 'recipes', _type: 'recipe', _id: recipe.id}});
        recipes.push(recipe);

        if (recipes.length === 2000) {
            esClient.bulk({
                body: recipes
            }, function (err, data) {
                console.log(data.length);
                recipes = [];
            });
        }

        /*esClient.bulk({
            body: recipes
        }, function (err, data) {
            console.log(data);
        });*/

        /*esClient.create({
            index: 'recipes',
            type: 'recipe',
            id: recipe.id,
            body: recipe
        }, function (error, response) {
            console.log(response);
        });*/
    }
});
