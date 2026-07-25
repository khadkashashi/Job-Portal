@echo off
cd /d E:\Job_Portal
E:\Job_Portal\.venv\Scripts\python.exe manage.py send_deadline_reminders

#Why a .bat file instead of pointing Task Scheduler straight at python.exe: Task Scheduler needs to run the command from inside your project folder (so Django can find manage.py and your settings) — the cd /d line handles that automatically every time it runs, so you don't have to configure "start in" folder settings separately and get them wrong.