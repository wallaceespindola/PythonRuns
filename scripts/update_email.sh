#!/bin/bash

echo ""
echo "Email replacement started at: $(date '+%Y-%m-%d %H:%M:%S')"
echo ""

# Define variables
OLD_EMAIL="dev-email@wpengine.local"
NEW_EMAIL="abc@gmail.com"
WP_PATH_1="/var/www/"
WP_PATH_2="/srv/www/"
DB_NAME="your_database_name"
DB_USER="your_db_user"
DB_PASS="your_db_password"

# Replace in files
grep -rl "$OLD_EMAIL" $WP_PATH_1 | xargs sed -i "s/$OLD_EMAIL/$NEW_EMAIL/g"
grep -rl "$OLD_EMAIL" $WP_PATH_2 | xargs sed -i "s/$OLD_EMAIL/$NEW_EMAIL/g"
echo "Grep and replace done!"
echo ""

# Update database
mysql -u "$DB_USER" -p"$DB_PASS" "$DB_NAME" <<EOF
UPDATE wp_options SET option_value = '$NEW_EMAIL' WHERE option_name IN ('admin_email', 'new_admin_email') AND option_value = '$OLD_EMAIL';
UPDATE wp_users SET user_email = '$NEW_EMAIL' WHERE user_email = '$OLD_EMAIL';
UPDATE wp_usermeta SET meta_value = '$NEW_EMAIL' WHERE meta_key = 'billing_email' AND meta_value = '$OLD_EMAIL';
UPDATE wp_postmeta SET meta_value = '$NEW_EMAIL' WHERE meta_value = '$OLD_EMAIL';
EOF
echo "DB updated successfully!"
echo ""

# Restart services
systemctl restart apache2
systemctl restart mysql
echo "Restarts done successfully!"
echo ""

# Flush WP cache
wp cache flush --allow-root
echo "WP cache flushed successfully!"
echo ""

echo "E-mail updated successfully!"

## 0. Useful SQL queries to check email addresses in the database:
#SELECT * FROM wp_options WHERE option_value LIKE '%@gmail.com%';
#SELECT * FROM wp_users WHERE user_email LIKE '%@gmail.com%';
#SELECT * FROM wp_usermeta WHERE meta_value LIKE '%@gmail.com%';
#SELECT * FROM wp_postmeta WHERE meta_value LIKE '%@gmail.com%';
#SELECT * FROM wp_comments WHERE comment_author_email LIKE '%@gmail.com%';
#
#SELECT * FROM wp_options WHERE option_value LIKE '%wpengine%';
#SELECT * FROM wp_users WHERE user_email LIKE '%wpengine%';
#SELECT * FROM wp_usermeta WHERE meta_value LIKE '%wpengine%';
#SELECT * FROM wp_postmeta WHERE meta_value LIKE '%wpengine%';
#SELECT * FROM wp_comments WHERE comment_author_email LIKE '%wpengine%';
#
## 1. Update Admin Email in wp_options
#UPDATE wp_options
#SET option_value = 'abc@gmail.com'
#WHERE option_name IN ('admin_email', 'new_admin_email')
#AND option_value = 'dev-email@wpengine.local';
#
## 2. Update User Emails in wp_users
#UPDATE wp_users
#SET user_email = 'abc@gmail.com'
#WHERE user_email = 'skipy.europe@gmail.com';
#
## 3. Update Email in wp_usermeta (if stored there)
#UPDATE wp_usermeta
#SET meta_value = 'abc@gmail.com'
#WHERE meta_key = 'billing_email'
#AND meta_value = 'dev-email@wpengine.local';
#
## 4. Update Email in Post Meta (if stored in orders or forms)
#UPDATE wp_postmeta
#SET meta_value = 'abc@gmail.com'
#WHERE meta_value = 'dev-email@wpengine.local';
#
## 5. Check for Any Other Occurrences - To manually check where else the email appears, run:
#SELECT * FROM wp_options WHERE option_value LIKE '%dev-email@wpengine.local%';
#SELECT * FROM wp_users WHERE user_email LIKE '%dev-email@wpengine.local%';
#SELECT * FROM wp_usermeta WHERE meta_value LIKE '%dev-email@wpengine.local%';
#SELECT * FROM wp_postmeta WHERE meta_value LIKE '%dev-email@wpengine.local%';
#SELECT * FROM wp_comments WHERE comment_author_email LIKE '%dev-email@wpengine.local%';
