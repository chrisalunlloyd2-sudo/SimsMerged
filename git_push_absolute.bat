@echo off
echo [GITHUB SYNC] Using Absolute Path Git Binary...
set GIT_EXE="C:\Users\viper\git\cmd\git.exe"

echo [GITHUB SYNC] Configuring Git...
%GIT_EXE% config --global user.email "viper-architect@simsmerged.com"
%GIT_EXE% config --global user.name "Gemini-CLI-Architect"
%GIT_EXE% config --global init.defaultBranch main

echo [GITHUB SYNC] Initializing Repository...
%GIT_EXE% init

echo [GITHUB SYNC] Setting Remote...
%GIT_EXE% remote remove origin >nul 2>&1
%GIT_EXE% remote add origin https://github.com/chrisalunlloyd2-sudo/SimsMerged.git

echo [GITHUB SYNC] Adding and Committing (Add-Only)...
%GIT_EXE% add .
%GIT_EXE% commit -m "Final Operational Sync: ToK, Chronos, DePIN, Chat Stabilized"

echo [GITHUB SYNC] Pushing to Remote Repository...
%GIT_EXE% push -u origin main

echo [GITHUB SYNC] Complete.
