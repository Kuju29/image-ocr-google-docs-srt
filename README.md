# How to use
* [Install python](https://www.python.org/)
* Create new project from [Python Quickstart](https://developers.google.com/drive/api/v3/quickstart/python)
* Create new API for [download credentials.json or sa-account.json](https://console.cloud.google.com/apis/credentials) file and put beside main.py 
  - "credentials.json" rename from "OAuth 2.0" API file (free)
  - "sa-account.json" rename from "Service Accounts" API file (not sure)
* Install the Google Client Library using
```
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```
* Export images using [VideoSubFinder](https://sourceforge.net/projects/videosubfinder/) and put them in images folder
* Run main.py and login with google account (only for first time)
* Wait until it complete processing evey image.
