# Run wine in docker container
```
cd Wine-Docker-Image
bash run_wine.sh
```
# Config win to Windows 10 and win64
winecfg
export WINEARCH=win64
WINEARCH=win64 WINEPREFIX=~/.wine64 winecfg
wineboot --init

# Install vs build tools (Optional)
```
vs_buildtools.exe --norestart --passive --downloadThenInstall --includeRecommended --add Microsoft.VisualStudio.Workload.NativeDesktop --add Microsoft.VisualStudio.Workload.VCTools --add Microsoft.VisualStudio.Workload.MSBuildTools
```
# Install [python10](https://www.python.org/downloads/windows/)
apt-get update
WINEPREFIX=~/.wine64 wine python-install.exe 

# Install insightface
```
cd /mnt/build_winapp
wine64 python/python.exe -m pip install --upgrade pip
wine64 python/python.exe -m pip install wheel
wine64 python/python.exe -m pip install onnxruntime
wine64 python/python.exe -m pip install insightface-0.7.3-cp310-cp310-win_amd64.whl
wine64 python/python.exe -m pip install tensorflow
wine64 python/python.exe -m pip install opennsfw2==0.10.2 protobuf==4.23.2 tqdm==4.65.0 gfpgan==1.3.8
wine64 build_winapp/python/python.exe -m pip install -r requirements.txt
```

# Download ffmpeg package 
[ffmpeg-master-latest-win64-gpl.zip](https://www.ffmpeg.org/download.html)
```
cp -f ffmpeg.exe ffplay.exe ffprobe.exe /root/.wine64/drive_c/windows
```
# Build .exe file with PyInstaller
```
wine py -m PyInstaller -D -w --console run.py --add-data "models/*;models"
cp /mnt/build_winapp/python/Lib/site-packages/onnxruntime/capi/onnxruntime_providers_shared.dll dist/run/_internal/onnxruntime/capi/
cp -f modules/ui.json /mnt/dist/run/_internal/modules/
```