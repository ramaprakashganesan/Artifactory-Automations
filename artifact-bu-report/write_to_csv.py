from find_artifact_owner import findArtifactOwner
from find_artifact_owner_details import findArtifactOwnerDetails
from find_svp_evp import findBuSvpEvp

def convertToCsv(_artifact):
    #print(_artifact)
    _artifact_name = _artifact['name']
    _artifact_size = str(format(float(_artifact['size'])/1024/1024, '.6f'))
    _artifact_repo = _artifact['repo']
    _artifact_path = _artifact['path']
    _artifact_modified = _artifact['modified']
    _artifact_user = _artifact['modified_by']

    # Find the owner account of the deployer
    _artifact_owner = findArtifactOwner(_artifact_user)

    if _artifact_owner == 'Info not in AD':
        # Fill Artifact Owner's Department, Manager,
        # SVP, EVP details as empty when artifact owner not found
        _artifact_owner_details = [_artifact_owner,_artifact_owner,_artifact_owner,_artifact_owner]
        bu_svp_evp_details = [_artifact_owner, _artifact_owner, _artifact_owner]
    else:
    # Find the department, manager of the user
        _artifact_owner_details = findArtifactOwnerDetails(_artifact_owner)

        # Get BU, SVP, EVP Details
        bu_svp_evp_details = findBuSvpEvp(_artifact_owner)
        #print(bu_svp_evp_details)

    # If downloaded info not available mark it as Never Downloaded
    if 'stats' in _artifact:
        _artifact_downloaded = _artifact['stats'][0]['downloaded']
    else:
        _artifact_downloaded = "Never downloaded"

    print(_artifact_repo + ',' + _artifact_size + \
        ',' + _artifact_modified + ',' + \
        _artifact_downloaded + ',' + _artifact_user + \
        ',' + bu_svp_evp_details[0] + \
        ',"' + bu_svp_evp_details[1] + '","' + bu_svp_evp_details[2]) + '"'