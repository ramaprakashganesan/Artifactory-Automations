import requests, json, ldap, sys, datetime, re, csv, yaml
import argparse
from multiprocessing import Pool
from get_artifacts import getArtifactsOfRepo

reload(sys)
sys.setdefaultencoding('utf8')

if __name__ == '__main__':
    start_time_obj = datetime.datetime.now()
    start_time = start_time_obj.strftime("%y-%m-%d-%H-%M-%S")
    script_date = start_time_obj.strftime("%y-%m-%d")

    with open("config.yml", 'r') as ymlfile:
        cfg = yaml.load(ymlfile)

    headers = {'Authorization': 'Basic ' + cfg['artifactory']['basic_auth_token']}

    parser = argparse.ArgumentParser(description='Artifactory Storage Report')
    parser.add_argument('--url', dest='url', default="http://xxxxx.ca.com")
    parser.add_argument('--repo', dest='repo', required=True)
    parser.add_argument('--limit', dest='limit', type=int, default=1000)

    args = parser.parse_args()

    file1 = open("artifact-size-" + script_date + ".log","a")
    file1.write('Script started for %s: %s\n' % (args.repo, start_time))

    getArtifactsOfRepo(args.repo, args.url, headers, args.limit)

    end_time_obj = datetime.datetime.now()
    end_time = end_time_obj.strftime("%y-%m-%d-%H-%M-%S")

    file1.write('Script ended for %s: %s\n' % (args.repo, end_time))
    file1.write('Time taken for %s: %s seconds\n' % (args.repo, (end_time_obj - start_time_obj).total_seconds()))
    file1.write('----------------------------------------------\n')
    file1.close()
