#!/usr/bin/env bash

apt update
apt -y install uwsgi-plugin-python3
apt -y install python3-venv

python3 -m venv /opt/linker

. /opt/linker/bin/activate

pip install --upgrade pip

pip install ../

cp linker-uwsgi.ini /opt/linker/

cp linker-nginx.conf /etc/nginx/sites-available/
pushd /etc/nginx/sites-enabled/
  ln -s ../sites-available/linker-nginx.conf
popd

systemctl start linker.service
systemctl restart nginx
