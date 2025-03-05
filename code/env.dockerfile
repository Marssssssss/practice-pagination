FROM debian:12

# mongo
RUN apt-get -y install libcurl4 openssl liblzma5 wget
RUN cd /home && mkdir mongo
RUN wget https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-debian12-8.0.5.tgz
RUN 