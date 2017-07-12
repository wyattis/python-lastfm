import requests as r

base_url = "http://ws.audioscrobbler.com/2.0/"


class RequestWrapper:
    """
    Used to wrap basic requests made by the requests lib that will add lastfm
    api_keys and other required info.
    """
    def __init__(self, api_key, api_secret):
        self.api_key = api_key
        self.api_secret = api_secret
        
    
    def get_raw(self, url):
        """Just get response from the provided url. No edits to request are made"""
        response = r.get(url)
        return response.json()
    
    def handle_retry(self, result):
        """TODO: In the event of API calls exceeding the acceptable rate this function will handle retrying the call again."""
        if 'error' in result and result['error'] is 29:
            print('Should retry, but currently does not')
        return result
    
    def get(self, method=None, params={}):
        """Add the method, api_key and format to the request parameters"""
        params['method'] = method
        params['api_key'] = self.api_key
        params['format'] = 'json'
        try:
            response = r.get(base_url, params=params)
            result = response.json()
        except Exception as e:
            raise e
        return self.handle_retry(result)

class Facade:
    """Abstract Base Facade that is inherited from for all other Facades"""
    def __init__(self, wrapper):
        self.s = wrapper

class ArtistFacade(Facade):
    """Artist facade class to define methods that follow the API structure."""
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

class TrackFacade(Facade):
    """Track facade class to define methods that follow the API structure."""
    def getInfo(self, **kwargs):
        return self.s.get('track.getInfo', kwargs)
    def getSimilar(self, **kwargs):
        return self.s.get('track.getSimilar', kwargs)
    def getTopTags(self, **kwargs):
        return self.s.get('track.getTopTags', kwargs)
    def search(self, **kwargs):
        return self.s.get('track.search', kwargs)

class AlbumFacade(Facade):
    """Album facade class to define methods that follow the API structure."""
    def getInfo(self, **kwargs):
        return self.s.get('album.getinfo', kwargs)
    def getTopTags(self, **kwargs):
        return self.s.get('album.gettoptags', kwargs)
    def search(self, **kwargs):
        return self.s.get('album.search', kwargs)
    
class LastFM():
    """
    Class that simulates the semantics of the lastfm API. Requires an API key
    to be passed in or supplied as an env variable called LASTFM_API_KEY.
    Making API requests then simply follows the semantics demonstrated in the
    [LastFM](http://www.last.fm/api/) documentation.
    """
    def __init__(self, api_key=None, api_secret=None):
        import os
        api_key = api_key if api_key else os.getenv('LASTFM_API_KEY')
        api_secret = api_secret if api_secret else os.getenv('LASTFM_API_SECRET')
        self.wrapper = RequestWrapper(api_key, api_secret)
        self.album = AlbumFacade(self.wrapper)
        self.artist = ArtistFacade(self.wrapper)
        self.track = TrackFacade(self.wrapper)
    
    def page(self, response, increment):
        """
            Pull out the important variables from the response and change them 
            to increment to the next page.
        """
        if 'results' in response:
            r = response['results']
            total_results = int(r['opensearch:totalResults'])
            page =int(r['opensearch:Query']['startPage'])
            start_index = int(r['opensearch:startIndex'])
            limit = int(r['opensearch:itemsPerPage'])
            search_terms = r['opensearch:Query']['searchTerms']
            
            # Check if we're going to exceed the number of results
            if start_index + increment * limit >= total_results:
                return None
            
            if 'artistmatches' in r:
                base = self.artist
                query_type='artist'
            elif 'albummatches' in r:
                base = self.album
                query_type='album'
            elif 'trackmatches' in r:
                base = self.track
                query_type='track'
                
            p = {}
            p[query_type] = search_terms
            p['limit'] = limit
            p['page'] = page + increment
            return base.search(**p)
        else:
            return None
    
    def next_page(self, response):
        """Get the next page of results in a response object with multiple pages."""
        return self.page(response, 1)
    
    def prev_page(self, response):
        """Get the previous page of results in a response object with multiple pages"""
        return self.page(response, -1)