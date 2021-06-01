import csv, ldap, yaml

def findArtifactOwnerDetails(_artifact_owner):
    with open("config.yml", 'r') as ymlfile:
        cfg = yaml.load(ymlfile)

    ldapUrl = cfg['ldap']['url']
    ldapUsername = cfg['ldap']['username']
    ldapPassword = cfg['ldap']['password']

    # Check in local file if the details already cached
    _artifact_owner_details = checkDepartmentInCahceFile(_artifact_owner)
    #print(local_ldap_details)

    if _artifact_owner_details[0] == 'Absent in local file':
        # If not present in local file, get it from ldap
        # and write it to cache file
        _artifact_owner_details = findManagerDepComp(_artifact_owner, ldapUrl, ldapUsername, ldapPassword)
        #print(_artifact_owner_details)

    return _artifact_owner_details

def checkDepartmentInCahceFile(user):
    with open('ldap_details_cached.csv', 'rb') as csvfile:
        ldap_details = csv.reader(csvfile, delimiter=',')
        for row in ldap_details:
            if user == row[0]:
                return [user, row[1], row[2], row[3]]
    return ['Absent in local file']

def findManagerDepComp(user, ldapUrl, ldapUsername, ldapPassword):

    l = ldap.initialize(ldapUrl)

    baseDN = "dc=ca,dc=com"
    searchScope = ldap.SCOPE_SUBTREE
    ## retrieve all attributes
    retrieveAttributes = ['department', 'company', 'manager']
    searchFilter = "cn=" + user

    try:
        l.protocol_version = ldap.VERSION3
        l.set_option(ldap.OPT_NETWORK_TIMEOUT, 3.0)
        l.set_option(ldap.OPT_TIMEOUT, 3)
        l.simple_bind_s(ldapUsername, ldapPassword)
        ldap_result_id = l.search(baseDN, searchScope, searchFilter, retrieveAttributes)
        result_set = []
        result_type, result_data = l.result(ldap_result_id, 0)
        #print(result_data[0][0], result_type)

        file = open("ldap_details_cached.csv","a")
        if (result_data == []):
            # If response is empty, return empty
            empty='Info not in AD'
            file.write(user + ',' + empty + ',' + empty + ',' + empty + '\n')
            file.close()
            return [user,empty,empty,empty]
        elif (result_data[0][0] == None):
            # If actual object is None, return empty
            empty='Info not in AD'
            file.write(user + ',' + empty + ',' + empty + ',' + empty + '\n')
            file.close()
            return [empty,empty,empty,empty]
        else:
            if result_type == ldap.RES_SEARCH_ENTRY:
                result_set.append(result_data)

        if 'department' in result_set[0][0][1]:
            _dep = result_set[0][0][1]['department'][0].split('-')[1].strip()
        else:
            _dep = "Department not found in AD"

        if 'company' in result_set[0][0][1]:
            _comp = result_set[0][0][1]['company'][0].split('-')[1].strip()
        else:
            _comp = "Company not found in AD"

        if 'manager' in result_set[0][0][1]:
            _manager = result_set[0][0][1]['manager'][0].split('=')[1].split(',')[0]
        else:
            _manager = "Manager not found in AD"

        file.write(user + ',' + _dep + ',' + _comp + ',' + _manager + '\n')
        file.close()

        return [user, _dep, _comp, _manager]
    except Exception as error:
        print(error)