
# <img src="/static/img/AAMarkov.jpg">Markov Chains Tweet Generator</img>

A Markov Tweet Generator can be used to randomly generate (somewhat) realistic sentences, using words from a source text (like someone's tweet history). Words are joined together in sequence, with each new word being selected based on how often it follows the previous word in the source document. The results are often just nonsense, but at times can be strangely poetic.


## Table of Contents⛓

* [Tech Stack](#tech-stack)
* [Features](#features)
* [Setup/Installation](#installation)
* [To-Do](#future)
* [License](#license)

## <a name="tech-stack"></a>Tech Stack

__Frontend:__ HTML5, Jinja2, Bootstrap <br/>
__Backend:__ Python, Flask <br/>
__APIs:__ Twitter (Tweepy Library) <br/>

## <a name="features"></a>Features 🖇

Main Page 

![Main Page Logged out](/static/gif/main-page.gif)
<br/><br/><br/>
Log in with Twitter (via OAuth) 
  
![Twitter Log In](/static/gif/search-log-in-with-twitter.gif)
<br/><br/><br/>
Tweet one of the tweets generated via Markov Chains using Alice in Wonderland
text:
  
![Tweet Markov Chain](/static/gif/tweet-1.gif)
<br/><br/><br/>
Or search for Twitter accounts to generate tweets using their timeline:
  
![Search](/static/gif/search.gif)
<br>
![Search](/static/gif/search-results.gif)
<br/><br/><br/>
Tweet the results! 🐦
  
![Markov Chain Tweets](/static/gif/tweet-2.gif)

## <a name="installation"></a>Setup/Installation ⌨️

#### Requirements:

- pip
- Twitter account
- Python 2.7
- Twitter API keys

To have this app running on your local computer, please follow the below steps:

Clone repository:
```
$ git clone https://github.com/mbichoffe/markov_chains_twitter.git
```
Create a virtual environment🔮:
```
$ virtualenv venv
```
Activate the virtual environment:
```
$ source venv/bin/activate
```
Install dependencies🔗:
```
$ pip install -r requirements.txt
```
Get your own secret keys🔑 for [Twitter](https://apps.twitter.com/). Save them to a file `secrets.sh`. Your file should look something like this:
```
export TWITTER_CONSUMER_KEY="abc"
export TWITTER_CONSUMER_SECRET="abc"
export TWITTER_ACCESS_TOKEN_KEY="abc"
export TWITTER_ACCESS_TOKEN_SECRET="abc"
```
Load your secret info to your environment:
```
$ source secrets.sh
```
Run the app from the command line.
```
$ python server.py
```

## <a name="future"></a>TODO✨
* Create database to store users and tweets
* Complete mock api unittests

## <a name="license"></a>License

The MIT License (MIT)
Copyright (c) 2016 Agne Klimaite 

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.