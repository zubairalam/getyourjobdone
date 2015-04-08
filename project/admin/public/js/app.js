(function () {
    "use strict";

    var app = angular.module('myApp', ['ng-admin']);

    app.controller('main', function ($scope, $rootScope, $location) {
        $rootScope.$on('$stateChangeSuccess', function () {
            $scope.displayBanner = $location.$$path === '/dashboard';
        });
    });

    app.config(function (NgAdminConfigurationProvider, Application, Entity, Field, Reference, ReferencedList, ReferenceMany) {
        var totalCount;

        function truncate(value) {
            if (!value) {
                return '';
            }

            return value.length > 50 ? value.substr(0, 50) + '...' : value;
        }

        function totalItems(response) {
            return 9999999999; // fix for only using infinite pagination at this stage.
        }



        function pagination(page, maxPerPage) {
            return {
                skip: (page - 1) * maxPerPage,
                limit: maxPerPage
            }
        }

        var country = new Entity('countries');
        country
            .label('Countries')
            .order(1)
            .dashboard(null)
            .totalItems(totalItems)
            .pagination(pagination)
            .infinitePagination(true)
            .filterQuery(function(searchQuery) {
                return {
                    query: {"name":"~"+searchQuery}
                };
            })
            .titleCreate('Create country')
            .titleEdit('Edit country')
            .addField(new Field('_id')
                .label('ID')
                .type('number')
                .identifier(true)
                .edition('read-only')
        )
            .addField(new Field('name')
                .label('Name')
                .edition('editable')
                .truncateList(truncate)
        )
            .addField(new Field('alpha2')
                .label('Alpha-2')
        )
            .addField(new Field('alpha3')
                .label('Alpha-3')
        )
            .addField(new Field('formal_name')
                .label('Formal Name')
                .truncateList(truncate)
        )
            .addField(new Field('slug')
                .label('Slug')
                .edition('read-only')
        );


        var emailTemplate = new Entity('emailtemplates');
        emailTemplate
            .label('Email Templates')
            .order(1)
            .dashboard(null)
            .perPage(10)
            .pagination(pagination)
            .infinitePagination(false)
            .titleCreate('Create an email template')
            .titleEdit('Edit an email template')
            .description('Lists all the email templates with a simple pagination')
            .addField(new Field('_id')
                .label('ID')
                .type('number')
                .identifier(true)
                .edition('read-only')
        )
            .addField(new Field('name')
                .label('Name')
                .edition('editable')
                .truncateList(truncate)
        )
            .addField(new Field('from')
                .label('From')
        )
            .addField(new Field('to')
                .label('to')
        )
            .addField(new Field('subject')
                .label('subject')
        )
            .addField(new Field('text')
                .label('text')
        )
            .addField(new Field('html')
                .label('html')
                .type('wysiwyg')
        )
            .addField(new Field('slug')
                .label('Slug')
        );

        var role = new Entity('roles');
        role
            .label('Roles')
            .order(1)
            .dashboard(null)
            .pagination(pagination)
            .infinitePagination(false)
            .titleCreate('Create a role')
            .titleEdit('Edit a role')
            .description('Lists all the roles with a simple pagination')
            .addField(new Field('_id')
                .label('ID')
                .type('number')
                .identifier(true)
                .edition('read-only')
        )
            .addField(new Field('name')
                .label('Name')
                .edition('editable')
        )
            .addField(new Field('slug')
                .label('Slug')
                .edition('editable')
        );

        var skill = new Entity('skills');
        skill
            .label('Skills')
            .order(2)
            .dashboard(null)
            .infinitePagination(true)
            .titleCreate('Create a skill')
            .titleEdit('Edit a skill')
            .description('Lists all the skills with a simple pagination')
            .addField(new Field('_id')
                .label('ID')
                .type('number')
                .identifier(true)
                .edition('read-only')
        )
            .addField(new Field('name')
                .label('Name')
                .edition('editable')
        )
            .addField(new Field('slug')
                .label('Slug')
                .edition('editable')
        );

        var app = new Application('firethoughts Admin')
            .baseApiUrl('http://localhost:5000/api/v1/')
            .addEntity(country)
            .addEntity(emailTemplate)
            .addEntity(role)
            .addEntity(skill);

        NgAdminConfigurationProvider.configure(app);
    })
})();