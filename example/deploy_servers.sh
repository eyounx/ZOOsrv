#!/usr/bin/expect -f

# This script is provided for automatic login and deploying servers.
# To use this shell script, users should modify the content and add customized command. 

set loginuser "username" 
set loginpass "yourpassword"
set terminal_address yourdirectory # e.g. /Julia-0.6.app/Contents/Resources/julia/bin/julia

set ipaddr "serverip" # e.g. "114.212.190.147"
set timeout 30

spawn ssh $loginuser@$ipaddr
# expect "*yes/no*" {send "yes\n"}

expect "*password:*" {send "$loginpass\r;"} # \r shouldn't be omitted
expect "Last login:*" {
    send "cd $terminal_address\r"
    # the script to start Distributed ZOOpt servers can be added.
    }

interact
exit
