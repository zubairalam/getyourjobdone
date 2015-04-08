module.exports = function (grunt) {
    'use strict';
    require('load-grunt-tasks')(grunt);
    grunt.initConfig({
        pkg: grunt.file.readJSON('package.json'),
        devUpdate: {
            main: {
                options: {
                    updateType: 'report',
                    reportUpdated: false,
                    semver: true,
                    packages: {
                        devDependencies: true,
                        dependencies: true
                    },
                    packageJson: null,
                    reportOnlyPkgs: []
                }
            }
        },
        bower: {
            install: {
                options: {
                    targetDir: './public/vendor',
                    layout: 'byType',
                    install: true,
                    verbose: false,
                    cleanTargetDir: false,
                    cleanBowerDir: false,
                    bowerOptions: {}
                }
            }
        },
        jshint: {
            files: ['./Gruntfile.js', './index.js', 'geo.js', './controllers/**/*.js', './helpers/**/*.js', './routes/**/*.js'],
            options: {
                // options here to override JSHint defaults
                globals: {
                    jQuery: true,
                    console: true,
                    module: true,
                    document: true
                }
            }
        },
        jsonlint: {
            files: {
                src: ['./bower.json', './package.json']
            }
        },
        nodemon: {
            dev: {
                script: 'index.js',
                options: {
                    callback: function (nodemon) {
                        nodemon.on('log', function (event) {
                            console.log(event.colour);
                        });
                    },
                    env: {
                        PORT: '3000'
                    },
                    cwd: __dirname,
                    ignore: ['node_modules/**'],
                    ext: 'js,coffee',
                    watch: ['server'],
                    delay: 1000,
                    legacyWatch: true
                }
            }
        },
        watch: {
            files: ['<%= jshint.files %>'],
            tasks: ['jshint']
        }
    });

    grunt.registerTask('serve', ['nodemon']);
    grunt.registerTask('test', ['jshint', 'jsonlint']);
    grunt.registerTask('update', ['devUpdate']);


};
