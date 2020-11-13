import Timing
import selfreport_linux

if __name__ == '__main__':
    sp = selfreport_linux.SelfReport()
    while True:
        Timing.checktime(sp.run,sp.run)