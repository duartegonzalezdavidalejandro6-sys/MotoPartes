@echo off
black .
isort .
flake8
pause