angular.module('movieServices', [])

.factory('Movie', function($http) {
  urlOfSearch = 'https://hopster-backend-test.appspot.com/_ah/api/suggestion/v1/suggestions?fields=items';

  var db_search = new PouchDB('movie_search', {skip_setup: true});

  return {
    allMovies: function() {
      return $http({
        method: 'GET',
        url: urlOfSearch
      });
    },
    search: function(keyword) {
      return $http({
        method: 'GET',
        url: urlOfSearch
      });
    },
    getMovie: function(id) {
      return $http({
        method: 'GET',
        url: urlOfSearch + id
      });
    },
    saveLastData: function(key, data) {
      var lastresults;
      db_search.get(key).then(function(result) {
        lastresults = {
            _id: result._id,
            data: data,
            _rev: result._rev
        };

        db_search.put(lastresults, function callback(err, result) {
            if (!err) {
                console.log(result);
            } else {
                console.log(err);
            }
        });
      })
      .catch(function (err) {
        console.log(err);
        lastresults = {
            _id: key,
            data: data
        };

        db_search.put(lastresults, function callback(err, result) {
            if (!err) {
                console.log(result);
            } else {
                console.log(err);
            }
        });
      });
    },
    loadLastData: function(key) {
      return db_search.get(key);
    }
  };
});
