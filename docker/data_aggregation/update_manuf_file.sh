#!/bin/bash

curl https://gitlab.com/wireshark/wireshark/raw/master/manuf > ./files/manuf_lookup/manuf.txt

curl https://gitlab.com/wireshark/wireshark/raw/master/wka >> ./files/manuf_lookup/manuf.txt

