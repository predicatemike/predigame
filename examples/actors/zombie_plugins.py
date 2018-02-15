# A Place for Gamer Customizations
def setup(level_number):
   """ setup is called for every level. this is a place to add new things. """
   # pick a single background
   #background('grass')

   # randomly pick a background
   #choices = ['grass', 'ville']
   #background(choice(choices))

   # pick a background for a level
   if level_number == 1:
      background('grass')
   elif level_number == 2:
      background('ville')
   else:
      background('stormy')

   # add a count down timer for 30 seconds
   timer(color=WHITE, value=30)


target = True
