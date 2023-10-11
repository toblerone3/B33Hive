from tkinter import *


def show_data():

    print( 'My First and Last Name are %s %s' % (fname.get(), lname.get()) )


win = Tk()
Label( win, text='Server IP' ).grid( row=0 )
Label( win, text='Port' ).grid( row=1 )

servIP = Entry( win )
port = Entry( win )

servIP.grid( row=0, column=1 )
port.grid( row=1, column=1 )

Button( win, text='Exit', command=win.quit ).grid( row=3, column=0, sticky=W, pady=4 )
Button( win, text='Connect', command=show_data ).grid( row=3, column=1, sticky=W, pady=4 )

mainloop()