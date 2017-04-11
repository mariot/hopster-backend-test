var movieControllers = angular.module('movieControllers', []);

movieControllers.controller('SearchController', function($scope, $timeout, Movie) {
  Movie.loadLastData('lastquery').then(function (doc) {
    $scope.query = doc.data;
  }).catch(function (err) {
    $scope.query = '';
    console.log(err);
  });

  Movie.loadLastData('lastresults').then(function (doc) {
    $scope.results = doc.data.movies.items;

    $scope.resultData = doc.data;
    $scope.loadButton = showLoadButton();

    $timeout(function () {}, 0);
  }).catch(function (err) {
    console.log(err);
  });

  $scope.search = function(keyword) {
    Movie.search(keyword).then(function (doc) {
      $scope.results = doc.data.movies.items;

      $scope.resultData = doc.data;
      $scope.loadButton = showLoadButton();

      Movie.saveLastData('lastquery', keyword);
      Movie.saveLastData('lastresults', doc.data);

    }).catch(function (err) {
      console.log(err);
    });
  }

  $scope.loadMoreData = function() {
    if ($scope.resultData.movies.next) {
      Movie.searchNext($scope.resultData.movies.next).then(function (doc) {
        $scope.resultData.movies.items = $scope.resultData.movies.items
          .concat(doc.data.movies.items);
        $scope.results = $scope.results.concat(doc.data.movies.items);
      }).catch(function (err) {
        console.log(err);
      });
    }

    $scope.loadButton = showLoadButton();

    Movie.saveLastData('lastresults', $scope.resultData);
  }

  function showLoadButton() {
    if ($scope.resultData.movies.next) {
      return true;
    }
    return false;
  }
});

movieControllers.controller('MovieDetailsController', function($scope, $routeParams, Movie) {
  Movie.getArtist($routeParams.movieId).then(function (doc) {
    $scope.artist = doc.data;
  }).catch(function (err) {
    console.log(err);
  });
});
