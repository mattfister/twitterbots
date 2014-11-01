// This is a twitter bot that attempts to connect two people talking about the same trend.
// Every 15 minutes it picks a trend, announces what it's thinking about.
// Then it listens for 100 tweets about that trend. Once this is done it uses those
// 100 tweets to construct a new tweet via a Markov chain of those inputs. It tweets this.
// Then it picks two of the people who it had listened to and tries to connect them to each other
// The bot wins if those two people start talking.

// Created by Matthew Fister (@mattjfister)

// Thanks to Darius Kazemi (@tinysubversions) for this article and starter code http://tinysubversions.com/2013/09/how-to-make-a-twitter-bot/
// And Jason Bury for this Markov chain code http://www.soliantconsulting.com/blog/2013/02/draft-title-generator-using-markov-chains
// ttezel too, for twitjs https://github.com/ttezel/twit

// Every 15 minutes it picks a trend, announces what it's thinking about

var Twit = require('twit');
var fs = require('fs');

var consumerKey;
var consumerSecret;
var accessToken;
var accessTokenSecret;

// Read in our twitter keys from a text file called twitterKeys.txt (that should
// be located next to this file). You'll have to set it up so that it's formatted
// consumerKey
// consumerSecret
// accessToken
// accessTokenSecret
// The file is pretty raw, just each of those on a new line. Four lines total.
fs.readFile("twitterKeys.txt", "ascii", function(err, data) {
    if (err) {
	return console.log(err);
    }
    var splitData = data.split("\n");
    consumerKey = splitData[0].trim();
    consumerSecret = splitData[1].trim();
    accessToken = splitData[2].trim();
    accessTokenSecret = splitData[3].trim();

});

var T;
// Create our twitter client (we wait a second to give our file enough time to load
setTimeout( function() {
    T = new Twit({
	consumer_key:         consumerKey, 
	consumer_secret:      consumerSecret,
	access_token:         accessToken,
	access_token_secret:  accessTokenSecret
    }, 1000);
});


// These are all of our state variables to keep track of what we're doing
var terminals = {}; // map of words:true/false if each word in our markov chains is true or false
var startwords = []; // start word options for our markov chains
var wordstats = {}; // a map of words to words that follow it
var users = []; // a list of all the users we listened to
var user1 = ""; // one of the users that we selected
var user2 = ""; // the other user that we selected
var trends = []; // the top 10 trends in the US

// Resets our state (all the above variables)
function resetCorpus() {
    terminals = {};
    startwords = [];
    wordstats = {};
    users = [];
    user1 = "";
    user2 = "";
    trends = [];
}

// Chooses a good trend from the trends. Right now this just filters out ? and & from the trends
// because those seem to jack it up because they're an url parameter component
var chooseTrend = function() {
    var goodTrend = false;
    while (!goodTrend) {
	trend = choice(trends);
	if (trend.indexOf("&") >= 0) {
	    continue;
	} else if (trend.indexOf("?") >= 0) {
	    continue;
	} else {
	    return trend; 
	}
	
    }
}

// Filters out tweets that start with RT, these result in us trying to generate RTs which is a fool's game
var passesFilter = function(tweet) {
    var words = tweet.split(' ');
    if (words[0].toUpperCase() == "RT") {
	return false;
    } else {
	return true;
    }
}

// Adds a tweet to our Markov chain state, keeping track of how
function addTweet(tweet) {
    var words = tweet.split(' ');
    terminals[words[words.length-1]] = true;
    startwords.push(words[0]);
    for (var j = 0; j < words.length - 1; j++) {
        if (wordstats.hasOwnProperty(words[j])) {
            wordstats[words[j]].push(words[j+1]);
        } else {
            wordstats[words[j]] = [words[j+1]];
        }
    }
}

// Adds a user to the list of users we're keeping track of
function addUser(user) {
    users.push(user);
}

// Posts a tweet to our timeline
function postTweet(tweet) {
    T.post('statuses/update', {status: tweet}, function(err, data, reply) {
    });
}

// Given an array, returns a random element
var choice = function (a) {
    var i = Math.floor(a.length * Math.random());
    return a[i];
};

// Assuming our corpus has been generated, creates a tweet of at least size minLength
// and no bigger than 140 characters
var markovTweet = function(minLength) {
    word = choice(startwords);
    var title = [word];
    console.log("startWord: " + word);
    while (wordstats.hasOwnProperty(word)) {
        var next_words = wordstats[word];
	console.log("nextWords: " + next_words);
        word = choice(next_words);
	console.log("nextWord: " + word);
        title.push(word);
        if (title.length > minLength && terminals.hasOwnProperty(word)) break;
    }
    if (title.length < minLength || title.length > 140) return markovTweet(minLength);
    return title.join(' ');
};

// Chooses two random distinct users from all the tweets we listened to.
// These are the ones that we're going to try to connect
function chooseUsers() {
    user1 = choice(users);
    user2 = user1;
    while (user2 == user1) {
	user2 = choice(users);
    }
    console.log("Chose users: user1: " + user1 + " user2: " + user2);
}

// Follow our two special users
function followUsers() {
    T.post('friendships/create', { id: user1 }, function(err, data, reply) {
    });
    T.post('friendships/create', { id: user2 }, function(err, data, reply) {
    });
}

function postAboutTopic(topic) {
    var generalPost = "Thinking about " + topic;
    postTweet(generalPost);
}

// Keep track of if we're already processing tweets, so we don't start again
var processing = false;

// Listen for this many tweets before we start posting
var numToListenTo = 100;

// This guy does all the magic. Picks a trend in the US, listens to a bunch of tweets about it,
// generates a new tweet about it based on a Markov chain of all the tweets we listened to,
// follows two of the people who tweeted about it, then tries to connect them (phew!)
function connectorPost() {
    if (processing == true ) {
	console.log("Still processing...");
	return;
    }

    processing = true;
    
    console.log("\n");
    console.log("\n");

    resetCorpus();
    
    console.log("Getting trends");
    T.get('trends/place', {id: '23424977'}, function(err, reply) {
	if (err != null) {
	    console.log(err);
	}
	
	for (i = 0; i < 10; i++ ) {
	    console.log("Got trend: " + reply[0].trends[i].name);
	    trends.push(reply[0].trends[i].name)
	}
	console.log("Trends: " + trends);
	topic = chooseTrend();
	console.log("Selected trend: " + topic);

	postAboutTopic(topic);
	
	console.log("Starting listening");
	var stream = T.stream('statuses/filter', { track: topic })
	
	var numAdded = 0;
	var startListeningTime = Date.now();
	stream.on('tweet', function(tweet) {
	    // console.log("screen_name: " + tweet.screen_name);
	    var currentTime = Date.now();
	    var timePassed = currentTime - startListeningTime;
	    console.log("Been listening for " + timePassed/1000.0 + "s");
	    if (timePassed > 60000*5 && numAdded < numToListenTo/3) { // If we've been listening for more than 5 minutes, and we don't have a third as many tweets as we need, bail
		stream.stop();
		processing = false;
		console.log("Abandoning topic: " + topic);
	    }
	    if (passesFilter(tweet.text)) {
		console.log("Adding tweet " + numAdded + " by user: " + tweet.user.screen_name);
		console.log("text: " + tweet.text);
		addTweet(tweet.text);
		addUser(tweet.user.screen_name);
		numAdded++;
		console.log("\n");
		if (numAdded >= numToListenTo) {
		    var newStatus = markovTweet();
		    console.log("Status: " + newStatus);
		    postTweet(newStatus);
		    stream.stop();
		    chooseUsers();
		    followUsers();
		    var connectionStatus = "@" + user1 + " do you know @" + user2 + "?";
		    
		    console.log("ConnectionStatus: " + connectionStatus);
		    postTweet(connectionStatus);

		    processing = false;
		}
	    }
	});	
    });
}

// Every 5 hours go through and favorite retweets
function favRTs () {
  T.get('statuses/retweets_of_me', {}, function (e,r) {
    for(var i=0;i<r.length;i++) {
      T.post('favorites/create/'+r[i].id_str,{},function(){});
    }
    console.log('harvested some RTs'); 
  });
}

// Every 15 minutes try to start connecting people
setInterval(function() {
    try {
	connectorPost();
    } catch (e) {
	console.log(e);
    }
}, 60000*15 );

// every 5 hours, check for people who have RTed me, and favorite them
setInterval(function() {
  try {
    favRTs();
  }
 catch (e) {
    console.log(e);
  }
},60000*60*5);

// Wait 2 seconds after startup and start posting
setTimeout(function() {
    connectorPost();
}, 2000);
