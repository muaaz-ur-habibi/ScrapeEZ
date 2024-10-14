import sqlite3 as sql

class Presetter:
    def __init__(self, preset_name, preset_id):
        self.preset_name = preset_name
        self.preset_id = preset_id

    def create_and_save_preset(self,
                               url,
                               elements,
                               payloads,
                               parameters,
                               proxies):

        pass

    def get_preset(self,
                   id=None,
                   name=None):

        pass