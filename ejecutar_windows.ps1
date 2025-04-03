docker build -t slack-container .

docker run --name slack -d --volume /var/run/docker.sock:/var/run/docker.sock --privileged slack-container