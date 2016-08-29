FROM resin/rpi-raspbian
MAINTAINER  fnick2812@gmail.com

RUN apt-get update
RUN apt-get install python git
RUN mkdir /home/phpmyadmin
ADD ./* /home/phpmyadmin
RUN chmod +x *
RUN ./phpmyadminInstall.py
EXPOSE 1080 1080

RUN service apache2 start
ENTRYPOINT ["tail"]
CMD ["-f /dev/null"]