# vim: set expandtab ts=2 :
FROM debian:stretch

# ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update -qq && \
    apt-get install -qq -y \
    ca-certificates curl lsb-release apt-transport-https gnupg2 software-properties-common net-tools iptables arptables ebtables

RUN update-alternatives --set iptables /usr/sbin/iptables-legacy
RUN update-alternatives --set ip6tables /usr/sbin/ip6tables-legacy

# RUN curl -fsSL https://download.docker.com/linux/debian/gpg | gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
RUN curl -fsSL https://download.docker.com/linux/debian/gpg | apt-key add -

RUN add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/debian stretch stable"

# RUN echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/debian $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null

RUN apt-get update -qq && \
    apt-get install -qq -y docker-ce && \
    apt-get install -qq -y docker-ce-cli
#     && \
#     apt-get install -qq -y containerd.io

CMD service docker start