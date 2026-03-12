echo 'Building script...'

if [[ ! -d binaries ]] ; then
    mkdir binaries
fi

cp -R icons binaries/
cp -R Qt binaries/

pyinstaller --noconfirm --onefile --noconsole main.py
rm -rf build
rm main.spec
mv dist/main ./binaries
rm -r dist

echo 'Finished build!'
