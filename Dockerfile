FROM ubuntu:22.04

RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        ca-certificates \
        cmake \
        curl \
        git \
        libjpeg-dev \
        libpng-dev \
        libpango1.0-dev \
        pkg-config \
        python3-dev && \
    rm -rf /var/lib/apt/lists/*
ENV PATH /opt/conda/bin:$PATH

RUN curl -fsSL -v -o ~/miniconda.sh -O  https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-$(uname -m).sh  && \
    chmod +x ~/miniconda.sh && \
    ~/miniconda.sh -b -p /opt/conda && \
    rm ~/miniconda.sh && \
    /opt/conda/bin/conda install -y python==3.9.1 && \
    /opt/conda/bin/conda clean -ya
RUN pip install torch==1.8.2+cu102 torchvision==0.9.2+cu102 -f https://download.pytorch.org/whl/lts/1.8/torch_lts.html

LABEL com.nvidia.volumes.needed="nvidia_driver"
ENV NVIDIA_VISIBLE_DEVICES all
ENV NVIDIA_DRIVER_CAPABILITIES compute,utility
ENV LD_LIBRARY_PATH /usr/local/nvidia/lib:/usr/local/nvidia/lib64

WORKDIR /workspace
COPY ./requirements.txt /workspace/requirements.txt
RUN pip install cython && pip install -r requirements.txt && pip cache purge && rm requirements.txt


