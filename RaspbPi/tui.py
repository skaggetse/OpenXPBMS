import time
import curses

hello = "hello, world"

def main(stdscr):
    # disable cursor blinking
    curses.curs_set(0)

    # write something on the screen
    stdscr.addstr(5, 10, hello)

    # update the screen
    stdscr.refresh()

    # wait for 3 seconds
    time.sleep(3)

    # clear the screen
    stdscr.clear()


curses.wrapper(main)