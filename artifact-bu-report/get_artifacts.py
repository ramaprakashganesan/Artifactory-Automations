import requests, json
from write_to_csv import convertToCsv

def getArtifactsOfRepo(_repo=None, host=None, headers=None, limit=1000):
    # print("Fetching details of " + _repo + " Repository...")

    # Initial Offset
    offset = 0

    # Use Artifactory AQL Rest API to fetch all the artifacts of a given repo
    _path = "/artifactory/api/search/aql"
    _url = host + _path

    # Form AQL Query
    _part1 = """items.find({
        "type" : "file",
        "repo" : " """
    _part2 =  _repo
    _part3 = """"}).include("name","repo","path","size","modified","modified_by","stat.downloaded")
       .sort({"$desc": ["size"]})"""

    _payload = _part1 + _part2 + _part3 + \
        ".offset(" + str(offset) + ").limit(" + str(limit) + ")"

    # Start with offset 0
    getArtifactsList(_url, headers, _payload)

    offset += 1

    totalRepoCount = findRepoCount(_repo, host, headers)
    while (offset < totalRepoCount):
        # Loop until offest reaches total repository artifact count
        offset += limit
        _payload = _part1 + _part2 + _part3 + \
            ".offset(" + str(offset) + ").limit(" + str(limit) + ")"
        getArtifactsList(_url, headers, _payload)

def getArtifactsList(url, headers, data):
    # Call Artifactory AQL Rest API
    try:
        _r = requests.post(url, headers=headers, data=data)
        res = json.loads(_r.text)
        if isinstance(res, dict):
            for artifact in res['results']:
            # Loop the response and pass each artifact to convertToCsv function
                convertToCsv(artifact)
        else:
            print("Got unparsable response...")
    except Exception as error:
        print(error)

def findRepoCount(repo, host, headers):
    # Use Artifactory Storage Info Rest API to find the count of given repo
    _path = "/artifactory/api/storageinfo"
    _url = host + _path

    try:
        _r = requests.get(_url, headers=headers)
        res = json.loads(_r.text)
        for repoData in res['storageSummary']['repositoriesSummaryList']:
            if (repoData['repoKey'] == repo) and (repoData['repoType'] == 'LOCAL'):
                return repoData['filesCount']
    except Exception as error:
        print(error)