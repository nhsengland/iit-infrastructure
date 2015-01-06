import os
import time

import mechanize

CKAN = os.environ.get('CKAN', 'http://data.england.nhs.uk/')


class Transaction(object):
    def __init__(self):
        self.custom_timers = {}
    
    def run(self):
        # create a Browser instance
        br = mechanize.Browser()
        # don't bother with robots.txt
        br.set_handle_robots(False)
        # add a custom header so CKAN allows our requests
        br.addheaders = [('User-agent', 'Mozilla/5.0 Compatible')]
        
        # start the timer
        start_timer = time.time()
        # submit the request
        br.open(CKAN)
                
        # stop the timer
        latency = time.time() - start_timer
        
        # store the custom timer
        self.custom_timers['Load_Front_Page'] = latency  
           
        # think-time
        time.sleep(2)  
        
        # select first (zero-based) form on page
        br.select_form(nr=0)
        # set form field        
        br.form['q'] = 'england'
        
        start_timer = time.time()
        br.submit()
        
        assert 'datasets found for' in br.response().read(), 'Search not performed'
        # verify responses are valid
        assert (br.response().code == 200), 'Bad HTTP Response'
        
        latency = time.time() - start_timer
        
        # store the custom timer
        self.custom_timers['Search'] = latency  
                      
        # think-time
        time.sleep(2)  
        
if __name__ == '__main__':
    trans = Transaction()
    trans.run()
    
    for timer in trans.custom_timers:
        print '%s: %.5f secs' % (timer, trans.custom_timers[timer])
