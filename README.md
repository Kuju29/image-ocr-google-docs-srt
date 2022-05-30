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
* Export images using [VideoSubFinder](https://sourceforge.net/projects/videosubfinder/)
* Edit main.py in "DIR_images" put your image location. e.g. "D:\utorrent" change to "D:/utorrent"
![image](https://user-images.githubusercontent.com/22098092/170997358-0e018d48-9f84-4ac8-9dbf-914ab464c4f7.png)
* Run main.py and if use credentials.json need login with google account (only for first time)
* Wait until it complete processing evey image.
