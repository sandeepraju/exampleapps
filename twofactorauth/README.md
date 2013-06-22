Plivo Two Factor Auth Example
=======================================

## About

This example shows how [Plivo APIs](http://plivo.com/api) can be used to integrate a two factor authentication system into your own web application. This example is built in Python using Flask application framework but the concept behind it language agnostic. So, be it Python, PHP, Ruby or Node, the concept remains the same.

The next section explains how the application works and in-turn how Plivo as a platform works. There is a separate section on deployment which explains how to deploy this application on Heroku.

## How to use it

[Here is a live demo](http://shielded-hollows-9845.herokuapp.com/) of this sample application where you can try out how it works. This application verifies your phone number using the two factor authentication system. In the application, enter your phone number in [E.164](http://en.wikipedia.org/wiki/E.164) format (currently works for US numbers) and click on 'Send Verification Code'. This sends an SMS to that number with a random security code in it. The application now shows a text box to enter this code to verify your mobile number. Once you get the code in the SMS, enter the code in the text box and click 'Check'. This will tell you whether the code you entered is correct or not. If you enter the correct code, then the application knows that the phone number belongs to you and thus the number is verified.

## Deployment on Heroku

### Initial Setup

This section explains how to deploy this application on Heroku.

1. [Create an account](https://id.heroku.com/signup) on Heroku (its free!).

2. Install the Heroku toolbelt using the the command `wget -qO- https://toolbelt.heroku.com/install-ubuntu.sh | sh`
    for debian based systems (ubuntu, etc.) and for mac, download the toolbelt from [here](https://toolbelt.heroku.com/osx).

    From the official heroku docs,

    >The toolbelt contains the Heroku client, a command-line tool for creating and managing Heroku apps; Foreman, an easy option for running your apps locally; and Git, the revision control system needed for pushing applications to Heroku.

3. Login to heroku from the toolbelt using the `heroku login` command.
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

### Configuring the application

The application should be configured before deployment starts.

1. Removing the current `.git` folder in the project root using `rm -rf  .git/`.
2. Copy the `settings.py.sample` to `settings.py`.
3. Start by changing the value of `APPLICATION_REDIS_URI` to `redis://localost:6379`.
4. To get the Plivo Auth ID, Auth Token and Plivo Number, log into your plivo.com account.
5. The Auth ID and Auth Token can be found in the [dashboard](https://manage.plivo.com/dashboard/)'s top-right region. Update these values in the `settings.py`.
6. To buy a number for this application, create an application in the ['Applications'](https://manage.plivo.com/app/) menu and then click on ['Numbers'](https://manage.plivo.com/number/) and go to ['Buy Numbers Tab'](https://manage.plivo.com/number/search/).
7. Once you get the number, enter it in the `settings.py` file.

We are done with configuring the application, let us start the deployment process.

### The Actual Deployment

1. Change to directory which contains the `Procfile`.
2. Create a [virtual environment](http://www.virtualenv.org/en/latest/) by running `virtualenv --distribute`.  
__NOTE__: _if you don't have `virtualenv` installed, then install python setup tools first using `sudo apt-get install python-setuptools` and then install `virtualenv` using `sudo pip install virtualenv`_
3. Activate the `virtualenv` using `source ./venv/bin/activate`.
4. Install all the application's dependencies specified in `requirements.txt` using `pip install -r requirements.txt`.
5. Install the [redistogo](https://addons.heroku.com/redistogo) addon to use the heroku free data store for this application. To add a free redistogo data store to this application use `heroku addons:add redistogo` command.
6. Once, the dependencies are installed, start the application process locally using `foreman start` command. It should start the application locallly and should NOT throw any error or exception. If successfully started, do `CTRL+C` to stop it.
7. Initialize an empty git repository using `git init` command.
8. Add all the files of the current directory using `git add .` command.
9. Make an initial commit using `git commit -m "<commit message here>"`.
10. Finally create an application on Heroku server using the `heroku create` which creates a remote git repo and updates the origin to the newly created git repo.
11. Now, push the local code to the heroku repo for deployment using `git push heroku master`.
12. To run one web process as specified in the `Procfile`, run the `heroku ps:scale web=1` command.
13. Now, the application should be successfully running if everything went right!
14. We can test it using `heroku ps` command. It should say something like `web.1: up for 5s`.
15. We can check the application logs using `heroku logs` command.
16. To open the application in the web browser, type `heroku open` and hit `ENTER`.
17. You'll see this application in the web browser.

Find the live demo of the application [here](http://shielded-hollows-9845.herokuapp.com/). For more detailed information on deployment on heroku, visit the [official heroku documentation](https://devcenter.heroku.com/articles/python). More information about Plivo APIs can be found in the [offical API docs](http://plivo.com/docs/).

Helper libraries for various languages are available on the [Plivo github page](http://github.com/plivo).
