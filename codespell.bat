@ECHO Off
SETLOCAL
SET P=%PATH%
PATH=%PATH%;D:\Programme\Python27\Scripts
codespell.exe -S "*.pyc,*.log,*.txt,*.suo,./libs,./.vs" -I ./codespell_ignore.txt -q 3
PATH=%P%
PAUSE