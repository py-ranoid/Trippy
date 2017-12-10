# -*- coding: utf-8 -*-
# Here the text can be split into 3 different branches. These branches are characterized by a language namely Spanish, Hindi and English
# This hence generates three different data files. One for English one for Hindi and one for Spanish.

from boto3 import Session
import boto3
from botocore.exceptions import BotoCoreError, ClientError
from contextlib import closing
from transer import GoogleTranslator
from prime import text2speech
import os
import pandas as pd
import sys
from nltk.tokenize.punkt import PunktSentenceTokenizer
from pydub import AudioSegment
from pydub.utils import which
from time import sleep

print "--UPDATED--"

apiKey = "55972b0f3abe41928703b8e095e1f1c5" # This key is for Bing T2S

s3 = boto3.resource('s3')

engtext = u''
spatext = u''
hintext = u''

audiourlseng = list()
audiourlsspa = list()
audiourlshin = list()

session = Session(profile_name="default")
polly = session.client("polly")

one_second_pause = AudioSegment.silent(duration=1000)

STR = "https://s3.ap-south-1.amazonaws.com/trippystatic/"

def transWrapper(text, lang):
    translator = GoogleTranslator()
    resp = translator.translate(text, source="en", target=lang)
    try:
        return resp[0]['translatedText']
    except KeyError as e:
        print e
        print resp

def truncate_paragraph(text, maxch):
    """Truncate the text to at most maxnchars number of characters.

    The result contains only full sentences unless maxnchars is less
    than the first sentence length.
    """
    tokenize=PunktSentenceTokenizer().span_tokenize # Here we can change the tokenizing function.
    sentence_boundaries = tokenize(text)
    last = None
    for start_unused, end in sentence_boundaries:
        if end > maxch:
            break
        last = end
    return text[:last] if last is not None else text[:maxch]

def withText(text, name):
    print text
    engtext = text
    hintext = text
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
                filename = "../Audio/" + str(name) + ".mp3"
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
                filename = "../SpaAudio/" + str(name) + ".mp3"
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

def withPickle(city="Udaipur"):
    # This function will work with the pickles of different cities and auto generate content and audio files.
    # REQUIRED: The pickle file must have a column called 'desc' which has the content to universalize.
    # PARAMS:
    #   infopkl:    Denotes the name of the pickle file to autogenerate for.
    #   title:      The general title of the audio files that are generated. Ex: "udaipur1"
    print "--UPDATED--"
    title = city
    city = city.lower()
    df = pd.read_pickle("../BasicCityData/" + title + "/final_" + city + ".pkl")

    hindescs = list()
    spadescs = list()

    for i in range(len(df.index)):
        print i
        print df.index[i]
        print len(df['desc'][df.index[i]])

        engtext = df['desc'][df.index[i]]
        hintext = engtext
        spatext = transWrapper(engtext, 'es')

        print engtext
        print spatext
        print hintext

        hindescs.append(hintext)
        spadescs.append(spatext)

        audiourlseng.append(STR + title + str(df.index[i]) + "eng.mp3")
        audiourlsspa.append(STR + title + str(df.index[i]) + "spa.mp3")
        audiourlshin.append(STR + title + str(df.index[i]) + "hin.mp3")

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
                    filename = "../Audio/" + str(df.index[i]) + ".mp3"
                    print filename
                    with open(filename, "wb") as file:
                        file.write(stream.read())
                        file.close()
                        print s3.meta.client.upload_file(Filename= "../Audio/" + str(df.index[i]) + ".mp3", Bucket='trippystatic', Key= str(df.index[i]) +"eng.mp3", ExtraArgs={"ACL":'public-read'})
                        os.remove("../Audio/" + str(df.index[i]) + ".mp3")
                except IOError as error:
                    print(error)
                    sys.exit(-1)

        if "AudioStream" in response2:
            with closing(response2["AudioStream"]) as stream:
                try:
                    # Open a file for writing the output as a binary stream
                    filename = "../SpaAudio/" + str(df.index[i]) + ".mp3"
                    print filename
                    with open(filename, "wb") as file:
                        file.write(stream.read())
                        file.close()
                        print s3.meta.client.upload_file(Filename= "../SpaAudio/" + str(df.index[i]) + ".mp3", Bucket='trippystatic', Key= str(df.index[i]) +"spa.mp3", ExtraArgs={"ACL":'public-read'})
                        os.remove("../SpaAudio/" + str(df.index[i]) + ".mp3")
                except IOError as error:
                    print(error)
                    sys.exit(-1)

        eaud = AudioSegment.empty()
        eaud = one_second_pause
        tsize = 128

        try:
            while hintext != '':
                sub = truncate_paragraph(hintext.decode('utf-8'), tsize)
                print "PART:", sub

                hsub = transWrapper(sub, 'hi')
                print hsub, len(hsub)

                response3 = text2speech(text = hsub, gender = 'Female', body_lang='hi-IN', voice_lang='hi-IN', destination="")
                print "HINDI: ", response3
                hcontent = response3.content

                if response3.status_code == 403:
                    sleep(3)
                    continue

                with open("../HinAudio/" + str(df.index[i]) + ".wav", "wb") as f:
                    f.write(hcontent)
                    f.close()

                cur = AudioSegment.from_wav("../HinAudio/" + str(df.index[i]) + ".wav")
                cur.append(one_second_pause)
                eaud.append(cur)
                os.remove("../HinAudio/" + str(df.index[i]) + ".wav")

                hintext = hintext.split(sub)[1].strip()

            eaud.export("../HinAudio/" + str(df.index[i]) + ".mp3", format="mp3", bitrate="192k")
            print s3.meta.client.upload_file(Filename= "../HinAudio/" + str(df.index[i]) + ".mp3", Bucket='trippystatic', Key= str(df.index[i]) +"hin.mp3", ExtraArgs={"ACL":'public-read'})

        except Exception as e:
            continue

    df['audiourls'] = audiourlseng
    df.to_pickle("../BasicCityData/" + title + "/final_" + city + ".pkl")

    df['desc'] = hindescs
    df['audiourls'] = audiourlshin
    df.to_pickle("../BasicCityData/" + title + "/hinfinal_" + city + ".pkl")

    df['desc'] = spadescs
    df['audiourls'] = audiourlsspa
    df.to_pickle("../BasicCityData/" + title + "/spafinal_" + city + ".pkl")

#withPickle("final_udaipur.pkl")
