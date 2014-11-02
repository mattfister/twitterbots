// This is a twitter bot that attempts to connect two people talking about the same trend.
// Every 15 minutes it picks a trend, announces what it's thinking about.
// Then it listens for 5 minutes of tweets about that trend. Once this is done it uses those
// tweets to construct a new tweet via a Markov chain of those inputs. It tweets this.
// Then it picks two of the people who it had listened to and tries to connect them to each other
// The bot wins if those two people start talking.

// Created by Matthew Fister (@mattjfister)

// Thanks to Darius Kazemi (@tinysubversions) for this article and starter code http://tinysubversions.com/2013/09/how-to-make-a-twitter-bot/
// And Jason Bury for this Markov chain code http://www.soliantconsulting.com/blog/2013/02/draft-title-generator-using-markov-chains
// ttezel too, for twitjs https://github.com/ttezel/twit

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
    var goodTweet = false;
    var tweet = [""];
    while (goodTweet == false ) {
	word = choice(startwords);
	tweet = [word];
	console.log("startWord: " + word);
	while (wordstats.hasOwnProperty(word)) {
            var next_words = wordstats[word];
	    console.log("nextWords: " + next_words);
            word = choice(next_words);
	    console.log("nextWord: " + word);
            tweet.push(word);
            if (terminals.hasOwnProperty(word)) {
		break;
	    }
	}
	tweet = tweet.join(' ');
	if (tweet.length < 140) {
	    goodTweet = true;
	}
    }
    return tweet;
}

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

var thoughts = ["Thinking about ", "Considering ", "Wondering about ", "Contemplating ", "Learning about ", "Interested in ", "Been thinking about ", "Feeling like "];

function postAboutTopic(topic) {
    var generalPost = choice(thoughts) + topic;
    console.log("\n\n");
    console.log("|||||||||||| Post: " + generalPost);
    console.log("\n");
    //postTweet(generalPost);
}

// Keep track of if we're already processing tweets, so we don't start again
var processing = false;

var numAdded = 0;
var stream;
var startListeningTime = null;

// This keeps track of how our streamin is doing
// It will make decisions on whether we should stop or continue
// and if it's been going well enough for 5 minutes, it will
// send a tweet.
function monitorStreaming() {
    if (processing == true && startListeningTime != null) {
	var currentTime = Date.now();
	var timePassed = currentTime - startListeningTime;
	console.log("Been listening to " + topic + " for " + timePassed/1000.0 + "s. Added " + numAdded + " tweets");
	if (timePassed > 60000 && numAdded < 10) {
	    stream.stop();
	    processing = false;
	    console.log("Abandoning topic: " + topic);
	} else if (timePassed > 60000*5) {
	    var newStatus = markovTweet();
	    console.log("\n|||||||||||| Status: " + newStatus);
	    postTweet(newStatus);
	    stream.stop();
	    chooseUsers();
	    followUsers();
	    sendConnectTweet(user1, user2);
	    processing = false;
	}
    } else {
	console.log("Not currently streaming\n");
    }
}


connections = [" do you know ", " you know ", " what's up with ", " who is ", " you seem kind of like "] 
function sendConnectTweet(user1, user2) {
    connectionStatus = "@" + user1 + choice(connections) + "@" + user2 + "?"; 
    console.log("\n||||||||||| ConnectionStatus: " + connectionStatus);
    postTweet(connectionStatus);
}

// This sets up our streaming. Picks a trend in the US, listens to a bunch of tweets about it,
// and adds the tweets to our corpus
function connectorStream() {
    if (processing == true ) {
	console.log("Still processing...");
	return;
    }
    startListeningTime = null;
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
	stream = T.stream('statuses/filter', { track: topic })
	
	startListeningTime = Date.now();
	stream.on('tweet', function(tweet) {
	    if (passesFilter(tweet.text)) {
		// console.log("Adding tweet " + numAdded + " by user: " + tweet.user.screen_name);
		// console.log("text: " + tweet.text);
		addTweet(tweet.text);
		addUser(tweet.user.screen_name);
		numAdded++;
	    }
	});
    });
}

// Compares two long string integers
// Used because js has problems with int64s
var stringGreaterThan = function(a, b) {
    // Pad string a to size of string b
    while (a.length < b.length) {
	a = "0" + a;
    }
    // Pad string b to size of string a
    while (b.length < a.length) {
	b = "0" = b;
    }
    
    // now compare them
    return a > b;
}

// Keep track of which users we applied to
repliedToUsers = {};
replyMessages = [" you both seem p cool", " thought you were both interesting", " :)", " you're cool", " you both seem chill", " lol"]
function postReplyToMention(screenName, replyToId) {
    if (!repliedToUsers.hasOwnProperty(screenName)) {
	repliedToUsers[screenName] = true;
	tweet = "@" + screenName + choice(replyMessages);
	T.post('statuses/update', {status: tweet, in_reply_to_status_id: replyToId}, function(err, data, reply) {
	});
	console.log("||||||||| Replied: " + tweet);
    } else {
	console.log("Wanted to reply to screenName: " + screenName, ", but already replied to them");
    }
}


var lastMentionIdStr = null;
var firstMentionPull = true;
function handleMentions() {
    console.log("Getting mentions\n");
    T.get('statuses/mentions_timeline', {}, function(e,r) {
	for (var i=0; i < r.length; r++) {
	    if (lastMentionIdStr == null || stringGreaterThan(r[i].id_str, lastMentionIdStr) ) {
		lastMentionIdStr = r[i].id_str;
		console.log("Setting last mentionId to " + lastMentionIdStr);
		if (firstMentionPull == false) {
		    console.log("\n!!!!!!!!! Got a new mention!");
		    console.log("Mention from user: " + r[i].user.screen_name);
		    console.log("Mention text: " + r[i].text);
		    postReplyToMention(r[i].user.screen_name, r[i].id_str);
		}
	    }
	}
	firstMentionPull = false;
    });
}



function streamers() {
    try {
	connectorStream();
    } catch (e) {
	console.log(e);
    }
}

// Every 1 minute  try to start streaming
setInterval(streamers, 60000*1 );

// Every 15 seconds see how we're doing
setInterval(function() {
    try {
	monitorStreaming();
    } catch (e) {
	console.log(e);
    }
}, 1000 * 15 ); 

// Wait 2 seconds after startup and start posting
setTimeout(streamers, 2000);

function mentions() {
    try {
	handleMentions();
    } catch (e) {
	console.log(e);
    }
}

// Every 10 minutes see if we have new mentions
setInterval(mentions, 60000 * 10);

// Get our first mentions 5 seconds after we start
setTimeout(mentions, 5000);

// Do a quick first pass on mentions just to test
setTimeout(mentions, 60000 * 1);
