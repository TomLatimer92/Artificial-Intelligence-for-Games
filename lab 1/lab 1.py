# Three state machine example ... bad code included.
# There is no section as to where the states and other variables should go. IT is recommended to insert them at the top of the page like any other oop language.

# variables
Tired = 0
Hunger = 0
Health = 20
Damage = 0
Block = 0

# States that will be used throughout the program.
states = ['Sleeping','Awake','Eating','Defence','Attack','Support']
Current_State = 'Sleeping'

# Other Variables
Running = True
Alive = True
Max_Limit = 100
Game_Time = 0

# While statement used when certain states are met.
while Running and Alive:
   Game_Time += 1

    # Sleeping: reduces tired state, hunger still increases though.
    # if current_state is 'sleeping':
    # Do things for this state
    # print("Zzzzzz")
    # tired -= 1
    # hunger += 1
    # Check for change state
    # if tired < 5:
    # current_state = 'awake'
	
	 # Defence: Reduces damage, Health still decreases
    if current_state is 'Defence':
        # Do things for this state
        print("Blocked Attack")
        Health -= 3
        # Check for change state
        if Defence = Block:
            Current_State = 'Attack'

    # Awake: does nothing interesting. gets hunugry. gets tired
    # elif current_state is 'awake':
    # Do things for this state
    # print("Bored.... BORED! ...")
    # tired += 1
    # hunger += 1
    # Check for change state
    # if hunger > 7:
    # current_state = 'eating'
    # if tired > 16:
    # current_state = 'sleeping'
			
	# Support: Heals Either Defending or Attacking Player. 
    elif current_state is 'Support':
        # Do things for this state
        print("Healing Player...")
        Health += 5:
        # Check for change state
        if Health = 20:
            Current_State = 'Attack'
        if Health < 20:
            current_state = 'Defence'
            
    # Eating: reduces hunger, still gets tired
    # elif current_state is 'eating':
    # Do things for this state
    # print("Num, num, num...")
    # tired += 1
    # hunger -= 1
    # Check for change state
    # if hunger < 8:
    # current_state = 'awake'
			
	# Attack: Attacks Defending player, causes damage
    elif current_state is 'Attack':
        # Do things for this state
        print("Attacking Defending Player")
        Health -= 3
        # Check for change state
        if Health = 20:
            Current_State = 'Defence'
        if Health < 20:
            current_state = 'Attack'
            
    # check for broken ... :(
    # else:
    # print("AH! BROKEN .... how did you get here?")
    # die() # not a real function - just breaks things! :)
	
	# check for broken ... :(
    else:
        print("AH! BROKEN")
        die() 
	# not a real function - just breaks things! :)

    # if hunger > 20:
    # alive = False
		
	    if Health = 0;
	    alive = False
        
    # Check for end of game time
    if game_time > max_limit:
        running = False

print('-- The End --')


    
