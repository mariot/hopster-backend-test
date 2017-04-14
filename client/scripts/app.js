var myApp = angular.module('myApp', [
  'ngRoute',
  'movieServices',
  'movieControllers'
]);

myApp.config(['$interpolateProvider', function($interpolateProvider) {
  $interpolateProvider.startSymbol('{a');
  $interpolateProvider.endSymbol('a}');
}]);
