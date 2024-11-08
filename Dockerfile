FROM python:3.11.10-bookworm

#定義ARG,執行docker build --
ARG REPO_NAME

#set the working directory
WORKDIR /root/${REPO_NAME}

COPY ./requirements.txt .

#定義miniconda3的路徑
ENV PATH="/root/miniconda3/bin:${PATH}" 
ARG PATH="/root/miniconda3/bin:${PATH}"

# Install wget to fetch Miniconda
RUN apt-get update && \
    apt-get install -y wget && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Miniconda on x86 or ARM platforms
RUN arch=$(uname -m) && \
    if [ "$arch" = "x86_64" ]; then \
    MINICONDA_URL="https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh"; \
    elif [ "$arch" = "aarch64" ]; then \
    MINICONDA_URL="https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-aarch64.sh"; \
    else \
    echo "Unsupported architecture: $arch"; \
    exit 1; \
    fi && \
    wget $MINICONDA_URL -O miniconda.sh && \
    mkdir -p /root/.conda && \
    bash miniconda.sh -b -p /root/miniconda3 && \
    rm -f miniconda.sh

RUN conda --version && conda init


# 安裝git
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y git

# git初始化,修改成自已的
RUN git config --global user.name "roberthsu2003"
RUN git config --global user.email "roberthsu2003@gmail.com"

# start the server
CMD ["tail", "-f", "/dev/null"]