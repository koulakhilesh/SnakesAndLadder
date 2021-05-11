# -*- coding: utf-8 -*-
"""
Created on Wed Apr 28 10:12:14 2021

@author: akhilesh.koul
"""

import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_theme()

class snake_n_ladder:
    
    def __init__(self,player_num=2, epoch_plays_num=3,iteration_plays_num=10):
        
        self.player_num=player_num
        self.current_state = np.empty(player_num,dtype=object)
        self.win_prob=np.zeros(player_num,dtype=object)
        self.size=100
        self.ini_game_map()
        self.epoch_plays_num = epoch_plays_num
        self.iteration_plays_num= iteration_plays_num
        
        print("\n"+str(self.player_num) + " player game, playing for "+str(self.epoch_plays_num) + " epochs and " +str(self.iteration_plays_num) + " iterations per epoch")
      
        
    def reset_game(self):
        for i in range(np.shape(self.current_state)[0]):
            self.current_state[i]=-1
        
    def ini_game_map(self):

        
        self.game_map=np.empty(self.size,dtype=object)

        for i in range(np.shape(self.game_map)[0]):
            self.game_map[i]=['0','0',i]
    
        #ladders
        self.game_map[0]=['0','1',37]
        self.game_map[3]=['0','1',13]
        self.game_map[8]=['0','1',30]
        self.game_map[20]=['0','1',41]
        self.game_map[27]=['0','1',83]
        self.game_map[35]=['0','1',43]
        self.game_map[50]=['0','1',66]
        self.game_map[70]=['0','1',90]
        self.game_map[79]=['0','1',99]
        
        #snakes
        self.game_map[15]=['1','0',5]
        self.game_map[46]=['1','0',25]
        self.game_map[48]=['1','0',10]
        self.game_map[55]=['1','0',52]
        self.game_map[61]=['1','0',18]
        self.game_map[63]=['1','0',59]
        self.game_map[86]=['1','0',23]
        self.game_map[92]=['1','0',72]
        self.game_map[94]=['1','0',74]
        self.game_map[97]=['1','0',77]
 

        
    
    def play_dice(self):
        # print('\nNew dice play')
        old_state=self.current_state
        # print('current_state = '+str(self.current_state))
        
        dice=np.random.randint(low=1,high=7,size=self.player_num)
        # print('dice = '+str(dice))
        self.new_current_state=self.current_state + dice
        # print('new_current_state = '+str(self.new_current_state))

        new_state=self.check_game(self.current_state,self.new_current_state)
        
        # print('old_state = ' +str(old_state))
        # print('new_state = ' +str(new_state))
        self.current_state=new_state
        
        return old_state,new_state
        
        
        
    def check_game(self,current_state,new_current_state):
        
        updated_state=np.empty_like(self.current_state)
        # print(new_state)
        for i in range(np.shape(updated_state)[0]):
            if (new_current_state[i]<=self.size-1):
                # print(self.game_map[new_current_state[i]][2])
                updated_state[i]=self.game_map[new_current_state[i]][2]
                
                # print(updated_state)
            
            if (new_current_state[i]>self.size-1):
                # print("Didn't got the exact number")
                # print(self.game_map[current_state[i]][2])
                updated_state[i]=self.game_map[current_state[i]][2]
                # print(updated_state)
        
        return updated_state   

    def play_god(self):       


        epoch_plays=[]
        epoch_plays_num=self.epoch_plays_num
        
        # for j in tqdm(range(epoch_plays_num),position=0):
        for j in range(epoch_plays_num):
        
            iteration_plays=[]
            iteration_plays_num=self.iteration_plays_num
            
            
            total_number_plays=0
            iteration=[]
            average_per_iteration=[] 
            
            for i in range(iteration_plays_num): 
                plays=[]    
                self.reset_game()
                stop_criteria=False
                while stop_criteria==False :  
                    
                    old_state,new_state=self.play_dice()
                    plays.append([old_state,new_state])
                    # print("new_state = "+str(new_state))
                    # print(np.argwhere(new_state == 99))
                    # if (np.where(new_state ==99)[0]):
                    # win=np.where(new_state==99)[0]
                    # if(win.size!=0):
                        # print(win[0])
                        # print(win.size)
                        # self.win_prob[win[0]]+=1
                        
                    stop_criteria = 99 in new_state
                    
            
                    
                total_number_plays+=len(plays)
                iteration_plays.append(plays)
                iteration.append(i)
                average_per_iteration.append(total_number_plays/(i+1))      
                
            # print("\nAverge number of dice plays for " +str(iteration_plays_num) + " iteration = " +str(total_number_plays/iteration_plays_num)) 
            
            epoch_plays.append(iteration_plays)
            
            # plt.scatter(iteration,average_per_iteration,marker='.',label=j)
        # plt.ylim(0,100)
        # plt.show()
        
        total_score=0
        total_iteration=len(epoch_plays)*len(iteration_plays)
        
        for k in range(len(epoch_plays)):
            
            for l in range(len(epoch_plays[k])):
                
                # print(len(epoch_plays[k][l]))
                total_score+=len(epoch_plays[k][l])
                
        
        print("\nAverage number of round plays to finish the "+str(self.player_num) + " player game in " + str(epoch_plays_num) +" epochs = " +str(total_score/total_iteration))
        
        return total_score/total_iteration,self.win_prob/(self.epoch_plays_num *self.iteration_plays_num)



player_list=np.arange(1,10)
avg_rounds_list=[]
player_win_prob=[]
for player in tqdm(player_list):
    game=snake_n_ladder(player_num=player, epoch_plays_num=10,iteration_plays_num=100000)
    avg_round,win_prob=game.play_god()
    avg_rounds_list.append(avg_round)
    player_win_prob.append(win_prob)
    # print("\nWinning probabilty = "+str(win_prob))

plt.plot(player_list,avg_rounds_list)
plt.ylim(0,50)
plt.show()


