# Artifactory Automations

## Aritfactoy BU Report
### This script will give the list of all the artifacts in artifactory in csv format as below

Artifact Name, Size, Repository, Path, Last Download Time, Generic/PMF Key Account Used to Deploy, PMF Key's Owner, Owner's Manager, Owner's Project, Owner's Department  

Requirements to run the script:
* Linux
* python2

### clone the repo
### cd into repo
### cd into artifact-bu-report
### pip install -r requirements.txt
this may be pip3 depends on your python installation
### bash get-all-artifact-size-and-user-details.sh <artifactory_home_url> <output_dir>
example: bash get-all-artifact-size-and-user-details.sh https://xxxxx.ca.com output

This will start multiple python process, each for a repository. Each process will create csv file. One file for one repository. You can find out if the script is running or complete by checking the status by doing "ps -ef | grep python"

After the script has been completed, you can move to the "output" directory and aggregate all the results into single file.
```
cd output
cat * > artifactory_report.csv
```

if you get python not found error, put your correct python exeuctable file name in the shell script

## Finding Upload and Download Times of Artifacts
Requirements to run the script:
* Linux
* Bash
### Clone the repo
### cd into repo
### cd into find_uplaod_download_times.sh
### bash initial-setup.sh <location>
<location> is the location from where you are running the script
example: bash initial-setup.sh elmsford
### bash find_upload_download_time.sh <location>
example: bash find_upload_download_time.sh elmsford
