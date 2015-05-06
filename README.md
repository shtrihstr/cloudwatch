#AWC EC2 custom metrics for CloudWatch

Send memory and cpu usage metrics to Amazon CloudWatch

##Required:
https://github.com/giampaolo/psutil

##Usage:
##### 1. Clone cloudwatch.py to EC2 linux server

##### 2. Create a boto credentials file `/etc/boto.cfg`
```
[Credentials]
aws_access_key_id = <aws access key>
aws_secret_access_key = <aws access secret>
```
##### 3. confugure crontab `$ crontab -e`
```
* * * * * /usr/bin/python /path/to/cloudwatch.py
```