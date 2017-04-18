var movieControllers = angular.module('movieControllers', []);

movieControllers.controller('SearchController', function($scope, $http, $timeout, Movie) {
  Movie.allMovies().then(function(doc) {
    if (doc.data.items) {
      $scope.results = doc.data.items;
      console.log(doc.data);
    } else {
      $scope.results = [];
    }
  })

  Movie.loadLastData('lastquery').then(function (doc) {
    $scope.query = doc.data;
    $timeout(function () {}, 0);
  }).catch(function (err) {
    $scope.query = '';
    console.log(err);
  });

  $scope.search = function(keyword) {
    Movie.saveLastData('lastquery', keyword);
  };

  $scope.sendSuggestion = function () {
    var data = {
        title: $scope.title,
        plot: $scope.plot
    };
    console.log(data);

    var config = {
        headers : {
            'Content-Type': 'application/json'
        }
    }

    $http.post('http://localhost:8080/_ah/api/suggestion/v1/suggestion',
     data, config)
    .then(function (data, status, headers, config) {
        console.log(data);
        $scope.message = 'Success!';
    })
    .catch(function (data, status, header, config) {
        $scope.message = 'Something went wrong...'
        console.log(status);
        console.log(data);
    });
  };
});

movieControllers.controller('MovieDetailsController', function($scope, $routeParams, Movie) {
  Movie.getMovie($routeParams.movieId).then(function (doc) {
    $scope.movie = doc.data;
  }).catch(function (err) {
    console.log(err);
  });
});
