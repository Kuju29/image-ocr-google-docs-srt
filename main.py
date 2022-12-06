from google.cloud import vision
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from pathlib import Path
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload

import io
import os
import json

CREDS_FILE_LOCATION = os.path.join(os.getcwd(), "sa-account.json")
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = CREDS_FILE_LOCATION


with open('config.json') as config_file:
    data = json.load(config_file)

SCOPES = ['https://www.googleapis.com/auth/drive']
CLIENT_ACCOUNT = os.path.isfile('./credentials.json')
CLIENT_SECRET_FILE = 'credentials.json'


def get_credentials(CLIENT_SECRET_FILE):
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CLIENT_SECRET_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return build('drive', 'v3', credentials=creds)


def detect_text(path):
    """Detects text in the file."""
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))

    retval = None
    if len(texts) > 0:
        retval = texts[0].description
        # retval += '\n'

    return retval


def main(mydir=data['Image_location']):
    if CLIENT_ACCOUNT and CLIENT_SECRET_FILE:
        service = get_credentials(CLIENT_SECRET_FILE)

        current_directory = Path(Path.cwd())
        raw_texts_dir = Path(f'{current_directory}/raw_texts')
        texts_dir = Path(f'{current_directory}/texts')
        srt_file = open(
            Path(f'{current_directory}/subtitle_output.srt'), 'a', encoding='utf-8')
        line = 1

        if not raw_texts_dir.exists():
            raw_texts_dir.mkdir()
        if not texts_dir.exists():
            texts_dir.mkdir()

        images = Path(f'{mydir}').rglob('*.jpeg')
        for image in images:

            # Get data
            imgfile = str(image.absolute())
            imgname = str(image.name)
            raw_txtfile = f'{current_directory}/raw_texts/{imgname[:-5]}.txt'
            txtfile = f'{current_directory}/texts/{imgname[:-5]}.txt'

            if os.path.exists(txtfile):
                continue

            mime = 'application/vnd.google-apps.document'
            res = service.files().create(
                body={
                    'name': imgname,
                    'mimeType': mime
                },
                media_body=MediaFileUpload(
                    imgfile, mimetype=mime, resumable=True)
            ).execute()

            downloader = MediaIoBaseDownload(
                io.FileIO(raw_txtfile, 'wb'),
                service.files().export_media(
                    fileId=res['id'], mimeType="text/plain")
            )
            done = False
            while done is False:
                status, done = downloader.next_chunk()

            service.files().delete(fileId=res['id']).execute()

            # Create clean text file
            raw_text_file = open(raw_txtfile, 'r', encoding='utf-8')
            text_content = raw_text_file.read()
            raw_text_file.close()
            text_content = text_content.split('\n')
            text_content = ''.join(text_content[2:])
            text_file = open(txtfile, 'w', encoding='utf-8')
            text_file.write(text_content)
            text_file.close()

            start_hour = imgname.split('_')[0][:2]
            start_min = imgname.split('_')[1][:2]
            start_sec = imgname.split('_')[2][:2]
            start_micro = imgname.split('_')[3][:3]

            end_hour = imgname.split('__')[1].split('_')[0][:2]
            end_min = imgname.split('__')[1].split('_')[1][:2]
            end_sec = imgname.split('__')[1].split('_')[2][:2]
            end_micro = imgname.split('__')[1].split('_')[3][:3]

            # Format start time
            start_time = f'{start_hour}:{start_min}:{start_sec},{start_micro}'

            # Format end time
            end_time = f'{end_hour}:{end_min}:{end_sec},{end_micro}'
            # Append the line to srt file
            srt_file.writelines([
                f'{line}\n',
                f'{start_time} --> {end_time}\n',
                f'{text_content}\n\n',
                ''
            ])
            print(f"""{line}: [ {start_time} ]: {imgname}\n{text_content}\n""")
            line += 1

        srt_file.close()
    else:
        current_directory = os.getcwd()
        srt_file = open(os.path.join(
            f'{current_directory}', 'subtitle_output.srt'), 'w', encoding='utf-8')

        images = Path(f'{mydir}').rglob('*.jpeg')
        line = 1

        for image in images:
            # Get data
            imgname = str(image.name)
            text_content = detect_text(image)

            if text_content is not None:
                text_content = text_content.strip()
                start_hour = imgname.split('_')[0][:2]
                start_min = imgname.split('_')[1][:2]
                start_sec = imgname.split('_')[2][:2]
                start_micro = imgname.split('_')[3][:3]

                end_hour = imgname.split('__')[1].split('_')[0][:2]
                end_min = imgname.split('__')[1].split('_')[1][:2]
                end_sec = imgname.split('__')[1].split('_')[2][:2]
                end_micro = imgname.split('__')[1].split('_')[3][:3]

                # Format start time
                start_time = f'{start_hour}:{start_min}:{start_sec},{start_micro}'

                # Format end time
                end_time = f'{end_hour}:{end_min}:{end_sec},{end_micro}'

                # Append the line to srt file
                srt_file.writelines([
                    f'{line}\n',
                    f'{start_time} --> {end_time}\n',
                    f'{text_content}\n\n'
                ])
                print(
                    f"""{line}: [ {start_time}] : {imgname}\n{text_content}\n""")
                line += 1

        srt_file.close()


if __name__ == '__main__':
    main()
