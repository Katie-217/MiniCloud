#!/bin/sh
set -eu
MYSQL_PWD="$MARIADB_ROOT_PASSWORD" mariadb -uroot -e "GRANT SELECT ON studentdb.* TO '$MARIADB_USER'@'%';"
