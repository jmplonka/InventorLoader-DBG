@ECHO Off
codespell.exe -S "*.pyc,*.log,*.txt,*.suo,./libs" -I ./codespell_ignore.txt -q 3

PAUSE