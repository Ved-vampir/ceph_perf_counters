#!/bin/bash

set -e
set -o pipefail

if [[ $# < 2 ]]
    then 
        echo "Fuel host and environment name are required"
        exit 1
fi

fuel_host=$1
env_name="$2"

echo "You need to know fuel node root password!"
echo "You need use rsa key (you must create it, if you haven't). id_rsa used by default"

# Get access to fuel node by ssh
ssh-copy-id root@$fuel_host

# Copy key on fuel node 
scp ~/.ssh/id_rsa.pub root@$fuel_host:/root/my_temp_rsa.pub

# Get environment id from fuel by it's name
env_id=$(ssh root@$fuel_host fuel env | awk  -v en=$env_name '
    {
        if (($1 !~ /-/) && (NR!=1) && ($5 ~ en)) {
         print $1 
        }
    }')

# If something isn't ok
if [[ $env_id == "" ]]
    then 
        echo "Cannot find such environment!"
        exit 1
fi

ip_list=$(ssh root@$fuel_host fuel --env-id $env_id  node list | awk  '
    {
        if ((NR!=1) && (NR!=2)) {
         print $9 
        }
    }')

for ip in $ip_list
do
    ssh root@$fuel_host ssh-copy-id -i /root/my_temp_rsa.pub root@$ip
done    
