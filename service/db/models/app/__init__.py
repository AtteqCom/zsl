from json import JSONEncoder

class AppModel:
    def __init__(self, raw):
        for (k, v) in raw.items():
            if not isinstance(v, (type(None), str, int, long, float, bool, unicode)):
                continue
            setattr(self, k, v)

class SportClub(AppModel):
    pass

class Sport(AppModel):
    pass

class State(AppModel):
    pass

class AppModelJSONEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, AppModel):
            return o.__dict__
        else:
            return JSONEncoder.default(self, o)
