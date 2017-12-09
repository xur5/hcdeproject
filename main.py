
import webapp2, urllib, urllib2, webbrowser, json
import jinja2
import flickr_key
import os


# FLICKR_KEY = 'b5649f05223a5e2eaae47bad728c7982'
#


#
# class MainHandler(webapp2.RequestHandler):
#     def get(self):
#         logging.info("In MainHandler")
#
#         template_values = {}
#         template_values['page_title'] = "Music Cover Search by Lyrics"
#         template = JINJA_ENVIRONMENT.get_template('greetform.html')
#         self.response.write(template.render(template_values))

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

def flickrREST(baseurl = 'https://api.flickr.com/services/rest/',
               method = 'flickr.photos.search',
               api_key = flickr_key.key,
               format = 'json',
               params={},
               ):
    params['method'] = method
    params['api_key'] = api_key
    params['format'] = format
    if format == "json": params["nojsoncallback"]=True
    url = baseurl + "?" + urllib.urlencode(params)
    return safeGet(url)
#
# class Photo:
#     def __init__(self, d):
#         self.title = d['title']['_content']
#         self.author = d['owner']['username']
#         self.userid = d['owner']['nsid']
#         self.tags = [item['_content'] for item in d['tags']['tag']]
#         self.commentcount = int(d['comments']['_content'])
#         self.numViews = int(d['views'])
#         self.url = d['urls']['url'][0]['_content']
#         self.thumbnailURL = "https://farm"+str(d['farm'])+".staticflickr.com/"+str(d['server'])+"/"+str(d['id'])+"_"+\
#                             str(d['secret'])+"_q.jpg"
#     def __str__(self):
#         result = "~~~ "+self.title+" ~~~"+"\nauthor: "+self.author+"\nnumber of tags: "+str(len(self.tags))+"\nviews: "\
#                  +str(self.numViews)+"\ncomments: "+str(self.commentcount)
#         return result

def pretty(obj):
    return json.dumps(obj, sort_keys=True, indent=2)

# title = "ride"
# artist = "lana del rey"
def getLyrics(title, artist):
    resp = musREST(params = {'q_track': title, 'q_artist': artist})
    if resp != None:
        dict = json.loads(resp.read())
        print(pretty(dict))
        if dict is not None and 'lyrics' in dict['message']['body']:
            data = dict['message']['body']['lyrics']['lyrics_body']
            words = data.split("*******")[0].split("...")[0]
            #words = words[:-1] #.lower().split()
            return words

    return None

text = "I've been out on that open road.\n You can be my full time daddy, white and gold.\n Singing blues has been getting old.\n But you can be my full time baby, hot or cold.\n Don't break me down.\n I've been traveling too long.\n I've been trying too hard.\n With one pretty song.\n I hear the birds on the summer breeze. \nI drive fast. I am alone at midnight. \nBeen trying hard not to get into trouble. \nBut I, I've got a war in my mind. \nSo, I just ride. Just ride."

# from aylienapiclient import textapi
# client = textapi.Client('25777ab7', '93d253c5f5b915779ab649b119cf7d09')
# summary = client.Summarize({'title': 'lana', 'text':text})

# def loadStopwords():
#     stopwords = {}
#     with open('stopwords.txt','r') as f:
#         for line in f:
#             stopwords[line.rstrip().lower()] = True
#     return stopwords
#
# def wordFreqs():
#     freqs = {}
#     sw = loadStopwords()
#     for word in words:
#         word = stripWordPunctuation(word)
#         print (word)
#
#         if word not in sw:
#             freqs[word] = freqs.get(word, 0)
#             freqs[word] += 1
#     return freqs
# def makeSentences(words):
#     words = words.replace('\n', '. ')
#     return words
#
# lyrics = getLyrics(title, artist)
# sentences = ''
# if lyrics == None:
#     print ("Sorry, we cannot find the song with the combo you entered. :( Please try again.")
# else:
#     print(lyrics)
#     sentences = makeSentences(lyrics)
#     print
# string
# Article or webpage URL
# title:	string
# Title of the text to summarize
# text:	string
# Text to summarize
# sentences_number:	integer5
# Summary length as number of sentences
# sentences_percentage:	integer
# Summary length as percentage of original document
def safeGet2(url, data):
    try:
        headers = {'Accept':'text/xml',
                   'X-AYLIEN-TextAPI-Application-ID':'25777ab7',
                   'X-AYLIEN-TextAPI-Application-Key': '93d253c5f5b915779ab649b119cf7d09',
                   'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
                  }
        req = urllib2.Request(url, data, headers)
        #req.add_header(headers)
        return urllib2.urlopen(req)
    except urllib2.URLError, e:
        if hasattr(e,"code"):
            print "The server couldn't fulfill the request."
            print "Error code: ", e.code
        elif hasattr(e,'reason'):
            print "We failed to reach a server"
            print "Reason: ", e.reason
        return None

title = "ride"
artist = "lana del rey"
def aylienREST(baseurl = 'https://api.aylien.com/api/v1/summarize',
               params={'title': title, 'text': text, 'sentences_number': '5'},
               ):
    url = baseurl + "?"  #urllib.urlencode(params)
    print(url)
    return safeGet2(url, params)

def getSummary():
    resp = aylienREST(params={})
    if resp != None:
        dict = json.loads(resp.read())
        print(pretty(dict))
        if dict is not None and 'sentences' in dict:
            data = dict['sentences']
            print(data)


getSummary()




    # fDict = wordFreqs()
    # sortedList = sorted(fDict.items(), key=lambda x: x[1], reverse=True)
    # print(sortedList)


def getPhotoIDs(tags="Seattle", n=100):
    resp = flickrREST(params={"tags": tags, "per_page": n})
    if resp is not None:
        photosdict = json.loads(resp.read())['photos']
        if photosdict is not None:
            if 'photo' in photosdict and len(photosdict['photo']) > 0:
                return [photo['id'] for photo in photosdict['photo']]
    return None

def getPhotoInfo(photo_id):
    data_retrieved = flickrREST(method="flickr.photos.getInfo", params=({'photo_id': photo_id}))
    if (data_retrieved != None):
        data_read = data_retrieved.read()
        data_load = json.loads(data_read)
        return data_load['photo']
    else:
        return None


def get_photo_sizes(photo_id):
    data_retrieved = flickrREST(method="flickr.photos.getSizes", params=({'photo_id': photo_id}))
    if (data_retrieved != None):
        jsonresult = data_retrieved.read()
        d = json.loads(jsonresult)
        d = d['sizes']['size'][2]['source']
    return d

#
# class Photo():
#     def __init__(self, photosdict):
#         self.title = photosdict['title']['_content'].encode('utf-8')
#         self.author = photosdict['owner']['username'].encode('utf-8')
#         self.userid = photosdict['owner']['nsid']
#         self.tags = [tag['_content'] for tag in photosdict['tags']['tag']]
#         self.numViews = int(photosdict['views'])
#         self.commentcount = int(photosdict['comments']['_content'])
#         self.url = photosdict['urls']['url'][0]['_content']
#         self.photo_url = get_photo_sizes(photosdict['id'])
#
#     def __str__(self):
#         s = "Title: %s / Author: %s" % (self.title, self.author)
#
#     def open_url(self):
#         webbrowser.open(self.url)

# tag = "lana"
#
# photos = [Photo(getPhotoInfo(pid)) for pid in getPhotoIDs("lana")]
#
# print("\nTop Three Photos by Views")
# print("------------")
# byviews = sorted(photos, key=lambda x: x.numViews, reverse=True)
# for photo in byviews[:5]:
#     print(photo)
#
# # (b) Order the photo objects by number of tags. Print the three most tagged photos
# print("\nTop Three Photos by Number of Tags")
# print("------------")
#
# bytags = sorted(photos, key=lambda x: len(x.tags), reverse=True)
# for photo in bytags[:5]:
#     print(photo)
#
# # (c) Order the photo objects by number of tags. Print the three most commented photos
# # NOTE: it is completely possible that you will have no photos with comments in your data set.
#
# print("\nTop Three Photos by Number of Comments")
# print("------------")
#
# bycomments = sorted(photos, key=lambda x: x.commentcount, reverse=True)
# for photo in bycomments[:5]:
#     print(photo)
#
#
JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
                                       extensions=['jinja2.ext.autoescape'],
                                       autoescape=True)

tvals = {'results': {}, 'song': title, 'artist': artist, 'text': text }
# byviews
tvals['results']['title'] = title
tvals['results']['artist'] = artist
tvals['results']['text'] = text
# tvals['results']['summary'] = summary

# print(tvals)
f = open("response.html", 'w')
template = JINJA_ENVIRONMENT.get_template('greetform.html')
f.write(template.render(tvals))
f.close()

#
# class GreetResponseHandlr(webapp2.RequestHandler):
#     def post(self):
#         latlng = self.request.headers.get("X-AppEngine-CityLatLong", None)
#         vals = {}
#         tag = self.request.get('tag')
#         vals['page_title'] = "Flickr Tag Search Results: " + tag
#
#         if tag:
#             tag = self.request.get('tag')
#             vals['tag'] = tag
#             photos = [Photo(get_photo_info(photo_id)) for photo_id in get_photo_ids(tag, latlng)]
#
#             # Top Five Photos by Views
#             topviews = sorted(photos, key=lambda x: x.num_views, reverse=True)
#             topfiveviews = []
#             for photo in topviews[:5]:
#                 topfiveviews.append(photo)
#             vals['topfiveviews'] = topfiveviews
#
#             # The photo with the highest number of tags
#             toptags = sorted(photos, key=lambda x: len(x.tags), reverse=True)
#             toponetags = toptags[0]
#             vals['toponetags'] = toponetags
#
#             # The photo with the highest number of comments
#             topcomments = sorted(photos, key=lambda x: x.commentcount, reverse=True)
#             toponecomments = topcomments[0]
#             vals['toponecomments'] = toponecomments
#
#             template = JINJA_ENVIRONMENT.get_template('greetresponse.html')
#             self.response.write(template.render(vals))
#         else:
#             template = JINJA_ENVIRONMENT.get_template('greetform.html')
#             self.response.write(template.render(vals))
#
#
# application = webapp2.WSGIApplication([ \
#     ('/gresponse', GreetResponseHandlr),
#     ('/.*', MainHandler)
# ],
#     debug=True)