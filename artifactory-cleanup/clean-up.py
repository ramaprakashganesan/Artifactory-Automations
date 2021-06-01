import requests, json, sys, re, csv, yaml
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
import argparse

reload(sys)
sys.setdefaultencoding('utf8')

def findDate(old):

    if old[-1:].isalpha():
        oldDate = ""

        if old[-1:] == 'm':
            oldDate = (date.today() + relativedelta(months=-int(old[:-1]))).strftime("%Y-%m-%d")
        if old[-1:] == 'd':
            oldDate = (date.today() + relativedelta(days=-int(old[:-1]))).strftime("%Y-%m-%d")
    else:
        raise Exception("Input to find out cut off date should be few digits and a character(m or d)!")

    return oldDate

def deleteArtifacts(baseUrl, repo, folder, artifact, headers):
    _url = baseUrl + "/artifactory/" + repo + "/" + folder + "/" + artifact
    try:
        _r = requests.delete(_url, headers=headers)
        if (_r.status_code == 204):
            print(_url + " artifact has been deleted!")
    except Exception as error:
        print(error)
        exit(1)

def findArtifacts(baseUrl, repo, folder, old, headers, limit=1000):
    # Use Artifactory AQL Rest API to fetch all the artifacts of a given repo
    _path = "/artifactory/api/search/aql"
    _url = baseUrl + _path
    _created = findDate(old)

    # Form AQL Query
    _payload = 'items.find({' + \
        '"type" : "file",' + \
        '"repo" : "' + repo + '",' + \
        '"path" : "' + folder + '",' + \
        '"created" : {"$lt":"' + _created + 'T"}' + \
        '}).include("name","repo","path","size","created")'

    # Call Artifactory AQL Rest API
    try:
        _r = requests.post(_url, headers=headers, data=_payload)
        res = json.loads(_r.text)
        if isinstance(res, dict):
            for artifact in res['results']:
                print artifact['name']
                deleteArtifacts(baseUrl, repo, folder, artifact['name'], headers)
        else:
            print("Got unparsable response...")
    except Exception as error:
        print(error)
        exit(1)

if __name__ == '__main__':
    start_time_obj = datetime.now()
    start_time = start_time_obj.strftime("%y-%m-%d-%H-%M-%S")
    script_date = start_time_obj.strftime("%y-%m-%d")

    parser = argparse.ArgumentParser(description='Artifactory Cleanup Script. \
        To delete 6 months old artifacts, \
        Example: python clean-up.py --repo <repo_name> --folder <folder_path> \
        --apikey <api_key> --old 6m')
    parser.add_argument('--url', dest='url', default="https://isl-dsdc.ca.com")
    parser.add_argument('--repo', dest='repo', required=True)
    parser.add_argument('--folder', dest='folder', required=True)
    parser.add_argument('--old', dest='old', type=str, required=True)
    parser.add_argument('--apikey', dest='apikey', required=True)

    args = parser.parse_args()

    headers = {
        'X-JFrog-Art-Api': args.apikey
    }

    if (args.folder == '.'):
        print("Folder cannot be dot")
        exit(1)

    print('Script started for %s: %s\n' % (args.repo, start_time))

    findArtifacts(args.url, args.repo, args.folder, args.old, headers)

    end_time_obj = datetime.now()
    end_time = end_time_obj.strftime("%y-%m-%d-%H-%M-%S")

    print('')
    print('Script ended for %s: %s\n' % (args.repo, end_time))
    print('Time taken for %s: %s seconds\n' % (args.repo, (end_time_obj - start_time_obj).total_seconds()))
    print('----------------------------------------------\n')