# Arabic-Spam-Tweets-Bots-User-Detection-Tool
This entire project was proposed at Prince Sattam Bin Abdulaziz University as a graduating project by Moayad Alkhozayem and Nasser Alkhotaifi.

We can briefly explain the project idea as an application called TwitFake that listens to the Arabic hashtag/keyword entered by the user and starts listening to Twitter API stream for any tweet containing that hashtag the user entered, then analyze each account tweeting in that hashtag by sending at to a third-party server (botometer) which is responsible for analyzing the instance from the Twitter stream, after that a classification of the hashtag if its spam hashtag or not. The results are displayed to the user in GUI and a copy of the results is stored in a dataset for future work.

Note that the software cannot run if Python libraries required by the application are not
installed in your machine or the Python/libraries existing in your system might conflict with the application used libraries (Python 3.10 was used for this application).
Also, the credential keys are required to fill in config.ini by anyone who wants to use this tool, all keys can be generated for free from the following resources:

1- Twitter developers portal: https://developer.twitter.com/en

2- Botometer key from Rapid API: https://rapidapi.com/OSoMe/api/botometer-pro

If you faced any problems with botometer library please consider uninstalling tweepy and botometer libraries and reinstalling botometer library alone (tweepy will automatically install with botometer installation).

The very first records of the datasets uploaded might need a preprocessing/cleaning steps since these few records were built during the first tests of the tool which might had some errors before it was fixed, so please consider that.

Thanks.
