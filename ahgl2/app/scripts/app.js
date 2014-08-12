'use strict';

/**
 * @ngdoc overview
 * @name ahgl2App
 * @description
 * # ahgl2App
 *
 * Main module of the application.
 */
angular
	.module('ahgl2App', [
		'ngAnimate',
		'ngCookies',
		'ngResource',
		'ngRoute',
		'ngSanitize',
		'ngTouch'
	])
	.config(function ($routeProvider) {
		$routeProvider
			.when('/', {
				templateUrl: 'views/main.html',
				controller: 'MainCtrl'
			})
			.otherwise({
				redirectTo: '/'
			});
	});
