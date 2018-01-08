WIDTH=20
HEIGHT=20
TITLE='Scoring Test'

def bigscore1(s):
   score(9999999999)
   s.destroy()

def bigscore2(s):
   score(-9999999999)
   s.destroy()


shape(CIRCLE, RED, (1,1)).bouncy().clicked(bigscore1)
shape(CIRCLE, BLUE, (9,9)).bouncy().clicked(bigscore2)



