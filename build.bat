@echo off

echo Building executables...

IF NOT EXIST "binaries" (
    mkdir binaries
)

xcopy /E /I icons binaries\icons
xcopy /E /I Qt binaries\Qt

pyinstaller --noconfirm --onefile --noconsole --icon=icons\icon.ico main.py
rmdir /S /Q build
del main.spec
move dist\main.exe .\binaries
rmdir /Q dist

echo Finished build!
