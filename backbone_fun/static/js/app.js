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
      return -tweet.get("timestamp");
    }
  });

  window.TweetView = Backbone.View.extend({
    tagName : 'li',
    className : 'tweet',

    render : function() {
      $(this.el).html(ich.tweetTemplate(this.model.toJSON()));
      return this;
    }
  });

  window.App = Backbone.View.extend({
    el : $('#app'),

    events : {
      'click .tweet' : 'createTweet'
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
      this.$('#tweets').append(view.render().el);
    },
    // Notice that displaying the new tweet isn't even part of this
    // function!  It is all handled by the bound listeners
    createTweet : function() {
      var tweet = this.$('#message').val();
      var username = this.$('#username').val();
      if(tweet) {
        this.tweets.create({
          message : tweet,
          username : username
        });
        this.$('#message').val('');
        window.app.tweets.fetch();
      }
    }
  });

  window.app = new App();

 
   setInterval(
     function() {
      window.app.tweets.fetch();
     },
     2000
   );
  
});
