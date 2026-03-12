echo 'Building script...'

if [[ ! -d binaries ]] ; then
    mkdir binaries
fi

pyinstaller --noconfirm --onefile --noconsole main.py
rm -rf build
rm main.spec
mv dist/main ./binaries
rm -r dist

echo 'Finished build!'
