FROM debian:12

# 安装环境
RUN apt-get update
RUN apt-get install -y curl vim procps sudo net-tools

# 创建 elasticsearch 用户
RUN useradd -m -g sudo -s /bin/bash elasticsearch
USER elasticsearch

# 下载解压 es
WORKDIR /home/elasticsearch
RUN curl -L -O https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-8.15.3-linux-x86_64.tar.gz
RUN tar -xvf elasticsearch-8.15.3-linux-x86_64.tar.gz
RUN rm elasticsearch-8.15.3-linux-x86_64.tar.gz

# 构造启动脚本并启动 es
WORKDIR /home/elasticsearch
RUN echo "#!/bin/bash" >> start_es.sh
RUN echo "nohup /home/elasticsearch/elasticsearch-8.15.3/bin/elasticsearch &" >> start_es.sh
RUN chmod +x start_es.sh

# 构造容器启动脚本
RUN echo "#!/bin/bash" >> entrypoint.sh
RUN echo "nohup /bin/bash /home/elasticsearch/start_es.sh > /dev/null &" >> entrypoint.sh
RUN echo "echo \"Starting bash....\"" >> entrypoint.sh
RUN echo "/bin/bash" >> entrypoint.sh
RUN chmod +x entrypoint.sh

# 开放端口
EXPOSE 9200
EXPOSE 9300

# elasticsearch 8.0.1 以后有个配置叫 xpack.security.enabled 默认是 true
# 作为 docker 学习使用，可以直接关掉这个选项
# =。= 这里有个坑，elasticsearch 是第一次启动的时候如果没有对应选项才会把选项写入，所以这里不能用 sed，应该直接把选项写进去
RUN echo "xpack.security.enabled: false" >> ./elasticsearch-8.15.3/config/elasticsearch.yml

ENTRYPOINT ["/home/elasticsearch/entrypoint.sh"]
