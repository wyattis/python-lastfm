import unittest
from lastfm import LastFM

class AlbumTestCase(unittest.TestCase):
    def setUp(self):
        self.fm = LastFM()
        self.artist_name = 'Wintersleep'
        self.album_name = "New Inheritors"
        self.album_mbid = '3f46329d-b15c-494b-912e-b802a5a8a3bb'
    def test_getInfo_by_mbid(self):
        info = self.fm.album.getInfo(mbid=self.album_mbid)
        self.assertEqual(self.album_mbid, info['album']['mbid'])
    def test_getInfo_by_name(self):
        info = self.fm.album.getInfo(artist=self.artist_name, album=self.album_name)
        self.assertEqual(self.album_mbid, info['album']['mbid'])
    def test_getTopTags_by_mbid(self):
        tags = self.fm.album.getTopTags(mbid=self.album_mbid)
        self.assertEqual({}, tags)
    def test_search(self):
        res = self.fm.album.search(album=self.album_name)
        self.assertTrue('results' in res)

class ArtistTestCase(unittest.TestCase):
    def setUp(self):
        self.fm = LastFM()
        self.artist_name = 'Wintersleep'
        self.artist_mbid = 'cda8e877-fe39-4939-8b09-045d68617367'
    def test_getInfo_by_mbid(self):
        info = self.fm.artist.getInfo(mbid=self.artist_mbid)
        self.assertEqual(self.artist_mbid, info['artist']['mbid'])
    def test_getInfo_by_name(self):
        info = self.fm.artist.getInfo(artist=self.artist_name)
        self.assertEqual(self.artist_mbid, info['artist']['mbid'])
    def test_getTopTracks(self):
        res = self.fm.artist.getTopTracks(mbid=self.artist_mbid)
        self.assertTrue('toptracks' in res)
    def test_getTopAlbums(self):
        res = self.fm.artist.getTopAlbums(mbid=self.artist_mbid)
        self.assertTrue('topalbums' in res)
    def test_search(self):
        res = self.fm.artist.search(artist=self.artist_name)
        self.assertTrue('results' in res)
        
class TrackTestCase(unittest.TestCase):
    def setUp(self):
        self.fm = LastFM()
        self.artist_name = "Wintersleep"
        self.artist_mbid = 'cda8e877-fe39-4939-8b09-045d68617367'
        self.track_name = "Jaws of Life"
        self.album_name = "Untitled"
        self.track_mbid = 'e0b110b4-fef4-473a-9c42-207d3c92cae0'
    def test_getInfo_by_mbid(self):
        res = self.fm.track.getInfo(mbid=self.track_mbid)
        self.assertEqual(self.track_mbid, res['track']['mbid'])
    def test_getInfo_by_name(self):
        res = self.fm.track.getInfo(artist=self.artist_name, track=self.track_name)
        self.assertEqual(self.track_mbid, res['track']['mbid'])

class PaginateTestCase(unittest.TestCase):
    def setUp(self):
        self.fm = LastFM()
        self.query = 'winter'
    def page(self, results):
        new_results = self.fm.next_page(results)
        self.assertTrue(results != None)
        self.assertTrue(new_results != None)
        self.assertTrue(results['results']['opensearch:startIndex'] != new_results['results']['opensearch:startIndex'])
    def test_artist_page_results(self):
        self.page(self.fm.artist.search(artist=self.query))
    def test_album_page_results(self):
        self.page(self.fm.album.search(album=self.query))
    def test_track_page_results(self):
        self.page(self.fm.track.search(track=self.query))

if __name__ == '__main__':
    unittest.main()