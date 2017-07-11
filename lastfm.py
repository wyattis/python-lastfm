import requests as r

base_url = "http://ws.audioscrobbler.com/2.0/"

class RequestWrapper:
    def __init__(self, api_key, api_secret):
        self.api_key = api_key
        self.api_secret = api_secret
    
    def get_raw(self, url):
        response = r.get(url)
        return response.json()
    
    def get(self, method=None, params={}):
        params['method'] = method
        params['api_key'] = self.api_key
        params['format'] = 'json'
        response = r.get(base_url, params=params)
        return response.json()

class Facade:
    def __init__(self, wrapper):
        self.s = wrapper

class ArtistFacade(Facade):
    def getInfo(self, **kwargs):
        return self.s.get('artist.getinfo', kwargs)
    def getSimilar(self, **kwargs):
        return self.s.get('artist.getSimilar', kwargs)
    def getTopAlbums(self, **kwargs):
        return self.s.get('artist.gettopalbums', kwargs)
    def getTopTracks(self, **kwargs):
        return self.s.get('artist.gettoptracks', kwargs)
    def search(self, **kwargs):
        return self.s.get('artist.search', kwargs)

class AlbumFacade(Facade):
    def getInfo(self, **kwargs):
        return self.s.get('album.getinfo', kwargs)
    def getTopTags(self, **kwargs):
        return self.s.get('album.gettoptags', kwargs)
    def search(self, **kwargs):
        return self.s.get('album.search', kwargs)
    
class LastFM:
    
    def __init__(self, api_key=None, api_secret=None):
        import os
        api_key = api_key if api_key else os.getenv('LASTFM_API_KEY')
        api_secret = api_secret if api_secret else os.getenv('LASTFM_API_SECRET')
        self.wrapper = RequestWrapper(api_key, api_secret)
        self.album = AlbumFacade(self.wrapper)
        self.artist = ArtistFacade(self.wrapper)
    
    def next(self, response):
        if 'next' in response:
            return self.wrapper.get_raw(response['next'])
        else:
            return None