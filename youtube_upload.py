import httplib2
import os
import random
import sys
import time

from apiclient.discovery import build
from apiclient.errors import HttpError
from apiclient.http import MediaFileUpload
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow
from traceback import print_exc

httplib2.RETRIES = 1

MAX_RETRIES = 0
RETRIABLE_EXCEPTIONS = (httplib2.HttpLib2Error, IOError)
RETRIABLE_STATUS_CODES = [500, 502, 503, 504]

YOUTUBE_UPLOAD_SCOPE = "https://www.googleapis.com/auth/youtube.upload"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

MISSING_CLIENT_SECRETS_MESSAGE = ""
VALID_PRIVACY_STATUSES = ("public", "private", "unlisted")

def get_authenticated_service(args, account):
    client_secrets_filepath = os.path.join(".", "credentials", account, "client_secrets.json")
    oauth2_filepath = os.path.join(".", "credentials", account, "oauth2.json")
    
    flow = flow_from_clientsecrets(client_secrets_filepath,
        scope=YOUTUBE_UPLOAD_SCOPE,
        message=MISSING_CLIENT_SECRETS_MESSAGE)

    storage = Storage(oauth2_filepath)
    credentials = storage.get()
    
    if credentials is None or credentials.invalid:
        credentials = run_flow(flow, storage, args)

    return build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
        http=credentials.authorize(httplib2.Http()))

def initialize_upload(youtube, options):
    tags = None
    if options.keywords:
        tags = options.keywords.split(",")

    body=dict(
        snippet=dict(
            title=options.title,
            description=options.description,
            tags=tags,
            categoryId=options.category
        ),
        status=dict(
            privacyStatus=options.privacyStatus
        )
    )

  # Call the API's videos.insert method to create and upload the video.
    insert_request = youtube.videos().insert(
        part=",".join(body.keys()),
        body=body,
        media_body=MediaFileUpload(options.file, chunksize=-1, resumable=True)
    )

    resumable_upload(insert_request)

def resumable_upload(insert_request):
    response = None
    error = None
    retry = 0
    while response is None:
        try:
            print("Uploading file...")
            status, response = insert_request.next_chunk()
            if response is not None:
                if 'id' in response:
                    print("Video id {0} was successfully uploaded. ".format(response['id']))
                else:
                    exit("The upload failed with an unexpected response: %s" % response)
        except HttpError: 
            exit(print_exc())

        if error is not None:
            print(error)
            retry += 1
            if retry > MAX_RETRIES:
                exit("No longer attempting to retry.")

            max_sleep = 2 ** retry
            sleep_seconds = random.random() * max_sleep
            print ("Sleeping %f seconds and then retrying... " + sleep_seconds)
            time.sleep(sleep_seconds)


def upload_video(account: str, video_file: str, title: str ="Test Title", description: str ="Test Desctiption", category: str ="22", keywords: str ="", privacy_status: str ="public"):
    args = argparser
    args.file = video_file
    args.title = title
    args.description = description
    args.category = category
    args.keywords = keywords
    args.privacyStatus = privacy_status
    argparser.parse_args()
    youtube = get_authenticated_service(args, account)
    try:
        initialize_upload(youtube, args)
    except (HttpError):
        print("An HTTP error %d occurred:\n%s")


# if __name__ == '__main__':
#     argparser.add_argument("--file", required=True, help="Video file to upload")
#     argparser.add_argument("--title", help="Video title", default="Test Title")
#     argparser.add_argument("--description", help="Video description",
#         default="Test Description")
#     argparser.add_argument("--category", default="22",
#         help="Numeric video category. " +
#             "See https://developers.google.com/youtube/v3/docs/videoCategories/list")
#     argparser.add_argument("--keywords", help="Video keywords, comma separated", default="")
#     argparser.add_argument("--privacyStatus", choices=VALID_PRIVACY_STATUSES,
#         default=VALID_PRIVACY_STATUSES[0], help="Video privacy status.")
#     args = argparser.parse_args()

#     if not os.path.exists(args.file):
#         exit("Please specify a valid file using the --file= parameter.")

#     youtube = get_authenticated_service(args)
    # try:
    #     initialize_upload(youtube, args)
    # except HttpError:
    #     print ("An HTTP error %d occurred:\n%s")