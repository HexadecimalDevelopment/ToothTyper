#!/bin/bash

if [[ ! -d yt-dlp ]] ; then
    mkdir yt-dlp
fi

if [[ ! -f yt-dlp/yt-dlp ]] ; then
    echo 'Downloading yt-dlp...'
    wget 'https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp' -O yt-dlp/yt-dlp
fi

if [[ ! -f rick.webm ]] ; then
    echo 'Downloading video...'
    chmod +x yt-dlp
    ./yt-dlp 'https://www.youtube.com/watch?v=dQw4w9WgXcQ' -o 'rick.webm'
fi

if [[ ! -d vlc ]] ; then
    mkdir vlc
fi

if [[ ! -f vlc/vlc_port ]] ; then
    echo 'Downloading VLC...'
    wget 'https://github.com/cmatomic/VLCplayer-AppImage/releases/latest/download/VLC_media_player-3.0.11.1-x86_64.AppImage' -O 'vlc/vlc_port'
fi

echo 'Building script...'

if [[ ! -d binaries ]] ; then
    mkdir binaries
fi

pyinstaller --noconfirm --onefile --console text.py
rm -rf build
rm text.spec
mv dist/text ./binaries
rm -r dist

pyinstaller --noconfirm --onefile --noconsole --add-data=rick.webm:. --add-data=binaries/text:. --add-data=vlc/vlc_port:. main.py
rm -rf build
rm main.spec
mv dist/main ./binaries
rm -r dist

rm ./binaries/text

echo 'Finished build!'