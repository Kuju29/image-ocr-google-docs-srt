Note : I recommend you to use it from [subtitleedit](https://github.com/SubtitleEdit/subtitleedit/releases), they just developed to support this. But if you still want free service My project is still working.

# How to use
* [Install python](https://www.python.org/)
* Download [image-ocr-google-docs-srt](https://github.com/Kuju29/image-ocr-google-docs-srt/archive/refs/heads/master.zip)
* Create new project from [Python Quickstart](https://developers.google.com/drive/api/v3/quickstart/python)
* Create new API for download api.json file and put beside main.py 
  - "credentials.json" rename from "[OAuth 2.0](https://console.cloud.google.com/apis/credentials/oauthclient)" API file (work slow but free)
  - "sa-account.json" rename from "[Service Accounts](https://console.cloud.google.com/iam-admin/serviceaccounts)" API file (work fast but 300$)
  
    ![image](https://user-images.githubusercontent.com/22098092/171820037-08f5f23d-109e-415f-8f45-ea6acd7aa7e4.png)

* Install the Google Client Library using
```
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```
* Export images using [VideoSubFinder](https://sourceforge.net/projects/videosubfinder/) and put them in images folder
* Input image location in `Config` file. [ **Need change `\` to `/` | E.g. `C:\Users` to `C:/Users`** ]
* Run main.py and login with google account (only for first time)
* Wait until it complete processing evey image.

# Credits
* [Abu3safeer](https://github.com/Abu3safeer/image-ocr-google-docs-srt)
* [brownbat](https://github.com/brownbat/image-ocr-google-docs-srt)
* [sengkyaut](https://github.com/sengkyaut/image-ocr-google-docs-srt)
