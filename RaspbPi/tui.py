import curses

## TUI

screen = curses.initscr()
curses.noecho()
curses.cbreak()
screen.keypad(True)
curses.curs_set(0)
screensize = screen.getmaxyx()

wthirds = int(screensize[1]/3)
hthirds = int(screensize[0]/3)

def centercol(w,col):
    if col>3:
        col = 3
    colcenter = int(((wthirds / 2) + ( wthirds * (col-1))) - (len(w) // 2))
    return colcenter
def centerrow(h,row):
    if row>3:
        row = 3
    rowcenter = int(((hthirds / 2) + ( hthirds * (row-1))) - h)
    return rowcenter

# FIRST ROW

boxSOC = screen.subwin(hthirds,wthirds, 0, 0)
boxSOC.box()
screen.addstr(0, centercol(" S O C % ",1), " S O C % ")

boxCurrent = screen.subwin(hthirds,wthirds, 0, wthirds)
boxCurrent.box()
screen.addstr(0, centercol(" Current (A) ",2), " Current (A) ")

boxPack = screen.subwin(hthirds,wthirds, 0, wthirds * 2)
boxPack.box()
screen.addstr(0, centercol(" Pack (V) ",3), " Pack (V) ")

# SECOND ROW

boxSOC = screen.subwin(hthirds,wthirds, hthirds, 0)
boxSOC.box()
screen.addstr(hthirds, centercol(" Cell High (mV) ",1), " Cell High (V) ")

boxCurrent = screen.subwin(hthirds,wthirds, hthirds, wthirds)
boxCurrent.box()
screen.addstr(hthirds, centercol(" Cell High (C) ",2), " Cell High (C) ")

boxPack = screen.subwin(hthirds,wthirds, hthirds, wthirds * 2)
boxPack.box()
screen.addstr(hthirds, centercol(" PCB High (C) ",3), " PCB High (C) ")

# THIRD ROW

boxSOC = screen.subwin(hthirds,wthirds, hthirds*2, 0)
boxSOC.box()
screen.addstr(hthirds*2, centercol(" Cell Low (mV) ",1), " Cell Low (V) ")

boxCurrent = screen.subwin(hthirds,wthirds, hthirds*2, wthirds)
boxCurrent.box()
screen.addstr(hthirds*2, centercol(" Cell Low (C) ",2), " Cell Low (C) ")

boxPack = screen.subwin(hthirds,wthirds, hthirds*2, wthirds * 2)
boxPack.box()
screen.addstr(hthirds*2, centercol(" PCB Low (C) ",3), " PCB Low (C) ")

screen.refresh()

# STATUS ROW

screen.addstr((hthirds*3)-1, 1, " ERR: ")

## END TUI