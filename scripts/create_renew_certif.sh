#!/bin/bash

domains=("aaa.com.br" "bbbb.be" "ccc.online" "ddd.io" "eee.com")

for domain in "${domains[@]}"; do
  sudo cat <<EOL > /etc/letsencrypt/renewal/$domain.conf
# /etc/letsencrypt/renewal/$domain.conf
version = 1.21.0
archive_dir = /etc/letsencrypt/archive/$domain
cert = /etc/letsencrypt/live/$domain/cert.pem
privkey = /etc/letsencrypt/live/$domain/privkey.pem
chain = /etc/letsencrypt/live/$domain/chain.pem
fullchain = /etc/letsencrypt/live/$domain/fullchain.pem

# Options used in the renewal process
[renewalparams]
account = your-account-id
authenticator = webroot
webroot_path = /var/www/$domain,  # Adjust this path to the correct webroot
server = https://acme-v02.api.letsencrypt.org/directory
EOL
done
