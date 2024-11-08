FROM python:3.11.10-bookworm

#定義常數
ARG REPO_NAME

#set the working directory
WORKDIR /root/${REPO_NAME}

# start the server
CMD ["tail", "-f", "/dev/null"]