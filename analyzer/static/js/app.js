var parserApp = angular.module('parserApp', ['ngRoute', 'ngSanitize', 'angular-loading-bar', 'ui.bootstrap', 'ngAnimate']);



parserApp.config(function($routeProvider) {
    $routeProvider
    .when("/", {
        template : parserTmp,
        controller : "collectionAppController"
    })
    .when("/admin", {
        template : adminTmp,
        controller : "administratorAppController"
    })
    .when("/settings", {
        template : settingsTmp,
        controller : "settingsAppController"
    })
    .when("/admin/create", {
        template : adminCreateTmp,
        controller : "administratorCreateAppController"
    })
    .when("/admin/profile", {
        template : adminCreateTmp,
        controller : "administratorProfileAppController"
    });
});

angular.module('parserApp')
    .config(function($httpProvider) {
        $httpProvider.defaults.xsrfCookieName = 'csrftoken';
        $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    });

angular.module('parserApp')
    .config(function(cfpLoadingBarProvider) {
        cfpLoadingBarProvider.includeSpinner = true;
    });

parserApp.controller("collectionAppController", function($scope, $location, $http, cfpLoadingBar) {
    $scope.start = function () {
        cfpLoadingBar.start();
    };

    $scope.complete = function () {
        cfpLoadingBar.complete();
    };

    $scope.count_paginator = function(num) {
        range = [];
        for (var i = 1; i <= num; ++i){
            range.push(i)
        }
        return range
    };

    $scope.get_collection = function (page) {
        var page_number = page || 1;
        $http.get('api/v1.0/collections/?page='+page_number)
        .then(function(response) {
            $scope.collections = response.data.results;
            $scope.total_pages = response.data.total_pages;
            $scope.collection_count = response.data.count;
            $scope.current_page = response.data.current_page;
        });
    };

    $scope.get_collection();
});

parserApp.controller("administratorAppController", function($scope, $location, $http, cfpLoadingBar) {

    $scope.start = function () {
        cfpLoadingBar.start();
    };

    $scope.complete = function () {
        cfpLoadingBar.complete();
    };

    $scope.count_paginator = function(num) {
        range = [];
        for (var i = 1; i <= num; ++i){
            range.push(i)
        }
        return range
    };

    $scope.get_users = function (page) {
        var page_number = page || 1;
        $http.get('api/v1.0/users/?page='+page_number)
        .then(function(response) {
            $scope.users = response.data.results;
            $scope.total_pages = response.data.total_pages;
            $scope.users_count = response.data.count;
            $scope.current_page = response.data.current_page;
        });
    };

    $scope.get_users();

    $scope.get_email = function (user) {
        $http.patch('api/v1.0/users/'+user.id+'/get_email/', {"is_get_email": user.is_get_email } )
    }


});

parserApp.controller("administratorProfileAppController", function($scope, $location, $http, $window, cfpLoadingBar) {
    $scope.$location = $location;
    $scope.start = function () {
        cfpLoadingBar.start();
    };

    $scope.complete = function () {
        cfpLoadingBar.complete();
    };
    $scope.user = {};
    $scope.get_current_user = function () {
        $http.get('api/v1.0/users/current_user')
        .then(function(response) {
            $scope.user = response.data;
        }, function(response) {

        });
    };
    $scope.get_current_user();
    $scope.save = function () {
        $http.put('api/v1.0/users/'+$scope.user.id+'/', $scope.user)
            .then(function(response) {
                $scope.status = response.status;
                $scope.data = response.data;
                $scope.error_username = false;
                $scope.error_password = false;
                $scope.error_email = false;
                $scope.error_password2 = false;
                var host = $window.location.host;
                var landingUrl = "http://" + host + "/accounts/logout/";
                $window.location.href = landingUrl;
            }, function(response) {
                console.log(response.data);
                if (response.data.username){
                    $scope.error_username = response.data.username[0];
                }else{
                    $scope.error_username = false;
                }
                if (response.data.password){
                    $scope.error_password = response.data.password[0];
                }else{
                    $scope.error_password = false;
                }
                if (response.data.password2){
                    $scope.error_password2 = response.data.password2[0];
                }else{
                    $scope.error_password2 = false;
                }
                if (response.data.email){
                    $scope.error_email = response.data.email[0];
                }else{
                    $scope.error_email = false;
                }
                $scope.status = response.status;
            });
    };
});

parserApp.controller("administratorCreateAppController", function($scope, $location, $http, cfpLoadingBar) {
    $scope.$location = $location;
    $scope.start = function () {
        cfpLoadingBar.start();
    };

    $scope.user = {
        // first_name: ''
    };
    $scope.save = function () {
        $http.post('api/v1.0/users/', $scope.user)
            .then(function(response) {
                $scope.status = response.status;
                $scope.data = response.data;
                $scope.error_username = false;
                $scope.error_password = false;
                $scope.error_email = false;
                $scope.error_password2 = false;
            }, function(response) {
                console.log(response.data);
                if (response.data.username){
                    $scope.error_username = response.data.username[0];
                }else{
                    $scope.error_username = false;
                }
                if (response.data.password){
                    $scope.error_password = response.data.password[0];
                }else{
                    $scope.error_password = false;
                }
                if (response.data.password2){
                    $scope.error_password2 = response.data.password2[0];
                }else{
                    $scope.error_password2 = false;
                }
                if (response.data.email){
                    $scope.error_email = response.data.email[0];
                }else{
                    $scope.error_email = false;
                }
                $scope.status = response.status;
            });
    };
    $scope.complete = function () {
        cfpLoadingBar.complete();
    };
});

parserApp.controller("currentLocationAppController", function($scope, $location, $http, cfpLoadingBar) {
    $scope.$location = $location;
});

parserApp.controller("settingsAppController", function($scope, $location, $http, cfpLoadingBar) {
    $scope.$location = $location;
    jQuery('.datepicker-plugin').datepicker({
        weekStart: 1,
        startView: 2,
        minViewMode: 2,
        maxViewMode: 2,
        clearBtn: true,
        language: "ru",
        autoclose: true,
        todayHighlight: true,
        format: "yyyy-mm-dd"
    });
    $http.get('api/v1.0/settings')
    .then(function(response) {
            $scope.settings_site = response.data.results[0];
        }, function(response) {

        });
    $scope.save_settings = function () {
        // if($scope.settings_site.date_from)
        // typeof($scope.settings_site.date_from);
        // console.log(typeof($scope.settings_site.date_from));
        // console.log($scope.settings_site.date_from);
        if ($scope.settings_site.date_from.length === 0){
            $scope.settings_site.date_from = null;
        }

        $http.patch('api/v1.0/settings/1/', $scope.settings_site)
        .then(function(response) {
            $scope.alerts.push({msg: 'Saved!'});
        }, function(response) {
            $scope.alerts.push({msg: 'ERROR'});
        });
    };

    $scope.alerts = [];

    $scope.closeAlert = function(index) {
        $scope.alerts.splice(index, 1);
    };

    $http.get('api/v1.0/status')
        .then(function(response) {
            $scope.status = response.data.results;
        }, function(response) {

        });

    $scope.site = {};

    $scope.save_status = function () {
        $http.patch('api/v1.0/status/save_all/', $scope.status)
        .then(function(response) {
            $scope.alerts.push({msg: 'Saved!'});
        }, function(response) {
            $scope.alerts.push({msg: 'ERROR'});
        });
    };

    $scope.word_input = {
        'word': ''
    };

    $http.get('api/v1.0/stopword')
    .then(function(response) {
            $scope.stopwords = response.data.results;
        }, function(response) {

        });

    $scope.save_word = function () {
        $http.post('api/v1.0/stopword/', $scope.word_input)
        .then(function(response) {
            $scope.stopwords.push(response.data);
            $scope.word_input = {'word': ''}
        }, function(response) {
            $scope.alerts.push({msg: response.data.word});
        });
    };

    $scope.delete_word = function (word) {
        $http.delete('api/v1.0/stopword/' + word.id + '/')
        .then(function(response) {
            var index = $scope.stopwords.indexOf(word);
            console.log(index);
            delete $scope.stopwords.splice(index, 1);
        }, function(response) {
            $scope.alerts.push({msg: response.data.word});
        });
    }

});