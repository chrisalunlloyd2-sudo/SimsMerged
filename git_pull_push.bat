@echo off
echo [GITHUB SYNC] Merging Remote History...
set GIT_EXE="C:\Users\viper\git\cmd\git.exe"

set GIT_MERGE_AUTOEDIT=no
%GIT_EXE% pull origin main --allow-unrelated-histories --no-edit

echo [GITHUB SYNC] Pushing Merged State...
%GIT_EXE% push -u origin main
