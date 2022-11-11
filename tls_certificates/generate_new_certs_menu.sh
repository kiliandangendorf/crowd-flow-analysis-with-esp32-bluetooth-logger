#!/bin/bash
#
# This script should help you creating and signing self-signed TLS certificates.
#
# Edit values for you needs in $CN, $DURATION_IN_DAYS_<type> and $SUBJECT_BASE only!
#
# KD 2022-06-08
#
# from: 
# - https://gist.github.com/suru-dissanaike/4344f572b14c108fc3312fc4fcc3d138
# - http://www.steves-internet-guide.com/mosquitto-tls/
# - https://stackoverflow.com/a/1885534/11438489
# - https://askubuntu.com/a/1716

# Choose URL or IP here, but make sure this is the exact same as the client connects to.
CN="example.com"

DURATION_IN_DAYS_CA=7300 # 20 years
DURATION_IN_DAYS_SERVER=398 # 13 months
DURATION_IN_DAYS_CLIENT=398 # 13 months

# x.509 subjects
# country (countryName, C),
# state or province name (stateOrProvinceName, ST),
# locality (locality, L),
# organization (organizationName, O),
SUBJECT_BASE="/C=US/ST=San Fransisco/L=San Fransisco/O=Example Company"
# organizational unit (organizationalUnitName, OU),
# (for the ESP32 the ca-cert needs to have literal "CA" here)
# common name (commonName, CN).
SUBJECT_CA="${SUBJECT_BASE}/OU=CA/CN=${CN}"
SUBJECT_SERVER="${SUBJECT_BASE}/OU=Server/CN=${CN}"
SUBJECT_CLIENT="${SUBJECT_BASE}/OU=Client/CN=${CN}"


# keypair _and_ cert for CA
function generate_ca () {
	echo "$SUBJECT_CA"
	# create keypair and cert
	openssl req -x509 -nodes -sha256 -newkey rsa:2048 -subj "$SUBJECT_CA"  -days $DURATION_IN_DAYS_CA -keyout ca.key -out ca.crt
}

# keypair _and_ cert for server _and_ csr (Certificate Signing Request)
# Here CN (common name usually domainname) is important ("You could use the IP address or Full domain name. You must use the same name when configuring the client connection.")
function generate_server () {
	echo "$SUBJECT_SERVER"
	# create keypair and cert
	openssl req -nodes -sha256 -new -subj "$SUBJECT_SERVER" -keyout server.key -out server.csr
	# sign server cert with CA key
	openssl x509 -req -sha256 -in server.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out server.crt -days $DURATION_IN_DAYS_SERVER
}

function generate_client () {
	echo "$SUBJECT_CLIENT"
	# create keypair and cert
	openssl req -new -nodes -sha256 -subj "$SUBJECT_CLIENT" -out client.csr -keyout client.key 
	# sign server cert with CA key
	openssl x509 -req -sha256 -in client.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out client.crt -days $DURATION_IN_DAYS_CLIENT
}

# for server we actually need ca.crt, serever.crt and server.key
# for client ca.crt and optionally client.crt and client.key
# not used here...
function copy_keys_to_broker () {
   sudo cp ca.crt /etc/mosquitto/certs/
   sudo cp server.crt /etc/mosquitto/certs/
   sudo cp server.key /etc/mosquitto/certs/
}

function run_all_of_them () {
	generate_ca
	generate_server
	generate_client
	#copy_keys_to_broker
}

function cleanup_all_files () {
	all_files=("ca.crt" "ca.key" "ca.srl" \
		"client.crt" "client.csr" "client.key" \
		"server.crt" "server.csr" "server.key")
	for file in "${all_files[@]}"
	do
		if [ -f "$file" ] ; then
			echo rm "$file"
			rm "${file}"
		fi
	done
}

function prompt_y_n () {
	read -p "This will overwrite/remove keyfiles in this dir. Are you sure? (y/n)" -n 1 -r
	echo    # (optional) move to a new line
	if [[ $REPLY =~ ^[Yy]$ ]]
	then
		# do dangerous stuff
		# run function given
		($1)
	else
		echo "Abort"
	fi
}

# Bash Menu Script
PS3='Please enter your choice: '
options=("CA / root certificate" "Server certificate" "Client certificate" "All of them!" "Cleanup all files!" "Quit")
select opt in "${options[@]}"
do
    case $opt in
        ${options[0]})
            echo ${options[0]}
            prompt_y_n generate_ca
            break
            ;;
        ${options[1]})
            echo ${options[1]}
            prompt_y_n generate_server
            break
            ;;
        ${options[2]})
            echo ${options[2]}
            prompt_y_n generate_client
            break
            ;;
        ${options[3]})
            echo ${options[3]}
            prompt_y_n run_all_of_them
            break
            ;;
        ${options[4]})
            echo ${options[4]}
            prompt_y_n cleanup_all_files
            break
            ;;
        "Quit")
            break
            ;;
        *) echo "invalid option $REPLY";;
    esac
done


