apt-get update
apt install -y software-properties-common
add-apt-repository -y ppa:deadsnakes/ppa
apt install -y python3.10 
update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.10 1
update-alternatives --install /usr/bin/python python /usr/bin/python3.10 1
pip install --upgrade pip setuptools wheel
apt install -y build-essential checkinstall libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev 
apt install -y python3-pip 
apt install -y python3.10-distutils
curl -sS https://bootstrap.pypa.io/get-pip.py | python3.10
apt install -y python3.10-dev
pip3 install insightface==0.7.3
pip3 install onnxruntime-gpu==1.15.1
pip3 install -r requirements.txt
pip3 install --default-timeout=100 tensorflow==2.13.0rc1
pip3 install opennsfw2==0.10.2 protobuf==4.23.2 tqdm==4.65.0 gfpgan==1.3.8
apt-get install -y ffmpeg
apt-get install -y python3.10-tk
apt-get install -y v4l-utils