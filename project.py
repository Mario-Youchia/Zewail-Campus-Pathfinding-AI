import cv2
import time
from math import sqrt
from math import exp 
import numpy as np
from copy import deepcopy
import matplotlib.pyplot as plt
from functions import Problem
import functions
image = cv2.imread('image.png')
scale_percent = 50 # percent of original size
rows = int(image.shape[1] * scale_percent / 100)
height = int(image.shape[0] * scale_percent / 100)
dim = (rows, height)
resized = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
new=deepcopy(resized)
print('Original Dimensions : ',image.shape)
print('Resized Dimensions : ',resized.shape)
ArrofColors=[[128,0,255],[164,73,163],[127,127,127],[195,195,195],[0,0,0],[255,255,255]
,[232,162,0],[255,255,128],[36,28,237]
,[87,122,185],[234,217,153],[0,242,255]
,[21,0,136],[255,0,0],[29,230,181]
,[201,174,255],[231,191,200],[76,177,34]
,[64,255,0],[204,72,63],[39,127,255]
,[190,146,112],[176,228,239],[14,201,255]
]
for i in range(height):
	for j in range(rows):
		arr=[]
		current=np.ndarray.tolist(resized[i][j])
		if(current not in ArrofColors):
			
			try:
				check1=np.ndarray.tolist(new[i][j+1])
				check2=np.ndarray.tolist(new[i][j-1])
				check3=np.ndarray.tolist(new[i+1][j])
				check4=np.ndarray.tolist(new[i-1][j])
				if(check1 in ArrofColors):
					new[i][j]=new[i][j+1]
				elif(check2 in ArrofColors):
					new[i][j]=new[i][j-1]
				elif(check3 in ArrofColors):
					new[i][j]=new[i+1][j]
				elif(check4 in ArrofColors):
					new[i][j]=new[i-1][j]
			except:
				pass

## Problem Definitions
class Map(Problem):

	def __init__(self,Map,init_state,goal_state):			
		self.RoomsPositions={"AB-ZA":(212,236),"AB-ZB"   :(191,262),"AB-ZC"   :(224,302),"AB-ZD"   :(253,285),"AB-ZE"   :(240,235),
"NB-S28"               :(186,183),"NB-S31"  :(192,180),"NB-F014" :(183,170),"NB-S024" :(183,170),"NB-S013" :(171,161),
"NB-S014"              :(175,155),"NB-G008" :(173,160),"HB-S024" :(295,190),"HB-F027" :(295,190),"HB-G006" :(293,209),"HB-G011" :(288,201)
,"HB-G002F"            :(300,198),"HB-S008" :(280,199),"HB-G016" :(305,183),"HB-G025" :(312,175)}
		self.room=None
		if(type(goal_state)!=tuple):
			self.room=goal_state
			assert goal_state in self.RoomsPositions.keys()
			goal_state=self.RoomsPositions[goal_state]
		assert init_state[0]>=0 and init_state[0]<=395 and init_state[1]>=0 and init_state[1]<=479
		assert goal_state[0]>=0 and goal_state[1]>=0 and goal_state[0]<=395 and goal_state[1]<=479
		self.Map=Map
		self.init_state=init_state
		self.goal_state=goal_state
		self.rows=395
		self.cols=479
		self.step=10
		self.buildings={(0,242,255)  :"NB" ,  (39,127,255) :"SB", (201,174,255):"HB",  (76,177,34) :"MS",  (21,0,136) :"AB"    ,      (232,162,0)  :"OS" ,
						(234,217,153):"CA" ,  (87,122,185) :"G1", (128,0,255)  :"G2",  (164,73,163):"G3",  (64,255,0) :"G4"    ,      (176,228,239):"G5"
					   ,(14,201,255) :"G6" ,  (195,195,195):"BD", (127,127,127):"GD",  (255,0,0)  :"ATM",  (36,28,237):"SS"    ,      (204,72,63):"WS"
					   ,(255,255,128):"OB" ,  (231,191,200):"PG", (190,146,112):"SC",  (29,230,181):"CF",  (255,255,255):"Road",      (0,0,0):"Block"    }
		self._action_values = {'left':(0,-self.step),'right':(0,+self.step) ,'down':(+self.step,0),'up':(-self.step,0),'downleft':(+self.step,-self.step),'downright':(+self.step,+self.step),'upleft':(-self.step,-self.step),'upright':(-self.step,+self.step)}
		self.costs={(0,0,0):2,(255,255,255):1.2,(255,255,128):1.5,(36,28,237):+1.1,(21,0,136):1,
					(0,242,255):1,(201,174,255):1,(234,217,153):1,(128,0,255):1.2,(164,73,163):1.2, 
					(127,127,127):1.2,(195,195,195):1.2,(232,162,0):1.2,(87,122,185):1.2,(255,0,0):1.2,
					(29,230,181):1.2,(231,191,200):1.2,(76,177,34):1.2,(64,255,0):1.2,(204,72,63):1.2,
					(39,127,255):1.2,(190,146,112):1.2,(176,228,239):1.2,(14,201,255):1.2}
		self.initialbuilding=self.Map[self.init_state[0]][self.init_state[1]]
		self.goalbuilding=self.Map[self.goal_state[0]][self.goal_state[1]]        #--> down    <-- up

	def actions(self, state):
		possible_moves = []
		#goal condition
		if(state[0]+self.step<=self.rows and (self.initialbuilding==self.Map[state[0]+self.step][state[1]] or self.Map[state[0]+self.step][state[1]]==[0,0,0] or self.Map[state[0]+self.step][state[1]]==[255,255,255] or self.Map[state[0]+self.step][state[1]]==[255,255,128] or self.goalbuilding==self.Map[state[0]+self.step][state[1]])):
			possible_moves.append('down')

		if(state[0]-self.step>=0 and (self.initialbuilding==self.Map[state[0]-self.step][state[1]] or self.Map[state[0]-self.step][state[1]]==[0,0,0] or self.Map[state[0]-self.step][state[1]]==[255,255,255] or self.Map[state[0]-self.step][state[1]]==[255,255,128] or self.goalbuilding==self.Map[state[0]-self.step][state[1]])):
			possible_moves.append('up') 

		if(state[1]+self.step<=self.cols and (self.initialbuilding==self.Map[state[0]][state[1]+self.step] or self.Map[state[0]][state[1]+self.step]==[0,0,0] or self.Map[state[0]][state[1]+self.step]==[255,255,255] or self.Map[state[0]][state[1]+self.step]==[255,255,128] or self.goalbuilding==self.Map[state[0]][state[1]+self.step])):
			possible_moves.append('right')

		if(state[1]-self.step>=0 and (self.initialbuilding==self.Map[state[0]][state[1]-self.step] or self.Map[state[0]][state[1]-self.step]==[0,0,0] or self.Map[state[0]][state[1]-self.step]==[255,255,255] or self.Map[state[0]][state[1]-self.step]==[255,255,128] or self.goalbuilding==self.Map[state[0]][state[1]-self.step])):
			possible_moves.append('left')

		if((state[0]-self.step>=0 and state[1]+1<=self.cols) and (self.initialbuilding==self.Map[state[0]-self.step][state[1]+self.step] or self.Map[state[0]-self.step][state[1]+self.step]==[0,0,0] or self.Map[state[0]-self.step][state[1]+self.step]==[255,255,255] or self.Map[state[0]-self.step][state[1]+self.step]==[255,255,128] or self.goalbuilding==self.Map[state[0]-self.step][state[1]+self.step])):
			possible_moves.append('upright')

		if((state[0]+self.step<=self.rows and state[1]+self.step<=self.cols) and (self.initialbuilding==self.Map[state[0]+self.step][state[1]+self.step] or self.Map[state[0]+self.step][state[1]+self.step]==[0,0,0] or self.Map[state[0]+self.step][state[1]+self.step]==[255,255,255] or self.Map[state[0]+self.step][state[1]+self.step]==[255,255,128] or self.goalbuilding==self.Map[state[0]+self.step][state[1]+self.step])):
			possible_moves.append('downright')

		if((state[0]-self.step>=0 and state[1]-self.step>=0) and (self.initialbuilding==self.Map[state[0]-self.step][state[1]-self.step] or self.Map[state[0]-self.step][state[1]-self.step]==[0,0,0] or self.Map[state[0]-self.step][state[1]-self.step]==[255,255,255] or self.Map[state[0]-self.step][state[1]-self.step]==[255,255,128] or self.goalbuilding==self.Map[state[0]-self.step][state[1]-self.step])):
			possible_moves.append('upleft')

		if((state[0]+self.step<=self.rows and state[1]-self.step>=0) and (self.initialbuilding==self.Map[state[0]+self.step][state[1]-self.step] or self.Map[state[0]+self.step][state[1]-self.step]==[0,0,0] or self.Map[state[0]+self.step][state[1]-self.step]==[255,255,255] or self.Map[state[0]+self.step][state[1]-self.step]==[255,255,128] or self.goalbuilding==self.Map[state[0]+self.step][state[1]-self.step])):
			possible_moves.append('downleft')
				
		return possible_moves


	def result(self, state, action):
		resultstate=[0,0]
		resultstate[0]=state[0]+self._action_values[action][0]
		resultstate[1]=state[1]+self._action_values[action][1]
		resultstate=tuple(resultstate)
		return resultstate
		
	def goal_test(self, state):
		dx=abs(state[0]-self.goal_state[0])
		dy=abs(state[1]-self.goal_state[1])
		if dx<self.step and dy<self.step:
			return True
		else:
			return False
	
	def step_cost(self, state, action):
		# step_state=self.result(state,action)
		# step_color=tuple(self.Map[step_state[0]][step_state[1]])
		# cost=self.costs[step_color]
		cost_calc=0
		new_move=[0,0]
		move=self._action_values[action]
		new_move[0]=int(move[0]/self.step)
		new_move[1]=int(move[1]/self.step)
		new_move=tuple(new_move)
		new_state=state
		def miniresult(state,move):
			resultstate=[0,0]
			resultstate[0]=state[0]+move[0]
			resultstate[1]=state[1]+move[1]
			resultstate=tuple(resultstate)
			return resultstate
		for i in range(self.step):
			step_state=miniresult(new_state,new_move)
			step_color=tuple(self.Map[step_state[0]][step_state[1]])
			cost_calc+=self.costs[step_color]
			new_state=step_state
		return cost_calc
	
	def heuristic(self, state):
		#Heurisitic 1 using minhateen distance
		# value=abs(state[0]-self.goal_state[0])+abs(state[1]-self.goal_state[1])
		 
		#Heurisitic 2 using Eculidean distance
		value=sqrt((state[0]-self.goal_state[0])**2+(state[1]-self.goal_state[1])**2)
		if value<self.step:
			return 0
		else:
			return value


def ourVisualizer(Actions,proplem):
	floors={"G":0,"F":1,"S":2,"Z":-1}
	inital=proplem.init_state
	goalbuilding=tuple(proplem.goalbuilding)
	listmoves=[]
	firsttime=0
	for action in Actions:
		newstate=proplem.result(inital,action)
		inital=newstate
		newbuilding=tuple(proplem.Map[newstate[0]][newstate[1]])
		if(newbuilding==goalbuilding and firsttime==0):
			firsttime=1
			print(f"Step into {proplem.buildings[goalbuilding]}")
			if(proplem.room!=None):
				floor=floors[proplem.room[3]]
				number=proplem.room[4:]
				if(floor==-1):
					print(f"Go to Zone {number}")
				elif(floor==0):
					print(f"Your destination is at Ground Floor, Follow the steps")
				elif(floor==1):
					print(f"Your destination is at First Floor, Please use Elivator!")
					print(f"Then follow the steps")
				elif(floor==2):
					print(f"Your destination is at Second Floor, Please use Elivator!")
					print(f"Then follow the steps")
			print(f"move to {newstate}")
			listmoves.append(newstate)
		else:
			print(f"move to {newstate}")
			listmoves.append(newstate)
		return listmoves

				



# plt.imshow(ZcMap)
# plt.show()

def program(start, user_input, dest, alg):
	rooms={1: "AB-ZA",   2:"AB-ZB" ,    3:"AB-ZC" ,  4:"AB-ZD" ,  5: "AB-ZE",
      6: "NB-S28",   7:"NB-S31" ,    8:"NB-F014" ,  9:"NB-S024" , 10: "NB-S013",  
     11: "NB-S014",  12:"NB-G008",   13: "HB-S024", 14: "HB-F027", 15: "HB-G006", 
     16: "HB-G011",  17:"HB-G002F", 18:   "HB-S008", 19: "HB-G016", 20: "HB-G025"}
	 
	ZcMap=np.ndarray.tolist(new)
	#start=input("Enter your start position (x,y):")
	#start=start.strip('(').strip(')').split(',')
	inital=tuple([int(start[0]),int(start[1])])
	#print(inital)
	#user_input=input("Choose how to Enter you Destination: 1)position(x,y) 2)Room:")
	if(int(user_input)==1):
		#dest=input("Enter your destination position (x,y):")
		#dest=dest.strip('(').strip(')').split(',')
		final=tuple([int(dest[0]),int(dest[1])])
	else:
		room=int(input("""Choose which room you want:\n1-AB-ZA    2-AB-ZB     3-AB-ZC    4-AB-ZD    5-AB-ZE 
6-NB-S28   7-NB-S31    8-NB-F014  9-NB-S024  10-NB-S013 
11-NB-S014 12-NB-G008  13-HB-S024 14-HB-F027 15-HB-G006 
16-HB-G011 17-HB-G002F 18-HB-S008 19-HB-G016 20-HB-G025\n"""))
		final=rooms[room]
	problem=Map(ZcMap,inital,final)
	# Actions =functions.A_star(problem)
	# ourVisualizer(Actions[0],problem)
	start_time = time.time()
	if alg == 1:
		states = functions.bfs_tree(problem)
	elif alg == 2:
		states = functions.dfs(problem)
	elif alg == 3:
		states = functions.ids(problem)
	elif alg == 4:
		states = functions.greedy_best_first(problem)
	elif alg == 5:
		states = functions.A_star(problem)
	elif alg == 6:
		final_state = functions.hill_climbing(problem)
		states = ([], 0)
	elif alg == 7:
		states = functions.simulated_annealing(problem,lambda t: exp(-t),True)
	else:
		states = functions.A_star(problem)
	print("--- %s seconds ---" % (time.time() - start_time))
	if isinstance(states, tuple) and len(states) >= 1:
		path_states = ourVisualizer(states[0], problem)
		return path_states, states
	return [], states

# init=(262,99)
# final=(178,158)
#program()
