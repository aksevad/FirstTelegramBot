t.me/MyFirstSandBoxBot

5336798046:AAHx9h_mhp-B7123cj26vGs4KFf-3aMcO8Y

For a description of the Bot API, see this page:
https://core.telegram.org/bots/api

botfather dialog:
/newbot

MyFirstSandBoxBot

/setname

My First Bot

/setjoingroups

Disable

/setdescription

ENG: Bot for assistance in antenna pointing at geostationary satellites by the sun position.
RU: Бот помощи в наведении антенн на геостационарные спутники по положению солнца.

/setabouttext

Bot for antenna pointing by the sun position / Бот для наведения антенн по положению солнца



heroku deploying:
heroku login
// next steps from project main directory
git init
git add .
git commit -m "First Release 0.5"
git remote -v
git push heroku master
heroku ps
heroku ps:scale worker=1

