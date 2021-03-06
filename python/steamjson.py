import sys
import url
import json
import copy
from pathlib import Path


class SteamJson:
    _STEAMAPI_BASE = ("http://api.steampowered.com/"
                      "/IDOTA2Match_570"
                      "/GetMatchHistory/v1")
    _STEAMAPI_LEAGUE = "?league_id="
    _STEAMAPI_KEY = "&key="
    _STEAMAPI_REQUEST = "&matches_requested="
    _STEAMAPI_MAXREQUEST = 300
    _STEAMAPI_STARTID = "&start_at_match_id="
    _FILENAME_SUFFIX = "_steamapi.json"

    def __init__(self, leagueid, apikey, start_id, end_id, folder_path):
        self.matches = {}
        self.old_match_dict = {}
        self._leagueid = leagueid
        self._apikey = apikey
        self._start_id = start_id
        self._end_id = end_id
        ####
        self.read_old_steam_json(folder_path)
        self.make_matchid_json()

    def make_matchid_json(self):
        is_first = True
        next_id = -1
        while(True):
            has_next = False
            result = {}
            _url = self._make_steam_url(next_id)
            result = url.get_url(_url)
            sort_matches = self._sort_matches_api(result)

            self._add_match(sort_matches)
            if not self._has_next(sort_matches):
                break
            next_id = sort_matches[-1]['match_id']

    def _make_steam_url(self, start_id=-1):
        url = (self._STEAMAPI_BASE
               + self._STEAMAPI_LEAGUE
               + str(self._leagueid)
               + self._STEAMAPI_KEY
               + str(self._apikey)
               + self._STEAMAPI_REQUEST
               + str(self._STEAMAPI_MAXREQUEST))
        if start_id != -1:
            url += (self._STEAMAPI_STARTID
                    + str(start_id))
        return(url)

    def _sort_matches_api(self, result):
        sort_matches = (sorted(result['result']['matches'],
                        key=lambda x: x['match_id'],
                        reverse=True))
        return(sort_matches)

    def _has_next(self, matches):
        if len(matches) <= 1:
            return False
        else:
            return True

    def _add_match(self, matches):
        for match in matches:
            if match['lobby_type'] == 1:
                if ((int(self._start_id) <= int(match['match_id']))
                   and (int(match['match_id']) <= int(self._end_id))):
                    self.matches[match['match_id']] = copy.deepcopy(match)

    def write_json(self, folder_path):
        filename = str(self._leagueid) + self._FILENAME_SUFFIX
        filepath = folder_path / filename
        with open(filepath, mode='w') as f:
            json.dump(self.matches, f, indent=4)

    def get_matches(self):
        return self.matches

    def get_last_unixdate(self):
        return self.matches[next(iter(self.matches))]['start_time']

    def get_unixdate_arr(self):
        unixdate_arr = []
        for match_id, match in self.matches.items():
            unixdate_arr.append(match['start_time'])
        return unixdate_arr

    def read_old_steam_json(self, folder_path):
        filename = str(self._leagueid) + self._FILENAME_SUFFIX
        filepath = folder_path / filename
        try:
            with open(filepath, mode='r') as f:
                self.old_match_dict = json.load(f)
        except FileNotFoundError:
            self.old_match_dict = {}
            

    def is_matchlist_not_change(self,folder_path):
        # because writing encoding diff, reopen new json file
        filename = str(self._leagueid) + self._FILENAME_SUFFIX
        filepath = folder_path / filename
        with open(filepath, mode='r') as f:
            new_match_dict = json.load(f)

        if new_match_dict == self.old_match_dict:
            return True
        return False


if __name__ == "__main__":
    pass
