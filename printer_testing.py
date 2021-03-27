from escpos.printer import Serial

def printing(fn, date, tx0, tx1, tx2, tx3):
    p = Serial(devfile='COM4',
            baudrate=9600,
            bytesize=8,
            parity='N',
            stopbits=1,
            timeout=1.00,
            dsrdtr=True)

    p.text("                      SOJETEX \n                 "+date+"\nProduit:                  "+tx0+"\n------------------------------------------------\nTotal:                               "+tx1+"TND\nCredit:                               "+tx2+"TND\nPaye:                                "+tx3+"TND\n\n            merci pour votre visite \n")
    #p.qr("You can readme from your smartphone")
    p.cut()
    if fn == 0:
        p.cashdraw(2)
    else:
        pass

#printing("08/03/2021", "250", "0", "250")

