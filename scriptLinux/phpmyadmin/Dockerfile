FROM resin/rpi-raspbian
MAINTAINER  fnick2812@gmail.com

RUN apt-get update
RUN apt-get -y install python git
RUN mkdir /home/phpmyadmin

WORKDIR /home/phpmyadmin
RUN git clone https://github.com/khiemdo/scriptLinux.git
WORKDIR /home/phpmyadmin/scriptLinux/
RUN git checkout -b toSync
RUN git pull origin toSync

WORKDIR /home/phpmyadmin/scriptLinux/scriptLinux/phpmyadmin

RUN chmod +x phpmyadminInstall.py
RUN chmod +x phpmyadminInstall.sh

RUN ./phpmyadminInstall.py
EXPOSE 1080 1080

RUN service apache2 start