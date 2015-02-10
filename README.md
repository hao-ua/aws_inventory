# aws_inventory
Tool to get data from AWS and output it in different formats

## Configuration
All configuration stored in aws_inventory.ini. Configuration file should contain at least one AWS account.

- General section (name: General)
  
 - site_root - directory to store result data

 - module_dir - directory with data and reander modules

 - log_file - path to log file

- AWS account section (Name should start with AWS)

 - aws_key - key ID to AWS account

 - aws_secret - secret key ID to AWS account

 - aws_account_name - name of the AWS account

## Requirements

To get data from AWS should be installed boto module (version 2.10.0+)
To output into XLSX format should be installed openpyxl module (version 2+)

## Modules

- EC - elasticache module (data_EC.py)

 Collects data about elasticache. Such as: Name, Endpoint, Status, Node type, Maintenance window, Engine.
- EC2 - EC2 module (data_EC2.py)

 Collects data about EC2 instances. Such as: Name, ELB name, IP address, State, Route53 name, Private IP, Public DNS, Instance type.
 
- EIP - elastic IP module (data_EIP.py)

 Collects data about elastic IP's. Such as: IP address, Instance ID, Instance name, Route53 name.

- ELB - elastic load balancer module (data_ELB.py)

 Collects data about elastic load balancers. Such as: Name, DNS name, Instances count, Route53 name.

- RDS - Relational Database Service module (data_RDS.py)

 Collects data about RDS. Such as: Name, Endpoint, Allocated storage, Instance class, Status.

- Route53 - Route53 module (data_Route53.py)

 Collects data about Route53. Used for mapping EIP, ELB, S3, etc. to DNS records.

- S3 - S3 module (data_S3.py)

 Collects data about S3. Such as: Name, Website endpoint, Route53 name.

- SG - Secyrity group module (data_SG.py)

 Collects data about secyrity groups. Such as: Protocol, Port, Source.

- Users - AWS IAM users module (data_Users.py)

 Collects data about AWS IAM users. Such as: User name, Groups

- Snapshots - AWS EBS snapshots module (data_snapshots.py)

 Collects data about EBS snapshots. Such as: ID, Status, Size, Volume ID, Volume exists, Owner ID, Image ID.

- Volumes - AWS EBS volumes module (data_volumes.py)

 Collects data about EBS volumes. Such as: ID, Attachment State, IOPS, Size, Create Time.
 
- CSV - module to output to CSV file (render_csv.py)

- pureHTML - module to output to single HTML page (render_purehtml.py)

- XLSX - module to output to XLSX file (render_xlsx.py)