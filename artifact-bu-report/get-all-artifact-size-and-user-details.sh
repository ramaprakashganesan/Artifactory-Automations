#!/bin/bash

if [ -z $1 ]; then
    echo "WARNING: Please provide Artifactory Home URL as first parameter"
    exit 1
fi

if [ -z $2 ]; then
    echo "WARNING: Please provide directory name to store output as parameter"
    exit 1
fi

artifactory_url="${1}/artifactory/api/repositories?type=local"
all_repos=`curl ${artifactory_url}`
curl http://xxxxx.ca.com/artifactory/p2-local/third-party/parsers/jq/jq-linux64 -o jq
chmod +x jq
export PATH=.:$PATH

if jq -e . >/dev/null 2>&1 <<<"$all_repos"; then
    echo "Parsed repos JSON successfully and got something other than false/null"
else
    echo "ERROR: Failed to parse repos JSON, or got false/null"
    exit 1
fi

mapfile -t lines < <(echo $all_repos | jq -r ".[].key")

if [ -d $2 ]; then
    echo "ERROR: Output directory already exists, please check"
    exit 1
fi

mkdir $2
for i in "${lines[@]}"
do
    nohup python main.py --url $1 --repo $i > ${2}/${i}.csv &
done
