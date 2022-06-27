import os
import sys
import requests
from bs4 import BeautifulSoup as Bs
from colorama import Fore
args = sys.argv

websites = {}


class Browser:

    def __init__(self):
        self.soup = None
        self.dir = args[1]
        self.user = None
        self.cache = {}
        self.page = None

    def directory(self):
        if os.access(self.dir, os.F_OK):
            pass
        else:
            os.mkdir(self.dir)
        os.chdir(self.dir)

    def error_check(self):
        if '.' not in self.user:
            print('Incorrect URL')
            return False

        if not self.user.startswith('https://'):
            self.user = 'https://' + self.user

        try:
            self.page = requests.get(self.user)
        except requests.exceptions.RequestException:
            return False
        return True

    def cache_check(self):
        if self.user in self.cache.keys():
            return True
        else:
            return False

    @staticmethod
    def cache_read(file):
        with open(file, 'r', encoding='utf-8') as file:
            print(file.read())

    def cache_save(self):
        strip = self.user[8:-4]
        with open(strip, 'w', encoding='utf-8') as file:
            file.write('\n'.join(self.soup))
            self.cache[strip] = rf'{os.getcwd()}\{strip}'

    def page_read(self):
        tags = ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'a', 'ul', 'ol', 'li']
        self.soup = []
        for c in Bs(self.page.content, 'html.parser').find_all(tags):
            if c.text:
                if c.name == 'a':
                    self.soup.append(Fore.BLUE + c.text)
                else:
                    self.soup.append(Fore.RESET + c.text)
        print(*self.soup, sep='\n')

    def main(self):
        history = []
        self.directory()
        while True:

            self.user = input()

            if self.user == 'exit':
                break

            elif self.cache_check():
                self.cache_read(self.user)
                history.append(self.user)

            elif self.user == 'back':
                try:
                    a = history.pop(-2)
                    self.cache_read(a)
                except IndexError:
                    pass

            elif self.error_check():
                self.page_read()
                self.cache_save()
                history.append(self.user[8:-4])


if __name__ == "__main__":
    Browser().main()
