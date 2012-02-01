$(function() {
  var oldSync = Backbone.sync;

  Backbone.sync = function(method, model, success, error) {
    var newSuccess = function(resp, status, xhr) {
      if(xhr.statusText === "CREATED") {
        var location = xhr.getResponseHeader('Location');
        return $.ajax({
          url : location,
          success : success
        });
      }
      return success(resp);
    };
    return oldSync(method, model, newSuccess, error);
  };

  window.Tweet = Backbone.Model.extend({
    url : function() {
      return this.get('resource_uri') || this.collection.url;
    }
  });

  window.Tweets = Backbone.Collection.extend({
    initialize: function() {
            _.bindAll(this, 'url');
    },
    
    url : function() { 
      qs = ''; //typeof(this.first() == "object")?("?last_time=" + this.first().get("timestamp")):'';
      return TWEET_API + qs;
    },

    parse : function(data) {
      return data.objects;
    },
    comparator : function(tweet) {
      return tweet.get("timestamp");
    }
  });

  window.TweetView = Backbone.View.extend({
    tagName : 'li',
    className : 'tweet',

    render : function() {
      $(this.el).html(ich.tweetTemplate(this.model.toJSON()));
      Backbone.ModelBinding.bind(this);
      return this;
    }
  });

  window.App = Backbone.View.extend({
    el : $('#app'),

    events : {
      'click .button' : 'createTweet',
      'click .deleteme' : 'deleteTweet'
    },

    initialize : function() {
      _.bindAll(this, 'addOne', 'addAll', 'render');
      this.tweets = new Tweets();
      this.tweets.bind('add', this.addOne);
      this.tweets.bind('refresh', this.addAll);
      this.tweets.bind('all', this.render);
      this.tweets.fetch();
    },
    addAll : function() {
      $("#tweets").empty();
      this.tweets.each(this.addOne);
    },
    addOne : function(tweet) {
      var view = new TweetView({
        model : tweet
      });
      this.$('#tweets').prepend(view.render().el);
    },
    // Notice that displaying the new tweet isn't even part of this
    // function!  It is all handled by the bound listeners
    createTweet : function() {
      var tweet = this.$('#message').val();
      var username = this.$('#username').val();
      if (tweet) {
        this.tweets.create({
          message : tweet,
          username : username
        });
        this.$('#message').val('');
        window.app.tweets.fetch();
      }
    },

    deleteTweet : function(event) {
      alert("Delete Tweet " + event.target.id.split('_')[1]);
      window.app.tweets.fetch();
    }
  });

  window.app = new App();

  // Didn't know how to bind this internally like the click since it requires
  // some information about what's going on.
  // If it's a return key, submit the tweet...
  $('#message').bind('keypress', function(event) {
    if (event.which == 13) {
      app.createTweet();
    }
  }); 
   
  // I would like to find a better way of doing this...
  setInterval(
    function() {
      window.app.tweets.fetch();
    },
    10000
  );  
});
