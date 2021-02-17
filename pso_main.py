#import the important libraries
import numpy as np
import random
import matplotlib.pyplot as plt
from matplotlib import animation

#from the plotter.py file import the plot_anim function to make the simulations

from plotter import plot_anim
from IPython.display import Image

SHWEFEL = True
BANANA = True

#class particle to define the attributes for each particle in the swarm

class Particle():
    
    #initializing the initial positions, velocity, personal best position, personal best fitness value 
    
    def __init__(self, bounds):
        self.pos = np.array([random.randrange(bounds[0], bounds[1]),random.randrange(bounds[0], bounds[1])])
        self.velocity = np.array([0,0])
        self.personal_bestpos = []
        self.personal_bestfit = float('inf')


# function to calculate the fitness value using the banana function
#and the shwefel function depending on the if case

def fit_func(func, particle_pos):
    if func == "banana":
        fit = (1 - particle_pos[0]) ** 2 + 100 * (particle_pos[1] - particle_pos[0] ** 2) ** 2
    elif func == "shwefel":
        z = particle_pos[0]*np.sin(np.sqrt(np.fabs(particle_pos[0]))) + particle_pos[1]*np.sin(np.sqrt(np.fabs(particle_pos[1])))
        fit = float(418.9829*2) - (z.astype(np.float))
        # print("fit", fit)
        # print("z", z)
    return fit

#Update the personal best fitness value and best position of a particle

def update_pbest(particle, fitness):
    if particle.personal_bestfit > fitness:
        particle.personal_bestfit = fitness
        particle.personal_bestpos = particle.pos
    return particle

#Update the global best fitness value and global best position of the swarm 

def update_gbest(particle, fitness):
    global global_bestfit
    global global_bestpos
    if global_bestfit > fitness:
        global_bestfit = fitness
        global_bestpos = particle.pos

#Update the velocity of particles using the hyperparameters:
#W = weight, c1 = cognitive coeficient, c2 = social coeficient 

def update_velocity(particle):
    W=0.8
    c1=0.5
    c2=0.3
    v =np.array([0.,0.])
    for i in range(2):
        r1=random.random()
        r2=random.random()
        cog_vel = c1*r1*(particle.personal_bestpos[i]-particle.pos[i])
        social_vel = c2*r2*(global_bestpos[i]-particle.pos[i])
        v[i] = float(((W*particle.velocity[i]) + cog_vel + social_vel))
    return v

if SHWEFEL:

    #implementation and simulation of the shwefel function using PSO algorithm 
    lr = 1
    limits=[(-500, 500 ), (-500, 500)]
    figsize =(10, 8)
    bounds = [-500,500]
    n_particles = 50
    iterations = 800
    
    #initialize the particles for the swarm
    
    swarm_particles = [Particle(bounds) for _ in range(n_particles)]
    
    #initializing the global best fitness value and the global best position
    
    global_bestfit = float('inf')
    global_bestpos = []
    target_val = 0
    min_err_criteria = 0.00001
    pos_history = []
    for i in range (iterations):
        for p in range (n_particles):
            
            #calculate fitness value of a particle using the banana function
            
            fitness = fit_func("shwefel", swarm_particles[p].pos)
            
            #update the personal best fitness value and best position of particle
            #using the update_pbest()function
            
            swarm_particles[p]= update_pbest(swarm_particles[p],fitness)
            
            #update the global best fitness value and global best position
            #of swarm using the update_gbest() function
            
            update_gbest(swarm_particles[p],fitness)
        
        #storing the postion of every particle in the swarm to use it as a history
        #when we are making the simulation of the PSO
        
        pos = [swarm_particles[p].pos for p in range (n_particles)]
        pos_history.append(np.array(pos))
        
        #if minimum error criteria is reached stop the iterations
        
        if (abs(global_bestfit - target_val) < min_err_criteria):
            print("err", global_bestfit)
            break;
        for p in range (n_particles):
            
            #update the velocity of each particle using the update_velocity() function
            
            velocity = update_velocity(swarm_particles[p])
            swarm_particles[p].velocity = velocity
            
            #update the particle positions based on the updated velocity
            
            swarm_particles[p].pos = swarm_particles[p].pos + (lr * swarm_particles[p].velocity)
            
            #keep the particles inside the defined bounds
            
            if swarm_particles[p].pos[1]>bounds[1]:
                swarm_particles[p].pos[1]=bounds[1]
            if swarm_particles[p].pos[1]<bounds[0]:
                swarm_particles[p].pos[1]=bounds[0]
            if swarm_particles[p].pos[0]>bounds[1]:
                swarm_particles[p].pos[0]=bounds[1]
            if swarm_particles[p].pos[0] < bounds[0]:
                swarm_particles[p].pos[0]=bounds[0]
        # print("The best position is ", global_bestpos, "in iteration ", i)
        # if (i == (iterations-1)) and (abs(global_bestfit - target_val)>min_err_criteria):
        #     print("best position not reached, iterations increased")
        #     iterations = iterations + 100
    print("The best position is ", global_bestpos, "in iteration number ", iterations)
    
    # construct the video simulation using the plot_anim function in the plotter.py file
    
    animation = plot_anim(pos_history=pos_history,
                              limits = limits,
                              title = "trajectory",
                              figsize = figsize,
                              mark=(420.9687,420.9687))
    
    animation.save('shwefel1.mp4', writer='ffmpeg',fps=5)
    Image(url='shwefel1.mp4')

if BANANA:

    #implementation and simulation of the Banana function using the PSO algorithm
    lr = 1
    limits=[(-10, 10 ), (-10, 10)]
    figsize =(10, 8)
    bounds = [-10,10]
    n_particles = 50
    iterations = 600
    
    #initialize the particles for the swarm
    
    swarm_particles = [Particle(bounds) for _ in range(n_particles)]
    
    #initializing the global best fitness value and the global best position
    
    global_bestfit = float('inf')
    global_bestpos = []
    target_val = 0
    min_err_criteria = 0
    pos_history = []
    for i in range (iterations):
        for p in range (n_particles):
            
            #calculate fitness value of a particle using the banana function
            
            fitness = fit_func("banana", swarm_particles[p].pos)
            
            #update the personal best fitness value and best position of particle
            #using the update_pbest()function
            
            swarm_particles[p]= update_pbest(swarm_particles[p],fitness)
            
            #update the global best fitness value and global best position
            #of swarm using the update_gbest() function
        
            update_gbest(swarm_particles[p],fitness)
        
        #storing the postion of every particle in the swarm to use it as a history
        #when we are making the simulation of the PSO
        
        pos = [swarm_particles[p].pos for p in range (n_particles)]
        pos_history.append(np.array(pos))
        
        #if minimum error criteria is reached stop the iterations
        
        if (abs(global_bestfit - target_val) < min_err_criteria):
            print("err", global_bestfit)
            break;
        for p in range (n_particles):
            
            #update the velocity of each particle using the update_velocity() function
            
            velocity = update_velocity(swarm_particles[p])
            swarm_particles[p].velocity = velocity
            
            #update the particle positions based on the updated velocity
            
            swarm_particles[p].pos = swarm_particles[p].pos + (lr * swarm_particles[p].velocity)
            
            #keep the particles inside the defined bounds
            
            if swarm_particles[p].pos[1]>bounds[1]:
                swarm_particles[p].pos[1]=bounds[1]
            if swarm_particles[p].pos[1]<bounds[0]:
                swarm_particles[p].pos[1]=bounds[0]
            if swarm_particles[p].pos[0]>bounds[1]:
                swarm_particles[p].pos[0]=bounds[1]
            if swarm_particles[p].pos[0] < bounds[0]:
                swarm_particles[p].pos[0]=bounds[0]
    
    print("The best position is ", global_bestpos, "in iteration number ", iterations)
    
    # construct the video simulation using the plot_anim function in the plotter.py file
    
    animation = plot_anim(pos_history=pos_history,
                              limits = limits,
                              title = "trajectory",
                              figsize = figsize,
                              mark=(1,1))
    
    animation.save('banana1.mp4', writer='ffmpeg',fps=5)
    Image(url='banana1.mp4')