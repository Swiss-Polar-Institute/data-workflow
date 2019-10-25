#!/bin/bash

if [ $# -ne 1 ]
then
	echo "Syntax error"
	echo $0: usage: $0 output_directory
	echo 'The name of the file will be dataworkflow-$DATE-$USER.sql'
	echo
	exit 1
fi

DIRECTORY="$1"

USER=$(whoami)
OUTPUT_NAME=$(date "+dataworkflow-%Y%m%d-%H%M%S-$USER.sql")
OUTPUT_FILE="$DIRECTORY/$OUTPUT_NAME"

mysqldump --defaults-file=/etc/mysql/data-workflow.cnf datawworkflow > "$OUTPUT_FILE"

echo
echo "Backup done: $OUTPUT_FILE"
