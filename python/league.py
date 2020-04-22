import hero
import json


class League:
    _FILENAME_SUFFIX = "_league.json"

    def __init__(self, leagueid, name, opendotajson, indexjson):
        # init
        self._leagueid = leagueid
        self._name = name
        self._opendotajson = opendotajson
        self._indexjson = indexjson
        self._herojson = {}
        # init league stats
        self._match_num = self._opendotajson.get_match_num()
        self._pickbans = {}
        self._pickbans_ranking = {}
        self.leaguejson = {}

        # init dictionary
        self._init_herojson()

        # make stats
        self._make_stats()

    def _make_stats(self):
        # match rootin
        for k, v in self._opendotajson.get_details().items():
            self._add_hero_pickbans(v['picks_bans'])

        # end of match rootin
        self._make_league_pickbans()

        # make_json
        self._make_leaguejson()
        self._make_herojson()

    def _make_league_pickbans(self):
        # order rootin
        for k, v in self._indexjson.pickbans.items():
            self._make_order_pickbans(k)

    def _make_order_pickbans(self, order):
        pickbans = {}
        for heroid, hero in self._herojson.items():
            pickbans[str(heroid)] = hero.get_pickbans(order)
        self._pickbans[str(order)] = pickbans

    def _add_hero_pickbans(self, pickbans):
        for v in pickbans:
            self._herojson[str(v['hero_id'])].add_pickbans(v['order'])

    def _init_herojson(self):
        for k, v in self._indexjson.opendota_heroes.items():
            self._herojson[k] = hero.Hero(k, v['name'], self._indexjson)

    def _make_leaguejson(self):
        self.leaguejson['match_num'] = self._match_num
        self.leaguejson['pickbans'] = self._pickbans

    def _make_herojson(self):
        self.leaguejson['heroes'] = {}
        for heroid, hero in self._herojson.items():
            self.leaguejson['heroes'][heroid] = hero.make_herojson()

    def write_json(self, folder_path):
        filename = str(self._leagueid) + self._FILENAME_SUFFIX
        filepath = folder_path / filename
        with open(filepath, mode='w') as f:
            json.dump(self.leaguejson, f, indent=4)

    def get_leaguejson(self):
        return self.leaguejson
