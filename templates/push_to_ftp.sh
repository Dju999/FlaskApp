#!/bin/bash
sftp -i ~/.ssh/ special@ftp.digitalaccess.ru <<EOF
cd /uploads/vast/production/ <<EOF
put {{ file_name }}
EOF

