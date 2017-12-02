# -*- coding: utf-8 -*-
# Here the text can be split into 3 different branches. These branches are characterized by a language namely Spanish, Hindi and English
# This hence generates three different data files. One for English one for Hindi and one for Spanish.

from boto3 import Session
import boto3
from botocore.exceptions import BotoCoreError, ClientError
from contextlib import closing
from transer import GoogleTranslator
import os
import pandas as pd
import sys

print "--UPDATED--"

s3 = boto3.resource('s3')

engtext = u''
spatext = u''
hintext = u''

audiourlseng = list()
audiourlsspa = list()
audiourlshin = list()

session = Session(profile_name="default")
polly = session.client("polly")

STR = "https://s3.ap-south-1.amazonaws.com/trippystatic/"

def transWrapper(text, lang):
    translator = GoogleTranslator()
    resp = translator.translate(text, source="en", target=lang)
    return resp[0]['translatedText']

def withText(text, name):
    print text
    engtext = text
    hintext = transWrapper(text, 'hi')
    spatext = transWrapper(text, 'es')
    try:
        response1 = polly.synthesize_speech(Text = engtext, OutputFormat="mp3", VoiceId="Aditi")
        response2 = polly.synthesize_speech(Text = spatext, OutputFormat="mp3", VoiceId=u'Penelope')
        print response1
        print response2
    except (BotoCoreError, ClientError) as error:
        print error

    if "AudioStream" in response1:
        with closing(response1["AudioStream"]) as stream:
            try:
                # Open a file for writing the output as a binary stream
                filename = "Audio/" + str(name) + ".mp3"
                print filename
                with open(filename, "wb") as file:
                    file.write(stream.read())
                    file.close()
                    print s3.meta.client.upload_file(Filename= "Audio/" + str(name) + ".mp3", Bucket='trippystatic', Key= str(name) +"eng.mp3", ExtraArgs={"ACL":'public-read'})
                    #os.remove("Audio/" + str(name) + ".mp3")
            except IOError as error:
                print(error)
                sys.exit(-1)

    if "AudioStream" in response2:
        with closing(response2["AudioStream"]) as stream:
            try:
                # Open a file for writing the output as a binary stream
                filename = "SpaAudio/" + str(name) + ".mp3"
                print filename
                with open(filename, "wb") as file:
                    file.write(stream.read())
                    file.close()
                    print s3.meta.client.upload_file(Filename= "SpaAudio/" + str(name) + ".mp3", Bucket='trippystatic', Key= str(name) +"spa.mp3", ExtraArgs={"ACL":'public-read'})
                    #os.remove("SpaAudio/" + str(name) + ".mp3")
            except IOError as error:
                print(error)
                sys.exit(-1)

    return(engtext, hintext, spatext)


def withPickle(infopkl, title):
    print "--UPDATED--"
    df = pd.read_pickle(infopkl)

    hindescs = list()
    spadescs = list()

    for i in range(len(df.index)):
        print i
        print df.index[i]
        print len(df['desc'][df.index[i]])

        engtext = df['desc'][df.index[i]]
        hintext = transWrapper(engtext, 'hi')
        spatext = transWrapper(engtext, 'es')

        print engtext
        print spatext
        print hintext

        hindescs.append(hintext)
        spadescs.append(spatext)

        audiourlseng.append(STR + title + str(df.index[i]) + "eng.mp3")
        audiourlsspa.append(STR + title + str(df.index[i]) + "spa.mp3")
        audiourlshin.append(STR + title + str(df.index[i]) + "eng.mp3")

        try:
            # Request speech synthesis
            response1 = polly.synthesize_speech(Text = engtext, OutputFormat="mp3", VoiceId="Aditi")
            response2 = polly.synthesize_speech(Text = spatext, OutputFormat="mp3", VoiceId=u'Penelope')
            print response1
            print response2
        except (BotoCoreError, ClientError) as error:
            # The service returned an error, exit gracefully
            print error
            sys.exit(-1)

        if "AudioStream" in response1:
            with closing(response1["AudioStream"]) as stream:
                try:
                    # Open a file for writing the output as a binary stream
                    filename = "Audio/" + str(df.index[i]) + ".mp3"
                    print filename
                    with open(filename, "wb") as file:
                        file.write(stream.read())
                        file.close()
                        print s3.meta.client.upload_file(Filename= "Audio/" + str(df.index[i]) + ".mp3", Bucket='trippystatic', Key= str(df.index[i]) +"eng.mp3", ExtraArgs={"ACL":'public-read'})
                        os.remove("Audio/" + str(df.index[i]) + ".mp3")
                except IOError as error:
                    print(error)
                    sys.exit(-1)

        if "AudioStream" in response2:
            with closing(response2["AudioStream"]) as stream:
                try:
                    # Open a file for writing the output as a binary stream
                    filename = "SpaAudio/" + str(df.index[i]) + ".mp3"
                    print filename
                    with open(filename, "wb") as file:
                        file.write(stream.read())
                        file.close()
                        print s3.meta.client.upload_file(Filename= "SpaAudio/" + str(df.index[i]) + ".mp3", Bucket='trippystatic', Key= str(df.index[i]) +"spa.mp3", ExtraArgs={"ACL":'public-read'})
                        os.remove("SpaAudio/" + str(df.index[i]) + ".mp3")
                except IOError as error:
                    print(error)
                    sys.exit(-1)

    df['audiourls'] = audiourlseng
    df.to_pickle(infopkl)

    df['desc'] = hindescs
    df.to_pickle("hin" + infopkl)

    df['desc'] = spadescs
    df['audiourls'] = audiourlsspa
    df.to_pickle('spa' + infopkl)

#withPickle("final_udaipur.pkl")
