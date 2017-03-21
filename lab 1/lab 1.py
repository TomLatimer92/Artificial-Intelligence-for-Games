import time
# There is no section as to where the states and other variables should go.
# It is recommended to insert them at the top of the page like any other oop language.

# Variables
Health = 20
Damage = 0
Block = False

# States that will be used throughout the program.
states = ['Defence','Attack','Support']
Current_State = 'Attack'

# Other Variables
Running = True
Max_Limit = 10
Game_Time = 0

# While statement used when certain states are met.
while Running:
    Game_Time += 1
    time.sleep(1)
    print("Health Points:", Health)
    print("Damage Taken:", Damage)
    print("Time:", Game_Time)
    
    # Defence: Reduces damage, Health still decreases
    if Current_State is 'Defence' :
        # Do things for this state
        print("Blocking")
        Block = True
        # Check for change state
        if Block is True:
            print("Blocked Attack")
            Damage += 5
            Health -= 5
            Current_State = 'Attack'

    # Support: Heals Either Defending or Attacking Player. 
    elif Health < 5:
    # elif Health in range(1,5):
        print ("Change to support state")
        Current_State = 'Support'
        # Do things for this state
        Damage += 5
        Health += 5
        print("Healing Player...")
        # Check for change state
        # if Health is 20:
        Current_State = 'Attack'
        # if Health < 20:
        # Current_State = 'Defence'

   # Attack: Attacks Defending player, causes damage
    elif Current_State is 'Attack':
        # Do things for this state
        Health -= 5
        print("Attacking Defending Player")
        # Check for change state
        # if Health is 20:
        Current_State = 'Defence'
        # if Health < 20:
        #  Current_State = 'Attack'				    
			
    # check for broken code...
    else:
        print("AH! BROKEN")
        die() 
		
    # Check if the game has finished
    if Game_Time > Max_Limit:
        Running = False
        break

    # doesn't work!
    elif Health < 0: 
            Running = False
            break
            
    elif Damage > 30:
            Running = False
            break
		
# Print conclusion to loop.
print('-- The End --')


    
