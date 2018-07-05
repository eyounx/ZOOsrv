#! /bin/bash

# This script is provided for automatic login and deploying servers.
# To use this shell script, users should modify the content and add customized command. 

# TODO: These variables should be set by users
login_clusters=("c01n04" "c01n06")
password="lamdaer"
script="~/liuyr/ZOOsrv/example/deploy_servers.exp"

len=${#login_clusters[@]}

for ((i=0; i<${len}; ++i))
do
    expect ${script} ${login_clusters[$i]} ${password} &
done
