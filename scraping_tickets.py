##'~~~~~~~~~~~~~~~~~~~~~~~~~~~')
##' Originaly by Bruno Parodi ')
##' Adapted by Girino Vey     ')
##'~~~~~~~~~~~~~~~~~~~~~~~~~~~')

from bs4 import BeautifulSoup
from os.path import expanduser
import platform, os, requests
import argparse

# constants


class userConfig():
    def __init__(self, path, order, full_txid):
        self.path = self.find_splitticketbuyer_folder(path)
        self.order = order
        self.full_txid = full_txid
    #get the user home folder (C:\Users\name)
    def home_folder(self):
        return expanduser('~')
    #return a list of all split tickets on folder
    def all_split_tickets(self):
        return os.listdir(self.path)
    #return a list of split ticket url
    def split_ticket_txid(self):
        return [split for split in self.all_split_tickets()]
    #complete split ticket folder
    def find_splitticketbuyer_folder(self, path):
        dsf = '/data/sessions'
        if path:
            if os.path.exists(path + dsf):
                return path + dsf
            else:
                raise Exception('Cannot find path: ' + path)
        else:
            dsf = '.splitticketbuyer' + dsf
            paths = [dsf, self.home_folder() + '/' + dsf]
            for p in paths:
                if os.path.exists(p):
                    return p
            raise Exception('Cannot find splitticketbuyer data path. Try passing it as a parameter')
    def get_tickets(self):
        load = 0
        ret = []
        for id in self.split_ticket_txid():
            ret.append(ticket(id))
            self.printbar(load)
            load += 1
        ret = sorted(ret, key=ticket.get_date)
        if self.order != 'date':
            ret = sorted(ret, key=ticket.get_status)
        return ret

    def printbar(self, status):
        size = 54 #comprimento na tela da barra
        total = len(self.all_split_tickets()) #100%
        print('\r',end='')
        print(f'{"||"} LOADING {"":{status + 1}} '
              f'{(status / total) * 100:{".2f" if (status / total) * 10 < 1 else ".1f"}}% '
              f'{"":{size - status}}||',end='')

    def print_tickets(self):
        if self.full_txid:
            header =    '++==================================================================+============+============+========++'
            separator = '++------------------------------------------------------------------+------------+------------+--------++'
            mask = '|| %64s | %10s | %10s | %6s ||'
            indent = (" " * 60)
        else:
            header =    '++====================================+============+============+========++'
            separator = '++------------------------------------+------------+------------+--------++'
            mask = '|| %34s | %10s | %10s | %6s ||'
            indent = (" " * 30)

        print(header)
        print( mask % ('TXID' + indent,'DATA' + (" " * 6), 'DATA VOTO ','STATUS'))
        print(header)

        tickets = self.get_tickets()
        live = voted = immature = 0
        for t in tickets:
            if t != tickets[0]:
                print(separator)
            txid = t.get_txid()
            if not self.full_txid:
                txid = txid[:31] + '...'
            print(mask % (txid, t.get_date(), t.get_date_voted(), t.get_status()))

            #print resume
            if t.get_status().lower() == 'live':
                live += 1
            elif t.get_status().lower() == 'voted':
                voted += 1
            elif t.get_status().lower() == 'immature':
                immature += 1
            total = live + voted + immature
        print(separator)
        print(f'||{"":12}'
              f'Total: {total:2} | '
              f'Voted: {voted:2} | '
              f'Live: {live:2} | '
              f'Immature: {immature:2}'
              f'{"":12}||')
        print(header)

class ticket():
    def __init__(self, txid):
        self.txid = txid
        self.url = self.explorer_url() + txid
        page = requests.get(self.url)
        self.parsed = BeautifulSoup(page.content, 'html.parser')
        self.status = (self.parsed.find_all('td')[5].get_text().split()[0])
        self.date_voted = ''
        if self.status == 'Voted':
            self.date_voted = self.get_vote().get_date()
    #return a default Decred block explorer
    def explorer_url(self):
        return 'https://explorer.dcrdata.org/tx/'
    def get_txid(self):
        return self.txid
    #return ticket status
    def get_status(self):
        return self.status
    # returns the ticket that voted this one. Not cached, beware
    def get_vote(self):
        return ticket(self.parsed.find_all('td')[5].find_all('a', href=True)[0]['href'].split('/')[2])
    # return ticket data
    def get_date(self):
        if self.status == 'live':
            return (self.parsed.find_all('td')[17].get_text().split()[1])
        elif self.status == 'voted':
            return (self.parsed.find_all('td')[1].get_text().split()[1])
        else:
            return (self.parsed.find_all('td')[13].get_text().split()[1])
    def get_date_voted(self):
        return self.date_voted

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Check Split Ticket status.')
    parser.add_argument('path', metavar='filename', type=str, nargs='?', default=False,
                        help='path where to find the splitticketbuyer data files. (default to ~/.splitticketbuyer)')
    parser.add_argument('--date', dest='order', action='store_const',
                        const='date', default='status',
                        help='sorts by date (default: sorts by status then by date)')
    parser.add_argument('--full', dest='full_txid', action='store_const',
                        const=True, default=False,
                        help='prints full txid (might be larger than screen).')

    args = parser.parse_args()

    user = userConfig(args.path, args.order, args.full_txid)
    user.print_tickets()


    input('\nPress ENTER to close.')
