import csv, os

def findBuSvpEvp(user):
    svpEvpDetails = checkSvpEvpinCacheFile(user)

    if svpEvpDetails[0] == 'Info not in Cache file':
        with open('EmpInfo.csv', 'rb') as csvfile:
            empinfo_mapping = csv.reader(csvfile, quotechar='"', delimiter=',', quoting=csv.QUOTE_ALL, skipinitialspace=True)
            for row in empinfo_mapping:
                if user.lower() == row[0].lower():
                    if row[1] != '' and row[2] != '' and row[3] != '':
                        with open('EmpInfoCached.csv', 'a') as csvfileCached:
                            csvfileCached.write(user + ',' + row[1] + ',"' + row[2] + '","' + row[3] + '"\n')
                        return [row[1], row[2], row[3]]
        return ['Info not in AD', 'Info not in AD', 'Info not in AD']
    else:
        return svpEvpDetails

def checkSvpEvpinCacheFile(user):
    fileName = 'EmpInfoCached.csv'

    with open(fileName, 'rb') as csvfile:
        empinfo_mapping = csv.reader(csvfile, quotechar='"', delimiter=',', quoting=csv.QUOTE_ALL, skipinitialspace=True)
        for row in empinfo_mapping:
            if user.lower() == row[0].lower():
                if row[1] != '' and row[2] != '' and row[3] != '':
                    return [row[1], row[2], row[3]]
        return ['Info not in Cache file']
