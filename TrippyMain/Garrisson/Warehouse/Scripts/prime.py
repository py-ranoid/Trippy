# -*- coding: utf-8 -*-
import requests
from xml.etree import ElementTree
# cd gitpository/TrippyRepo
# cd Trippy/TrippyMain/Warehouse/Scripts
from voice_name_gen import get_lang_dict

apiKey = "55972b0f3abe41928703b8e095e1f1c5"

Trans_Names = get_lang_dict()
trans_apikey = 'AIzaSyCQrLEKo-EfpK1BQeuOdmng41hziXH2OqE'


def translate(query='Hello', target_lang='es'):
    data = {'key': trans_apikey,
            'q': query,
            'format': 'text',
            'target': target_lang}
    r = requests.post('https://translation.googleapis.com/language/translate/v2',
                      data=data)
    return r.json()['data']['translations'][0]['translatedText']


def text2speech(text='This is a demo to call microsoft text to speech service in Python.', gender='Female', body_lang='en-us', voice_lang='en-US', destination='test.mp3'):
    body = ElementTree.Element('speak', version='1.0')
    body.set('{http://www.w3.org/XML/1998/namespace}lang', body_lang)

    voice = ElementTree.SubElement(body, 'voice')
    voice.set('{http://www.w3.org/XML/1998/namespace}lang', voice_lang)
    voice.set('{http://www.w3.org/XML/1998/namespace}gender', gender)
    voice.set('name', Trans_Names[voice_lang][gender])
    voice.text = text
    print type(voice.text)
    print voice.text

    headers = {"Ocp-Apim-Subscription-Key": apiKey}
    AccessTokenHost = "api.cognitive.microsoft.com"
    path = "/sts/v1.0/issueToken"
    s = requests.post('https://' + AccessTokenHost + path, headers=headers)
    acces_token_data = s.text
    print acces_token_data
    print s
    accesstoken = acces_token_data.decode("UTF-8")

    headers = {"Content-type": "application/ssml+xml",
               "X-Microsoft-OutputFormat": "riff-16khz-16bit-mono-pcm",
               "Authorization": "Bearer " + accesstoken,
               "X-Search-AppId": "07D3234E49CE426DAA29772419F436CA",
               "X-Search-ClientID": "1ECFAE91408841A480F00935DC390960",
               "User-Agent": "TTSForPython"}
    s2 = requests.post("https://" + 'speech.platform.bing.com' +
                       "/synthesize", data=ElementTree.tostring(body), headers=headers)

    return s2
    # print s2
    # print s2.reason
    #
    # cont = s2.content
    #
    # print len(cont)
    # return cont
    # with open(destination, 'w') as outfile:
    #     outfile.write(s2.content)


def trans_and_store(text, langs=['en-IN', 'hi-IN', 'ca-ES'], gender='Female', file_title='test'):
    fin_dict = {}
    for l in langs:
        language_code = l.split('-')[0]
        resp = translate(text, language_code)
        path = file_title + '_' + language_code + '.mp3'
        text2speech(resp, gender=gender, body_lang=l,
                    voice_lang=l, destination=path)
        fin_dict[l] = {'text': resp, 'audiopath': path}
    return fin_dict


# trans_and_store('With the Bing text to speech API, your application can send HTTP requests to a cloud server, where text is instantly synthesized into human-sounding speech.')


"""
ar-EG 	Arabic (Egypt), modern standard 	        hi-IN 	Hindi (India)
ca-ES 	Catalan (Spain) 	                        it-IT 	Italian (Italy)
da-DK 	Danish (Denmark)                            ja-JP 	Japanese (Japan)
de-DE 	German (Germany) 	                        ko-KR 	Korean (Korea)
en-AU 	English (Australia) 	                    nb-NO 	Norwegian (Bokmål) (Norway)
en-CA 	English (Canada) 	                        nl-NL 	Dutch (Netherlands)
en-GB 	English (United Kingdom) 	                pl-PL 	Polish (Poland)
en-IN 	English (India) 	                        pt-BR 	Portuguese (Brazil)
en-NZ 	English (New Zealand) 	                    pt-PT 	Portuguese (Portugal)
en-US 	English (United States) 	                ru-RU 	Russian (Russia)
es-ES 	Spanish (Spain) 	                        sv-SE 	Swedish (Sweden)
es-MX 	Spanish (Mexico) 	                        zh-CN 	Chinese (Mandarin, simplified)
fi-FI 	Finnish (Finland) 	                        zh-HK 	Chinese (Hong Kong SAR)
fr-CA 	French (Canada) 	                        zh-TW 	Chinese (Mandarin, Taiwanese)
fr-FR 	French (France)
"""
