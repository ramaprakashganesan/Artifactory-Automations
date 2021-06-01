import re,csv

def findArtifactOwner(_artifact_user):
    _artifact_owner = None

    pattern = re.compile('^[a-z]{5}[0-9]{2}$')

    # If deployer is not generic account, deployer and owner is same
    if pattern.match(_artifact_user):
        _artifact_owner = _artifact_user
    # If deployer is generic account find owner from local csv file
    else:
        _artifact_owner = findGenericAccountOwner(_artifact_user)

    return _artifact_owner

def findGenericAccountOwner(user):
    with open('generic_owners.csv', 'rb') as csvfile:
        accounts_mapping = csv.reader(csvfile, delimiter=',')
        for row in accounts_mapping:
            if user == row[0]:
                if row[1] != '':
                    return row[1]
    return 'Info not in AD'