INSTALLATION INSTRUCTIONS
=========================

virtualenv /var/www/stravasocial
cd /var/www/stravasocial
source bin/activate
mkdir stravatweet
cd stravatweet
easy_install https://github.com/packetslave/strava/tarball/master
python setup.py develop

MODIFICATIONS 
=============

copy stravatweet.cfg.sample to stravatweet.cfg and make the following changes

Modify RIDER to match your athlete id. Go to http://app.strava.com/dashboard
click on your name and the url will show your rider id.

rider = 1234

Modify your zip code. Yahoo uses this to determine the geographic area for
the weather report.

zip = '11111'

Create a Twitter app. https://dev.twitter.com/ Sign in with your user/password.
Mouse over your name and click 'My Applications.' Create a new application.
Assign it a Name, Description and Website URL (of your blog or a site that
you use). You do not need a callback URL. Click the settings tab, change the
Application Type to Read and Write and Update the Application Settings. Click
the Details tab, and at the bottom, click the 'Create my access token' button.
Fill in the following entries in the script from the Details page.

consumer_key = ''
consumer_secret = ''
access_key = ''
access_secret = ''

Modify the hashtags if desired.

hashtags = #bicycle, #cycling #bicycle, #cycling #bicycle #strava

Modify UNIT for either statute (Imperial) or metric

unit = 'statute'
#unit = 'metric'

Make sure the WORKDIR points to an existing directory. The system uses this
to keep track of the last ride that was tweeted.

workdir = '/var/www/stravasocial/stravatweet/'

CRONTAB
=======

*/15 * * * * /var/www/stravasocial/bin/python /var/www/stravasocial/stravatweet/stravatweet.py 2>&1>/dev/null
