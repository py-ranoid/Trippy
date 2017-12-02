from boto3 import Session
import boto3
from botocore.exceptions import BotoCoreError, ClientError
from contextlib import closing
import os
import pandas as pd

df = pd.read_pickle("final_udaipur.pkl")

s3 = boto3.resource('s3')
audiourls = list()

session = Session(profile_name="default")
polly = session.client("polly")

STR = "https://s3.ap-south-1.amazonaws.com/trippystatic/"

for i in range(len(df.index)):
    print i
    print df.index[i]
    print len(df['desc'][df.index[i]])
    print df['desc'][df.index[i]]

    audiourls.append("STR" + str(df.index[i]) + ".mp3");
    try:
        # Request speech synthesis
        response = polly.synthesize_speech(Text = df['desc'][df.index[i]], OutputFormat="mp3", VoiceId="Aditi")
        print response
    except (BotoCoreError, ClientError) as error:
        # The service returned an error, exit gracefully
        print error, "MIC DROP"
        sys.exit(-1)
    if "AudioStream" in response:
        with closing(response["AudioStream"]) as stream:
            try:
                # Open a file for writing the output as a binary stream
                filename = "Audio/" + str(df.index[i]) + ".mp3"
                print filename
                with open(filename, "wb") as file:
                    file.write(stream.read())
                    file.close()
                    print s3.meta.client.upload_file(Filename= "Audio/" + str(df.index[i]) + ".mp3", Bucket='trippystatic', Key= str(df.index[i]) +".mp3", ExtraArgs={"ACL":'public-read'})
                    os.remove("Audio/" + str(df.index[i]) + ".mp3")
            except IOError as error:
                print(error)
                sys.exit(-1)

df['audiourls'] = audiourls
