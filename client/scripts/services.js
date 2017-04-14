angular.module('movieServices', [])

.factory('Movie', function($http) {
  urlOfSearch = 'data/search.json?';
  urlOfMovie = 'data/movie.json?';

  var db_search = new PouchDB('movie_search', {skip_setup: true});

  return {
    search: function(keyword) {
      return $http({
        method: 'GET',
        url: urlOfSearch + keyword
      });
    },
    searchNext: function(url) {
      return $http({
        method: 'GET',
        url: url
      });
    },
    getMovie: function(id) {
      return $http({
        method: 'GET',
        url: urlOfMovie + id
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
