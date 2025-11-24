@echo off
setlocal

REM === 引数チェック ===
if "%1"=="" (
    echo 使用方法: makezip.bat フォルダー名
    echo 例: makezip.bat games
    echo     makezip.bat players
    exit /b
)

set TARGET=%1
set BASEDIR=%~dp0

REM === 対象フォルダの存在チェック ===
if not exist "%BASEDIR%apps\%TARGET%" (
    echo エラー: apps\%TARGET% フォルダーが見つかりません。
    exit /b
)

REM === 出力ディレクトリ（zips）を作成 ===
if not exist "%BASEDIR%zips" (
    mkdir "%BASEDIR%zips"
)

REM === 日付入りファイル名作成 ===
for /f "tokens=1-3 delims=/- " %%a in ("%date%") do (
    set YYYY=%%a
    set MM=%%b
    set DD=%%c
)
set ZIPNAME=%TARGET%_%YYYY%%MM%%DD%.zip

echo ZIP を作成中: %ZIPNAME%
powershell -command "Compress-Archive -Path '%BASEDIR%apps\%TARGET%\*' -DestinationPath '%BASEDIR%zips\%ZIPNAME%' -Force"

echo 完了しました！
echo 生成ファイル: zips\%ZIPNAME%

endlocal
