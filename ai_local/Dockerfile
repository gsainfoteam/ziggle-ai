# 베이스 이미지로 ubuntu 사용
FROM ubuntu:20.04


# 필수 패키지 설치
RUN apt-get update && apt-get install -y \
    build-essential \
    wget \
    curl \
    git \
    libssl-dev \
    zlib1g-dev \
    libncurses5-dev \
    libncursesw5-dev \
    libreadline-dev \
    libsqlite3-dev \
    libgdbm-dev \
    libdb5.3-dev \
    libbz2-dev \
    libexpat1-dev \
    liblzma-dev \
    libffi-dev \
    tk-dev

# Python 3.8.10 설치
RUN wget https://www.python.org/ftp/python/3.8.10/Python-3.8.10.tgz && \
    tar xzf Python-3.8.10.tgz && \
    cd Python-3.8.10 && \
    ./configure --enable-optimizations && \
    make altinstall && \
    cd .. && \
    rm -rf Python-3.8.10 Python-3.8.10.tgz

# pip 최신 버전으로 업그레이드
RUN python3.8 -m ensurepip && \
    python3.8 -m pip install --upgrade pip

# Colab에서 사용하는 패키지 설치
RUN python3.8 -m pip install \
    numpy \
    pandas \
    matplotlib \
    seaborn \
    scipy \
    scikit-learn \
    tensorflow \
    torch \
    torchvision \
    jupyter \
    jupyterlab


# unsloth 패키지 설치
RUN pip3 install "unsloth[colab-new] @ git+https://github.com/unslothai/unsloth.git"

# 추가 패키지 설치
RUN pip3 install --no-deps xformers "trl<0.9.0" peft accelerate bitsandbytes

# 작업 디렉토리 설정
WORKDIR /ai_local

# 컨테이너가 시작될 때 Jupyter Lab을 실행
CMD ["jupyter-lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root"]