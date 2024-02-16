FROM nexle/faceswap/deepfacelive:latest
ENV TZ=Asia/Ho_Chi_Minh
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN pip3 install pyarmor
COPY . /Deep-Live-Cam
WORKDIR /Deep-Live-Cam
# Encrypted all source code
RUN pyarmor-7 obfuscate --recursive run.py
RUN cp -rf dist/* ./
RUN rm -rf dist
ENTRYPOINT ["python3","run.py"]
