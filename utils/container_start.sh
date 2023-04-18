#!/bin/bash

# Allow to be queries from outside
sed -i '31 s/bind-address/#bind-address/' /etc/mysql/mysql.conf.d/mysqld.cnf

service mysql start

# Create a Database, a user with password, and permissions
cd /var/hackergram
mysql -u root < start.sql
python3 /var/hackergram/hackergram.py

while [ true ]; do sleep 60; done
