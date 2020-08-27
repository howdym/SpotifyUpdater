# Information Schema:

# List of People (lop): Sorted array of people

# Dictionary of People (dop):
# {
#   (Insert Name Here):
#   {
#       Index: Index corresponding to person
#       ID: ID of Spotify Playlist
#       Unique: Number of unique songs
#   }
#   ^ repeat for each person
# }

# First row (first_row):
# {
#   Entries: len(Row entries), the number of unique songs
#   (Insert Name Here): len_playlist, Length of the playlist from specific person (see param)
#   ^ repeat for each person
# }

# Just run a for loop when making this: the people should be in alphabetical order

# Row entries:
# {
#   Name: Name of Song
#   Artists: Artists of Song
#   List: Index represents specific person; people go in alphabetical order. 1 for yes, 0 or no
#   Sum: How many people chose the song
# }

# Dictionary of row entries (lore):
# {
#   ID of Song: Row Entry for that Song
#   ^ repeat for all other songs
# }

import spotipy
import numpy as np
from spotipy.oauth2 import SpotifyClientCredentials


def show_tracks(tracks):
    for ay, item in enumerate(tracks['items']):
        track = item['track']
        print("   %d %32.32s %s" % (ay, track['artists'][0]['name'], track['name']))
    return len(tracks['items'])


class DataScraper:
    def __init__(self):
        self.dop = {}
        self.lop = []

        # Fill in
        self.tags = {"Person's Name": "ID to their public Spotify Playlist"}

        self.lore = {}
        self.sorted_lore_ids = []
        self.first_row = {}

        self.make_lop()
        self.make_dop()
        self.sorted_lore_ids = self.make_lore()
        self.update_dop()

    def make_lop(self):
        for k in self.tags.keys():
            self.lop.append(k)
        self.lop.sort()

    def make_dop(self):
        people = self.lop
        for index in range(len(people)):
            self.dop[people[index]] = {"Index": index,
                                       "ID": self.tags[people[index]],
                                       "Unique": 0}

    def make_re(self, person, tracks):
        for index, item in enumerate(tracks['items']):
            track = item['track']
            artists_names = ""
            for artists in track['artists']:
                artists_names += artists["name"] + ", "
            artists_names = artists_names[:-2]
            if track["id"] not in self.lore:
                self.lore[track["id"]] = {"Name": track['name'],
                                            "Artists": artists_names,
                                            "List": np.zeros(len(self.lop)),
                                            "Sum": 0}
            self.lore[track["id"]]["List"][self.dop[person]["Index"]] = 1
        return len(tracks['items'])

    def update_sums(self):
        for k, v in self.lore.items():
            self.lore[k]["Sum"] = np.sum(self.lore[k]["List"])

    def update_dop(self):
        for k in self.dop.keys():
            self.dop[k]["Unique"] = self.unique_songs(k)

    def unique_songs(self, person):
        counter = 0
        for key, re in self.lore.items():
            if re["List"][self.dop[person]["Index"]] == 1 and re["Sum"] == 1:
                counter += 1
        return counter

    # First row is also being made in this too
    def make_lore(self):
        client_credentials_manager = SpotifyClientCredentials("Get your API tokens!!!")
        sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
        for person in self.dop.keys():
            info = self.dop[person]
            pl = sp.playlist(info["ID"])
            results = sp.playlist(pl['id'],
                                  fields="tracks,next")
            tracks = results['tracks']
            len_playlist = self.make_re(person, tracks)
            self.first_row[person] = len_playlist
            while tracks['next']:
                tracks = sp.next(tracks)
                len_playlist = self.make_re(person, tracks)
                self.first_row[person] += len_playlist
        self.first_row["Entries"] = len(self.lore.keys())
        self.update_sums()

        sorted_ids = sorted(self.lore, key=lambda k: (-self.lore[k]['Sum'], self.lore[k]['Name']))
        return sorted_ids
