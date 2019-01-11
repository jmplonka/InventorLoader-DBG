@ECHO Off
codespell.exe -S "*.pyc,*.log,*.txt,*.suo,./libs,./.vs" -I ./codespell_ignore.txt -q 3

PAUSE