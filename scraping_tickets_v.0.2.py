##'~~~~~~~~~~~~~~~~')
##'by Bruno Parodi ')
##'~~~~~~~~~~~~~~~~')

from bs4 import BeautifulSoup
from os.path import expanduser
import platform, os, requests


class userConfig():
    #print user OS (Linux for Linux, Darwin for Mac and Windows for Windows)
    def user_os(self):
        return platform.system()
    #get the user home folder (C:\Users\name)
    def home_folder(self):
        home = expanduser('~')
        return home
    #validate the split folder
    def split_folder_validator(self):
        if os.path.exists(self.split_ticket_folder()) == False:
            return ('Split ticket folder not found')
        else:
            True
    #return a list of all split tickets on folder
    def all_split_tickets(self):
        folder = os.listdir(self.split_ticket_folder())
        return folder
    #return a list of split ticket url
    def split_ticket_url(self):
        stu = []
        for split in self.all_split_tickets():
            stu.append(ticket.explorer_url(ticket) + split)
        return stu
    #complete split ticket folder
    def split_ticket_folder(self):
        complete_folder = user.home_folder() + ticket.default_split_folder(ticket)
        return complete_folder

class ticket():
    def __init__(self,url):
        self.url = url
    #default split ticket folder
    def default_split_folder(self):
        dsf = ('\.splitticketbuyer\data\sessions')
        return dsf
    #return a default Decred block explorer
    def explorer_url(self):
        eurl = ('https://explorer.dcrdata.org/tx/')
        return eurl
    #request info from url
    def page(self):
        page = requests.get(self.url)
        return BeautifulSoup(page.content, 'html.parser')
    #return ticket status
    def status(self):
        return (self.page().find_all('td')[5].get_text().split()[0])
    # return ticket data
    def data(self):
        if self.status() == 'live':
            return (self.page().find_all('td')[17].get_text().split()[1])
        elif self.status() == 'voted':
            return (self.page().find_all('td')[1].get_text().split()[1])
        else:
            return (self.page().find_all('td')[13].get_text().split()[1])

print('\n\n\n')
print('________________________________________________________')
print('| Check files in folder \.splitticketbuyer\data\sessions|')
print('| and get online status of split ticket.          Enjoy.|')
print('|_______________________________________________________|\n')

user = userConfig()

for x in user.split_ticket_url():
    print(x)
    print('Ticket data: ', ticket(x).data())
    print('Status     : ', ticket(x).status())
    print('')

input('\nPress ENTER to close.')