FROM odoo:16

USER root

COPY requirements.txt /mnt/requirements.txt


RUN pip3 install -r /mnt/requirements.txt