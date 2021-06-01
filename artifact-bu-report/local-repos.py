import requests,json

def getAllLocalRepos(host=None, headers=None):

    def _keys(obj):
        return obj['key']

    _path = "/artifactory/api/repositories?type=local"
    _url = host + _path
    _r = requests.get(_url, headers=headers)
    _repos = map(_keys, json.loads(_r.text))

    return list(_repos)