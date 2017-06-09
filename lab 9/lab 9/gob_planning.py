'''Goal Oriented Behaviour

Clinton Woodward, 2015, cwoodward@swin.edu.au
Works with Python 3+

Please don't share this code without permission.

Simple decision approach.
* Choose the most pressing goal (highest insistence value)
* Find the action that fulfills this "goal" the most (ideally?, completely?)

Goal: Eat (initially = 4)
Goal: Sleep (initially = 3)

Action: get raw food (Eat -= 3)
Action: get snack (Eat -= 2)
Action: sleep in bed (Sleep -= 4)
Action: sleep on sofa (Sleep -= 2)


Notes:
* This version is simply based on dictionaries and functions.

'''

VERBOSE = True

# Global goals with initial values
goals = {
	'Enemy Warrior HP': 25,
	'HP': 0,
	'Stamina': 0,
}

# Global (read-only) actions and effects
actions = {
	'Overhead Swing': { 'Enemy Warrior HP': -5, 'Stamina': 5, 'HP': 3},
	'Forward Thrust': { 'Enemy Warrior HP': -6, 'Stamina': 2,'HP': 5},
	'Shield': {'Enemy Warrior HP': -1, 'Stamina': -5,'HP': -5},
	'Vorpal Strike': {'Enemy Warrior HP': -15, 'Stamina': 7, 'HP': 9}
}


def apply_action(action):
	'''Change all goal values using this action. An action can change multiple
	goals (positive and negative side effects).
	Negative changes are limited to a minimum goal value of 0.
	'''
	for goal, change in list(actions[action].items()):
		goals[goal] = max(goals[goal] + change, 0)


def action_utility(action, goal):


	if goal in actions[action]:
		# Is the goal affected by the specified action?
		return -actions[action][goal]
	else:
		# It isn't, so utility is zero.
		return 0

	### Extension
	###
	###  - return a higher utility for actions that don't change our goal past zero
	###  and/or
	###  - take any other (positive or negative) effects of the action into account
	###    (you will need to add some other effects to 'actions')


def choose_action():
	'''Return the best action to respond to the current most insistent goal.
	'''
	assert len(goals) > 0, 'Need at least one goal'
	assert len(actions) > 0, 'Need at least one action'

	# Find the most insistent goal - the 'Pythonic' way...
	best_goal, best_goal_value = max(list(goals.items()), key=lambda item: item[1])

	# ...or the non-Pythonic way. (This code is identical to the line above.)
	#best_goal = None
	#for key, value in goals.items():
	#    if best_goal is None or value > goals[best_goal]:
	#        best_goal = key

	if VERBOSE: print('BEST_GOAL:', best_goal, goals[best_goal])

	# Find the best (highest utility) action to take.
	# (Not the Pythonic way... but you can change it if you like / want to learn)
	best_action = None
	best_utility = None
	for key, value in actions.items():
		# Note, at this point:
		#  - "key" is the action as a string,
		#  - "value" is a dict of goal changes (see line 35)

		# Does this action change the "best goal" we need to change?
		if best_goal in value:

			# 	# # Do we currently have a "best action" to try? If not, use this one
			if best_action is None:
				best_action = key
				best_utility = action_utility(best_action, best_utility)
				### 1. store the "key" as the current best_action
				### ...
				### 2. use the "action_utility" function to find the best_utility value of this best_action
				### ...
				# Is this new action better than the current action?
			else:
				# utility_value = action_utility(key, best_goal)
				# if utility_value > best_utility:
				# 	best_action = key
				# 	best_utility = utility_value
				utility_action = action_utility(best_action, best_utility)
				if best_utility < utility_action:
					best_utility = utility_action
				elif utility_action > best_utility:
					best_action = key
				### 1. use the "action_utility" function to find the utility value of this action
				### ...
				### 2. If it's the best action to take (utility > best_utility), keep it! (utility and action)
				### ...
			# Return the "best action"
	return best_action
#==============================================================================
#Discontentment
def discontentment():
	discontentment = 0
	for key, value in goals.items():
		discontentment +=value*value
	return discontentment

def retrieve_discontent(action, goal_list):
	discontent = 0
	for goal, change in list(actions[action].items()):  # adds discontentment to the list of goals and changes
		temporary = max(goal_list[goal]+change, 0)
		discontent += temporary*temporary
	return discontent

def preferredAction(goal_list):
	best_discontentment = 99999
	best_action = None
	for key, value in actions.items():
		currentDis = retrieve_discontent(key, goal_list)
		print(key, '(', current_discontentment, ')')
		if currentDis < best_discontentment:
			best_discontentment = currentDis
			best_action = key
	return best_action

def test(action, goal_list):
	temporary = goal_list.copy()
	for goal, change in list( actions[action].items()):
		temporary[goal] = max(temporary[goal] +change, 0)
	return temporary

def choice(maxDepth):

	best_action = None
	best_action2 = None
	best_action3 = None
	best_discontent = 999999
	best_plan = [None] * 3

	if VERBOSE:
		print('Now Searching')

	for key, value in actions.items():
		depth = maxDepth
		print('Step 1: ', key)
		run_discontentment = retrieve_discontent(key,goals)
		print('level of discontentment at: ', run_discontentment)
		best_action = key
		temporary = test(best_action, goals)
		print(' new goals: ', temporary)
		depth -= 1
		if depth > 0:

			for key, value in actions.items():
				depth = maxDepth - 1
				print('Step 2: ', key)
				best_action2 = key
				temporary = test(best_action, goals)
				temporary = test(best_action2, temporary)
				run_discontentment = retrieve_discontent(key,temporary)
				print('level of discontentment at: ', run_discontentment)
				print(' new goals: ', temporary)
				depth -= 1
				if depth > 0:

					for key, value in actions.items():
						depth = maxDepth - 1
						print('Step 2: ', key)
						best_action3 = key
						temporary = test(best_action, goals)
						temporary = test(best_action2, temporary)
						temporary = test(best_action3, temporary)
						run_discontentment = retrieve_discontent(key,goals)
						print('level of discontentment at: ', run_discontentment)
						print(' new goals: ', temporary)

						print('                ---> running: ', run_discontentment, ' best: ', best_discontent)
						if run_discontentment < best_discontent:
							best_discontent = run_discontentment
							best_plan[0] = best_action
							best_plan[1] = best_action2
							best_plan[2] = best_action3
				else:
					print('running: ', run_discontentment, ' best: ', best_discontent)
					if run_discontentment < best_discontent:
						best_discontent = run_discontentment
						best_plan[0] = best_action
						best_plan[1] = best_action2
		else:
			print('running: ', run_discontentment, ' best: ', best_discontent)
			if run_discontentment < best_discontent:
				best_discontent = run_discontentment
				best_plan[0] = best_action
	print('best plan is: ', best_plan)
	return best_plan

#==============================================================================

def print_actions():
	print('ACTIONS:')
	for name, effects in list(actions.items()):
		print(" * [%s]: %s" % (name, str(effects)))

def run_until_all_goals_zero():
	HR = '-'*40
	print_actions()
	print('>> Start <<')
	print(HR)
	running = True
	while running:
		print('GOALS:', goals)
		# What is the best action
		action = choice(1)
		print('now doing...')
		i = 0
		#apply best action
		while i < 1:
			print('CURRENT BEST ACTION:', action[i])
			apply_action(action[i])
			i += 1
		print('NEW GOALS:', goals)
		#check to stop if fulfilled
		if all(value == 0 for goal, value in list(goals.items())):
			running = False
		if goals['HP'] > 25 :
			print('You have died')
			running = False
		if goals['Enemy Warrior HP'] <= 1:
			print('You have bested me! Aarrgghh')
			running = False
		print(HR)
	# finished
	print('>> Done! <<')

if __name__ == '__main__':
	run_until_all_goals_zero()
