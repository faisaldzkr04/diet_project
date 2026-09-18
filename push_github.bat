@echo off
title Push Auto Git - diet_project
color 0A
cd /d "%~dp0"

echo ========================================================
echo        DIET PROJECT - AUTOMATED GIT PUSH SCRIPT
echo ========================================================
echo.

echo [1/5] Inisialisasi Git Repository...
git.exe init

echo.
echo [2/5] Menambahkan seluruh berkas project...
git.exe add .

echo.
echo [3/5] Membuat Commit...
git.exe commit -m "Fix food queries, bounds check, dynamic category, and add README"

echo.
echo [4/5] Mengatur Remote Repository...
git.exe branch -M main
git.exe remote add origin https://github.com/faisaldzkr04/diet_project.git >nul 2>&1
git.exe remote set-url origin https://github.com/faisaldzkr04/diet_project.git

echo.
echo [5/5] Mengirim perubahan ke GitHub (Force Push)...
git.exe push -u origin main --force

if %errorlevel% equ 0 (
    echo.
    echo ========================================================
    echo [BERHASIL] PUSH KE GITHUB SELESAI!
    echo Repo: https://github.com/faisaldzkr04/diet_project
    echo ========================================================
) else (
    color 0E
    echo.
    echo ========================================================
    echo [INFO] Jika terjadi masalah login/autentikasi,
    echo pastikan Anda telah memasukkan Personal Access Token (PAT)
    echo atau login ke akun GitHub Anda.
    echo ========================================================
)

echo.
echo Tekan sembarang tombol untuk menutup...
pause >nul
