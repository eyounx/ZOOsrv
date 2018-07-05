#! /bin/bash

# This script is provided for automatic login and deploying servers.
# To use this shell script, users should modify the content and add customized command.

# These variables should be set by users.
server="lamda@114.212.190.147"
script="~/liuyr/ZOOsrv/example/deploy_servers.sh"

ssh -tt ${server} <<-'ENDSSH'
	bash ${script}
ENDSSH
exit