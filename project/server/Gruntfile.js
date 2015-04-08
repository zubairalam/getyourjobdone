module.exports = function (grunt) {
    'use strict';
    require('load-grunt-tasks')(grunt);
    grunt.initConfig({
        pkg: grunt.file.readJSON('./package.json'),
        devUpdate: {
            main: {
                options: {
                    updateType: 'report', //just report outdated packages
                    reportUpdated: false, //don't report up-to-date packages
                    semver: true, //stay within semver when updating
                    packages: {
                        devDependencies: true, //only check for devDependencies
                        dependencies: true
                    },
                    packageJson: null, //use matchdep default findup to locate package.json
                    reportOnlyPkgs: [] //use updateType action on all packages
                }
            }
        },
        jshint: {
            files: ['./Gruntfile.js', './index.js', './config/**/*.js', './controllers/**/*.js', './data/**/*.js', './helpers/**/*.js', './models/**/*.js', './routes/**/*.js'],
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
                src: ['./bower.json', './package.json', './data/**/*.json']
            }
        },
        nodemon: {
            dev: {
                script: 'index.js',
                options: {
                    args: ['dev'],
                    nodeArgs: ['--debug'],
                    callback: function (nodemon) {
                        nodemon.on('log', function (event) {
                            console.log(event.colour);
                        });
                    },
                    env: {
                        PORT: '5000'
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
        shell: {
            npm : {command: 'npm install', options: {stderr: false, execOptions: {cwd: './'}}},
            compress: {command: 'node compress.js', options: {stderr: false, execOptions: {cwd: 'data'}}},
            drop: {command: 'node drop.js', options: {stderr: false, execOptions: {cwd: 'data'}}},
            export: {command: 'node export.js', options: {stderr: false, execOptions: {cwd: 'data'}}},
            import: {command: 'node import.js', options: {stderr: false, execOptions: {cwd: 'data'}}}
        },
        watch: {
            files: ['<%= jshint.files %>'],
            tasks: ['jshint']
        }
    });

    grunt.registerTask('serve', ['shell:npm', 'nodemon']);
    grunt.registerTask('backup', ['shell:export', 'shell:compress']);
    grunt.registerTask('export', ['shell:export']);
    grunt.registerTask('elasticsearch', ['shell:elasticsearch']);
    grunt.registerTask('import', ['shell:drop', 'shell:import']);
    grunt.registerTask('test', ['jshint', 'jsonlint']);
    grunt.registerTask('update', ['devUpdate']);


};
