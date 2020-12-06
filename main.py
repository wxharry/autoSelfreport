import Timing
import selfreport

if __name__ == '__main__':
    sp = selfreport.SelfReport()
    while True:
        Timing.checktime(sp.run,sp.run)