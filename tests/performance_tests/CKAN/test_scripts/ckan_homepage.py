import matplotlib
import httplib
import time
import mechanize


class Transaction(object):
    def __init__(self):
        self.custom_timers = {}
    
    def run(self):
        br = mechanize.Browser()
        br.open('http://ec2-54-77-144-171.eu-west-1.compute.amazonaws.com/').read()
        
        # verify responses are valid
        assert (br.response().code == 200), 'Bad HTTP Response'
        
            
if __name__ == '__main__':
    trans = Transaction()
    trans.run()
    
