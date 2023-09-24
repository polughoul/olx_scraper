init:
	type .\init.sql | .\sqlite3.exe olx.sqlite
run:
	python main.py
	
