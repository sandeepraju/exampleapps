Plivo 2 Factor Authentication Example
=====================================

## About

This example shows how [Plivo APIs](http://plivo.com/api) can be used to integrate a two factor authentication system into your own web application. This example is built in Python using Flask application framework but the concept behind it language agnostic. So be it Python, PHP, Ruby or Node, the concept remains the same.

The next section explains how the application works and inturn how plivo as a platform works. There is a seperate section on deployment which explains how to deploy this application on Heroku.

## How to use it

[Here is a live demo](http://shielded-hollows-9845.herokuapp.com/) of this sample application where you can try out how it works. This application verifies your phone number using the two factor authentication system. In the application, enter your phone number in [E.164](http://en.wikipedia.org/wiki/E.164) format and click on 'Send Verification Code'. This sends an SMS to that number with a random security code in it. The application now shows a text box to enter this code to verify your mobile number. Once you get the code in the SMS, enter the code in the text box and click 'Check'. This will tell you whether the code you entered is correct or not. If you enter the correct code, then the application knows that the phone number belongs to you and thus the number is verified.

## How it works

To understand how this application works, we need to look into how the 'Plivo Message' feature works. Lets assume you have a web server which requires to send & receive SMS. Here is the step by step procedure you need to follow ... _blah blah blah..._

## Deployment on Heroku

This section explains how to deploy this application on Heroku.

1. Create an account for on heroku.

2. Install the Heroku toolbelt using the the command 
```shell
wget -qO- https://toolbelt.heroku.com/install-ubuntu.sh | sh
``` 
for debian based systems (ubuntu, etc.) or for mac, download the toolbelt from [here](https://toolbelt.heroku.com/osx).

From the official heroku docs,

>The toolbelt contains the Heroku client, a command-line tool for creating and managing Heroku apps; Foreman, an easy option for running your apps locally; and Git, the revision control system needed for pushing applications to Heroku.

3. Login to heroku from the toolbelt using the following command

```
heroku login
```

If you do not have an ssh public key in your system, it prompts to automatically create it. Hit 'Y' when prompted.

```
$ heroku login
Enter your Heroku credentials.
Email: sandeep@plivo.com
Password: 
Could not find an existing public key.
Would you like to generate one? [Yn] 
Generating new SSH public key.
Uploading ssh public key /home/sandeep/.ssh/id_rsa.pub
```
Once this is done, then we are ready to deploy the application.

4. __more to come here...__
