import time
import mechanize


class Transaction(object):
    def __init__(self):
        self.custom_timers = {}
    
    def run(self):
        br = mechanize.Browser()
        start_timer = time.time()
        br.open('http://ec2-54-77-144-171.eu-west-1.compute.amazonaws.com/').read()
          
        # stop the timer
        latency = time.time() - start_timer
        
        # store the custom timer
        self.custom_timers['Load_Front_Page'] = latency
        
        # verify responses are valid
        assert (br.response().code == 200), 'Bad HTTP Response'
        
            
if __name__ == '__main__':
    trans = Transaction()
    trans.run()
    
    for timer in trans.custom_timers:
        print '%s: %.5f secs' % (timer, trans.custom_timers[timer])
