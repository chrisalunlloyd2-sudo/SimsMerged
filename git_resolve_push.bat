@echo off
echo [GITHUB SYNC] Resolving Conflicts Favoring Local State...
set GIT_EXE="C:\Users\viper\git\cmd\git.exe"

%GIT_EXE% checkout --ours .
%GIT_EXE% add .
%GIT_EXE% commit -m "Merged remote changes, favoring local operational state to preserve ToK, Chronos, and UI fixes"
%GIT_EXE% push -u origin main
