#!/usr/bin/env python3
class human(object):
    def __init__(self, firstname = 'john', lastname = 'deere'):
        self.firstname = firstname
        self.lastname = lastname
    def hprint(self):
        print('Firstname: {}/nLasneame: {}'.format(self.firstname,self.lastname))
class man(human):
    def __init__(self, firstname, lastname, length):
        super().__init__(firstname, lastname)
        self.length = length
    def hprint(self):
        print('Firstname: {}/nLasneame: {}/nLendth: {}'.format(self.firstname,self.lastname,self.length))
def main():
    h = man("janis","jarans",40)
    h.hprint()
if __name__  == "__main__":
    main()