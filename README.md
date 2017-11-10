# Linux Commands:

List Attached Volumes with No Disk Label (No Filesystem)

    echo `eval sudo parted --list | grep "unrecognised disk label" | awk -F ':' '{print $2}' | sed "s/^[ \t]*//"` 

Cat all files in a directory and append filename above output

    tail -n +1 * 

List processes and their associated memory utilization in human readable form

    ps -eo size,command --sort -size | awk '{ print $1/1024,"Mb", $2}' 

# AWS Commands:

List instances associated with a particular Security Group

    aws ec2 describe-instances --region us-east-1 --output json | jq '.Reservations[] | ( .Instances[] | { InstanceId, SecurityGroups} ) | .InstanceId as $InstanceId | .SecurityGroups[] | {$InstanceId, GroupId} | select(.GroupId=="sg-XXXXXXX")' 


# Tips/Tricks:

Automatically add scripts to your path

If you create a directory in your home directory called "bin", bash and zsh will automatically add that folder to your PATH. By doing this, you can place all your custom scripts in ~/bin, and not worry about assigning scripts to your PATH manually. This also keeps custom scripts organized and available. 
