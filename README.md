
## How to Run the Project Locally

Create `.env` file in the root directory of your project. Provide proper values for the following
environment variables:

### .env

```bash
# Flask
export FLASK_APP=application.py

# Microsoft SQL Server database
export SQL_SERVER=<your-sql-server-name>
export SQL_DATABASE=<your-sql-database-name>
export SQL_USER_NAME=<your-sql-user-name>
export SQL_PASSWORD=<your-sql-password>

# Oauth - MSAL and Azure Active Directory
export AUTHORITY=https://login.microsoftonline.com/common
export REDIRECT_PATH=/getAToken
export SCOPE=User.Read
export SESSION_TYPE=filesystem

export CLIENT_SECRET=<your-client-secret>
export CLIENT_ID=<your-client-id>
```

### Create Virtual Environment

````bash
# macOS/Linux
sudo apt-get install python3-venv    # If needed
python3 -m venv friss-env

# Windows
python -m venv friss-env
````

Activate the environment by running 

`source friss-env/bin/activate` # (Linux/macOS) 

or `friss-env\scripts\activate` # (Windows). 

### Install necessary Python dependencies:

`pip install -r requirements.txt`


### Run Flask app Locally

launch the program using
 
`python application.py`

# Identity Matching Probability (Flask Web Project)

This project is a Python web application built using Flask. The user can log in and out and input data of 2 people in order to calculate the probability of them being the same person. An use consists of a name and password stored in an Azure SQL Server. We also implement OAuth2 with Sign in with Microsoft using the `msal` library, along with app logging.

## Log In Credentials for Flask Web Project

- Username: admin
- Password: pass

Or, once the MS Login button is implemented, it will automatically log into the `admin` account.

## Project Instructions 

Necessary steps:
1. Create a Resource Group in Azure.
2. Create an SQL Database in Azure that contains a user table and data (populated with the scripts provided in the SQL Scripts folder).
    - Provided a screenshot of the populated tables as detailed further below.
3. Add functionality to the Sign In With Microsoft button. 
    - This will require using `msal` library, along with appropriate registration in Azure Active Directory.
4. Choose to use either a VM or App Service to deploy the Flask Web Project to Azure and go through with deployment.
5. Add logging for whether users successfully or unsuccessfully logged in.
6. To prove that the application in on Azure and working, go to the URL of your deployed app, log in using proper credentials, click the Compare button to calculate probability of matching identity.
7. Provide screenshots including all of the resources that were created to complete this project. (see sample screenshot in "images" folder)

## images Folder

This folder contains sample screenshots to prove the completed various tasks throughout the project.

1. friss-solution.png is a screenshot from running the Flask Web Project on Azure and prove that the I was able to create a new entry. The User and Password fields must be populated to prove that the data is being retrieved from the Azure SQL Database.
2. azure-portal-resource-group.png is a screenshot from the Azure Portal showing all of the contents of the Resource Group I needed to create. The resource group must (at least) contain the following:
	- SQL Server
	- SQL Database
	- Resources related to deploying the app
3. sql-storage-solution.png is a screenshot showing the created tables and one query of data from the initial scripts.
5. uri-redirects-solution.png is a screenshot of the redirect URIs related to Microsoft authentication.
6. log-solution.png is a screenshot showing one potential form of logging with an "Invalid login attempt" and "admin logged in successfully", taken from the app's Log stream. 

# OAuth2 with MSAL

This part helps integrating the Microsoft Authentication Library,
or `msal`, into an application. We need to registerer an app with Azure Active
Directory, and we'll use some of the information from there so that authentication can occur.

**Note**: This app will be served on `https` only as Azure AD will block insecure connections for redirect URIs on deployed applications. As such, when testing on `localhost`, make sure to add `https` at the start instead of `http`, e.g. `https://localhost:5555`.

1. You can launch the app, if desired, to start, but you'll notice that it doesn't yet allow you to log in with your Microsoft account. To start, open up `config.py`, and enter in both the client secret and application client ID copied down from Azure AD. 
2. You'll also notice a variable for `REDIRECT_PATH`. This should start with a `/`, and then can be whatever else you want it to be (although you should stay away from `/home`, `/login` or `/logout`, since those are used elsewhere in the app). Once you have this set, go back to Azure AD and enter this as the redirect URI for your app, as well as adding a logout URI.
3. Now, you're ready to get started with `msal`. The app code contained in `views.py` currently implements a bit of basic log in and logout with the `Flask-Login` libraryso that the "Sign in with Microsoft" button on the app  works appropriately. The suggested order is as follow:
    - Implement `_build_msal_app` to create a confidential client application
    - Implement `_build_auth_url` to get an authorization request URL
    - Acquire a token from an msal app within the `authorized` function
    - Add the appropriate logout URL to the `logout` function
    
    Together, the above four steps should allow you to have a functional "Sign in with Microsoft" button with the Microsoft Authentication Library, as well as to log back out of the related Microsoft account.
4. Test the app out in localhost (making sure to use `https`), or feel free to deploy the app as well.

# Deploying Application to Azure Web Services

After creating an Azure App Service by pointing out your Github or Azure Repos, 
configure the above environment variables by using the **configuration** settings.
 
<br><img src="https://github.com/nayanex/UdaciZoo/blob/main/images/settings.png"/>


In Azure Web Service Configuration:

```json
[
  {
    "name": "CLIENT_SECRET",
    "value": "<your-client-secret>",
    "slotSetting": false
  },
  {
    "name": "CLIENT_ID",
    "value": "<your-client-id>",
    "slotSetting": false
  },
  {
    "name": "SQL_SERVER",
    "value": "<your-sql-server-name>",
    "slotSetting": false
  },
  {
    "name": "SQL_DATABASE",
    "value": "<your-sql-database-name>",
    "slotSetting": false
  },
  {
    "name": "SQL_USER_NAME",
    "value": "<your-sql-user-name>",
    "slotSetting": false
  },
  {
    "name": "SQL_PASSWORD",
    "value": "<your-sql-password>",
    "slotSetting": false
  }
]
```

## Dependencies

1. A free Azure account
2. A GitHub account
3. Python 3.7 or later
4. Visual Studio 2019 Community Edition (Free)
5. The latest Azure CLI (helpful; not required - all actions can be done in the portal)

All Python dependencies are stored in the requirements.txt file. To install them, using Visual Studio 2019 Community Edition:
1. In the Solution Explorer, expand "Python Environments"
2. Right click on "Python 3.7 (64-bit) (global default)" and select "Install from requirements.txt"

## Troubleshooting

- Mac users may need to install `unixodbc` as well as related drivers as shown below:
    ```bash
    brew install unixodbc
    ```
- Check [here](https://docs.microsoft.com/en-us/sql/connect/odbc/linux-mac/install-microsoft-odbc-driver-sql-server-macos?view=sql-server-ver15) to add SQL Server drivers for Mac.


## Test the API

### with Curl 

```
curl -k -X POST -H 'Content-Type: application/json' -d '{"persons":[{"first_name":"Andrew", "last_name":"Craw", "birth_date": "20-02-1985", "bsn":"931212312"}, {"first_name":"A.", "last_name":"Craw", "birth_date": "20-02-1985", "bsn":"931212312"}]}' https://localhost:5555/probability
```

## Installation

Make a copy of `example.env` file with the name `.env`. Fill missed credentials and settings there.

From the root of the project run
```
make install
```
It will create a virtual environment and install all the dependencies.

## How to run
Switch to the virtual environment
```
friss-env/bin/activate
```
Then run 
```
python application.py 
```

## For developers

To setup a dev environment run
```
make dev_install
```
Run unittests
```
make test
```
Check linters
```
make lint
```
Try to fix linter and sort errors automatically
```
make format
```

Check `Makefile` for other possible commands

## PR Submission Policy

All commits are mandatory to start with the prefix NEW, FIX or OPT :

> NEW - all new features, can brake backward compatibility.

> FIX - fixing an issue in existing functionality.

> OPT - optional improvements, refactoring etc. Must be backward compatible.

