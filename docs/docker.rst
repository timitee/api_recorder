Install
=======

https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-16-04


sudo systemctl status docker



https://docs.microsoft.com/en-us/azure/virtual-machines/linux/docker-machine

curl -L https://github.com/docker/machine/releases/download/v0.10.0/docker-machine-`uname -s`-`uname -m` >/tmp/docker-machine &&
  chmod +x /tmp/docker-machine &&
  sudo cp /tmp/docker-machine /usr/local/bin/docker-machine


docker-machine version
docker-machine version 0.10.0, build 76ed2a6

docker-machine create --driver azure

docker-machine create -d azure \
  --azure-ssh-user ops \
  --azure-subscription-id ffea4fd2-d169-4caa-8c23-02a4a8448c18 \
  --azure-open-port 80 \
  machine


docker-machine env machine

export DOCKER_TLS_VERIFY="1"
export DOCKER_HOST="tcp://13.64.154.240:2376"
export DOCKER_CERT_PATH="/home/tim/.docker/machine/machines/machine"
export DOCKER_MACHINE_NAME="machine"
docker run -d -p 80:80 --restart=always nginx

docker ps

docker-machine ip <VM name>
