require('dotenv').config();
var Twitter = require('twitter');
 
var client = new Twitter({
  consumer_key: process.env.TWITTER_CONSUMER_KEY,
  consumer_secret: process.env.TWITTER_CONSUMER_SECRET,
  access_token_key: process.env.TWITTER_ACCESS_TOKEN_KEY,
  access_token_secret: process.env.TWITTER_ACCESS_TOKEN_SECRET
});

var data = require('fs').readFileSync('image.png');

client.post('media/upload', {media: data}, function(error, media, response) {
  if (!error) {

    var status = {
      media_ids: media.media_id_string
    }
    client.post('statuses/update', status, function(error, tweet, response) {
      if (!error) {
        console.log(tweet);
      } else {
        console.log(error);
      }
    });

  } else {
    console.log(error);
  }
});