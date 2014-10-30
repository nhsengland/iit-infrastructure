import time
import mechanize


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
        br.open('http://ec2-54-77-144-171.eu-west-1.compute.amazonaws.com/')
                
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