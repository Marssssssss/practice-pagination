FROM debian:12

# mongo
RUN apt-get update
RUN apt-get install -y gnupg curl sudo
RUN cd /home && mkdir mongo
RUN curl -fsSL https://www.mongodb.org/static/pgp/server-8.0.asc | \
sudo gpg -o /usr/share/keyrings/mongodb-server-8.0.gpg \
--dearmor
RUN echo "deb [ signed-by=/usr/share/keyrings/mongodb-server-8.0.gpg ] http://repo.mongodb.org/apt/debian bookworm/mongodb-org/8.0 main" | sudo tee /etc/apt/sources.list.d/mongodb-org-8.0.list
RUN sudo apt-get update
RUN apt-get install -y mongodb-org

# 开放端口
EXPOSE 27017

ENTRYPOINT ["/bin/bash"]
