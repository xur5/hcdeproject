import webapp2, urllib, urllib2, webbrowser, json
import jinja2

import os
import logging

def pretty(obj):
    return json.dumps(obj, sort_keys=True, indent=2)

def stripWordPunctuation(word):
    return word.strip(".,()<>\"\\'~?!;*:[]-+/`")

def safeGet(url):
    try:
        return urllib2.urlopen(url)
    except urllib2.HTTPError, e:
        print 'The server couln\'t fulfill the request.'
        print 'Error code: ', e.code
    except urllib2.URLError, e:
        print 'We failed to reach a server'
        print 'Reason: ', e.reason
    return None

def musREST(baseurl='http://api.musixmatch.com/ws/1.1/',
               method='matcher.lyrics.get',
               apikey='f9cf480f7586aad2c19dbc916c57a03a',
               format='json',
               params={},
               ):
    params['method'] = method
    params['apikey'] = apikey
    params['format'] = format
    if format == "json": params["nojsoncallback"] = True
    url = baseurl + "?" + urllib.urlencode(params)
    return safeGet(url)

def pretty(obj):
    return json.dumps(obj, sort_keys=True, indent=2)

# To get an API key, go to https://developer.musixmatch.com/plans
def getLyrics(title, artist):
    resp = musREST(params = {'q_track': title, 'q_artist': artist})
    if resp != None:
        dict = json.loads(resp.read())
        print(pretty(dict))
        if dict is not None and 'lyrics' in dict['message']['body']:
            data = dict['message']['body']['lyrics']['lyrics_body']
            words = data.split("*******")[0].split("...")[0]
            return words
    return None

# This method make lines into sentences by adding periods at the end so the text analysis program will work
def makeSentences(words):
    words = words.replace('\n', '. ')
    return words

def safeGet2(url):
    try:
        headers = {'X-AYLIEN-TextAPI-Application-ID':'25777ab7',
                   'X-AYLIEN-TextAPI-Application-Key': '93d253c5f5b915779ab649b119cf7d09'
                  }
        req = urllib2.Request(url, None, headers)
        return urllib2.urlopen(req)
    except urllib2.URLError, e:
        if hasattr(e,"code"):
            print "The server couldn't fulfill the request."
            print "Error code: ", e.code
        elif hasattr(e,'reason'):
            print "We failed to reach a server"
            print "Reason: ", e.reason
        return None

# To get an API key, go to https://developer.aylien.com/signup
def aylienREST(title = '',
               text = '',
               num = 0,
               baseurl = 'https://api.aylien.com/api/v1/summarize'
               ):
    qtext = urllib.quote(text)
    qtitle = urllib.quote(title)
    print(qtext)
    print(qtitle)
    url = baseurl+"?"+"title="+qtitle+"&text="+qtext+"&sentences_number="+str(num)
    print(url)
    return safeGet2(url)

def getSummary(title, text, num):
    resp = aylienREST(title, text, num)
    if resp != None:
        dict = json.loads(resp.read())
        print(pretty(dict))
        if dict is not None and 'sentences' in dict:
            data = dict['sentences']
            print(data)
    return data

JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class MainHandler(webapp2.RequestHandler):
    def get(self):
        logging.info("In MainHandler")
        template_values = {}
        template_values['page_title'] = "Lyrics Summarizer"
        template = JINJA_ENVIRONMENT.get_template('greetform.html')
        self.response.write(template.render(template_values))

class GreetResponseHandlr(webapp2.RequestHandler):
    def post(self):
        vals = {"lyrics":[]}
        vals['page_title'] = "Search Results: "
        if input:
            title = self.request.get('title')
            artist = self.request.get('artist')
            num = self.request.get('num')
            vals['title'] = title
            vals['artist'] = artist
            vals['num'] = num
            go = self.request.get('gobtn')
            logging.info(title)
            logging.info(artist)
            logging.info(num)
            logging.info(go)
            if num is None:
                num = 3
            lyrics = getLyrics(title, artist)
            if lyrics is None:
                vals['error'] = "LOL, the song/artist combo you entered is not found!"
                template = JINJA_ENVIRONMENT.get_template('error.html')
                self.response.write(template.render(vals))
            else:
                sentences = makeSentences(lyrics)
                result = getSummary(title, sentences, num)
                # takes away the periods at the end of lines
                for line in result:
                    line = stripWordPunctuation(line)
                    #list.append(line)
                    vals['lyrics'].append(line)

                template = JINJA_ENVIRONMENT.get_template('greetresponse.html')
                self.response.write(template.render(vals))
        else:
            template = JINJA_ENVIRONMENT.get_template('greetform.html')
            self.response.write(template.render(vals))


application = webapp2.WSGIApplication([ \
    ('/gresponse', GreetResponseHandlr),
    ('/.*', MainHandler)
],
    debug=True)
