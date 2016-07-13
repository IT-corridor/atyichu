var app = angular.module('app.main', [
    'ngAnimate',
    'ngAria',
    'ngTouch',
    'ui.bootstrap',
    'pascalprecht.translate',
    'constants',
    'app.route',
    'auth.services',
    'navbar',
    'footer',
    'alert',
    'selfie',
    'grid',
]);
app.factory('httpRequestInterceptor', function () {
    return {
        request: function (config) {
            config.headers['X-Requested-With'] = 'XMLHttpRequest';
            return config;
        }
    };
});
app.run(function($rootScope) {
    $rootScope.site = 'Atyichu';
    $rootScope.THEME = '/static/theme/';
});
app.config(function ($httpProvider) {
    $httpProvider.interceptors.push('httpRequestInterceptor');
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.useApplyAsync(true);
});
app.config(function($resourceProvider) {
  $resourceProvider.defaults.stripTrailingSlashes = false;
});
app.config(['$locationProvider', function($locationProvider){
    //$locationProvider.html5Mode(true);
    $locationProvider.hashPrefix('!');
}]);

app.config(['$translateProvider', function ($translateProvider) {
    $translateProvider.translations('en', {
        'COMMON': {
            'HOME': {
                'TITLE': 'Welcome!',
            },
        },
        'AUTHENTICATION': {
            'REQUIRED': 'Please, log in.',
            'SUCCESS': 'Welcome back!',
            'ERROR': 'Authentication error',
            'LOGOUT': 'Good by',

        },
        'NAVBAR': {
            'MODAL': {
                'CLOSE': 'Close',
                'TITLE': 'Sign in',
                'USERNAME': 'Username',
                'PASSWORD': 'Password',
                'ENTER': 'Enter',
                'FORGOT': 'I forgot my password',
            },
            'TOGGLE_NAV': 'Toggle Navigation',
            'LOGGED': 'You logged as {{username}}',
            'PROFILE': 'My profile',
            'STORE': 'My store',
            'LOGOUT': 'Logout',
            'SIGN': 'Sign',
            'SIGN_IN': 'Sign in',
        },
        'STORE': {
            'CREATE': {
                'HEADER': 'Create a store',
                'ALREADY': 'You already have a store',
                'SUCCESS': 'Store has been created',
            },
            'UPDATE': {
                'HEADER': 'Edit your store',
                'SUCCESS': 'Your store information has been updated.',
                'FAIL': 'Fail trying update.',
                'UPDATE_PHOTO': 'Update photo',
                'UPDATE_DATA': 'Update data',
            },
            'FORM': {
                'BRAND_NAME': 'Brand name',
                'STATE': 'State',
                'CITY': 'City',
                'DISTRICT': 'District',
                'STREET': 'Street',
                'BUILD_NAME': 'Building name',
                'BUILD_NO': 'Building number',
                'APT': 'Apartments',
                'PHOTO': 'Photo',
                'CROP': 'Crop',
                'SUBMIT': 'Submit',
                'CANCEL': 'Cancel',
                'WAIT': 'Please wait...',
                'LOCATION': 'Location',
                'NO_PHOTO': 'No photo',
            },
            'MYs': {
                'HEADER': 'Your store overview',
            }
        }
    });

    $translateProvider.translations('zh', {
        'COMMON': {
            'HOME': {
                'TITLE': 'Welcome!',
            },
        },
        'AUTHENTICATION': {
            'REQUIRED': 'Please log in.',
            'SUCCESS': 'Welcome back!',
            'ERROR': 'Authentication error',
            'LOGOUT': 'Good by',

        },
        'NAVBAR': {
            'MODAL': {
                'CLOSE': 'Close',
                'TITLE': 'Sign in',
                'USERNAME': 'Username',
                'PASSWORD': 'Password',
                'ENTER': 'Enter',
                'FORGOT': 'I forgot my password',
            },
            'TOGGLE_NAV': 'Toggle Navigation',
            'LOGGED': 'You logged as {{username}}',
            'PROFILE': 'My profile',
            'STORE': 'My store',
            'CHANGE_PASSWORD': 'Change password',
            'LOGOUT': 'Logout',
            'SIGN': 'Sign',
            'SIGN_IN': 'Sign in',
        },
        'STORE': {
            'CREATE': {
                'HEADER': 'Create a store',
                'ALREADY': 'You already have a store',
            },
            'UPDATE': {
                'HEADER': 'Update your store',
                'SUCCESS': 'Your store information has been updated.',
                'FAIL': 'Fail trying update.',
                'UPDATE_PHOTO': 'Update photo',
                'UPDATE_DATA': 'Update data',
            },
            'FORM': {
                'BRAND_NAME': 'Brand name',
                'STATE': 'State',
                'CITY': 'City',
                'DISTRICT': 'District',
                'STREET': 'Street',
                'BUILD_NAME': 'Building name',
                'BUILD_NO': 'Building number',
                'APT': 'Apartments',
                'PHOTO': 'Photo',
                'CROP': 'Crop',
                'SUBMIT': 'Submit',
                'CANCEL': 'Cancel',
                'WAIT': 'Please wait...',
                'LOCATION': 'Location',
                'NO_PHOTO': 'No Photo',
            },
            'MY': {
                'HEADER': 'Your store overview',
            }
        }
    });

  $translateProvider.preferredLanguage('zh');
}]);