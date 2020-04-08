"""
Ecuacion de onda en una cuerda
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation


#%%
# Datos

L = 1 #longitud de la cuerda
T = 40 #tension
mu = 0.01 #densidad lineal de la cuerda
v = (T/mu)**0.5 #velocidad de propagacion
v_prim = v #CFL: v<=v'=delta(x)/delta(t)

#%%
# Desplazamiento vertical
y = np.zeros((100,1000)) # y[filas=x][columnas=t]

#Condiciones iniciales
#for i in range(0,81): y[i,0] = 0.00125*i
#for i in range(81,100): y[i,0] = 0.1 - 0.005*(i-80)

# Forma mas simple y eficiente de inicializar condiciones iniciales (NOTA: no uses muchos bucles)
y[:, 0] = np.array([0.00125*i for i in range(100) if i<81 else 0.1 - 0.005*(i-80)])
                       

    
#Algoritmo
#for i in range(1,99): 
#    y[i,1] = 2*y[i,0]-y[i,0] + 0.5*(v/v_prim)**2*(y[i+1,0]+y[i-1,0]-2*y[i,0])
#for i in range(1,99):
#    y[i,2] = 2*y[i,1]-y[i,1] + 0.5*(v/v_prim)**2*(y[i+1,1]+y[i-1,1]-2*y[i,1])
#NOTA: Estabas haciendo doble iteracion para algo que solo necesitaba solo una iteracion, en este caso es tolerable pues son numeros perqueños pero si tu iteracion
# fuera sobre 1, 2, ...., 10000000000000000000000000000, tu programa te daria un pesimo rendimiento, asi que trata de evitar usar mucho bucles
fun = lambda y, i, v, v_prim: 2*y[i,1]-y[i,1] + 0.5*(v/v_prim)**2*(y[i+1,1]+y[i-1,1]-2*y[i,1])   
y[:, 1:3]= np.array([[fun(i, 1), fun(i, 2)] for i in range(99)])

for i in range(1,99):
    for j in range(2,999):
        y[i,j+1] = 2*y[i,j]-y[i,j-1] + 0.5*(v/v_prim)**2*(y[i+1,j]+y[i-1,j]-2*y[i,j])


        
#%%
# Plot 

x_plot = np.linspace(0,1,100)

for i in range(0,10):
    y_plot = y[:,i]
    plt.plot(x_plot,y_plot)
    
#%%
#Animation
    
fig = plt.figure()
ax = plt.axes(xlim=(0, 1), ylim=(-0.5, 0.5))
line, = ax.plot([], [], lw=1)

def init():
    line.set_data([], [])
    return line,

def animate(i):
    x_an = np.linspace(0,1,100)
    y_an = y[:,i]
    line.set_data(x_an, y_an)
    return line,

anim = animation.FuncAnimation(fig, animate, init_func=init,
                               frames=200, interval=10, blit=True)

anim.save('string.mp4', fps=30, extra_args=['-vcodec', 'libx264'])
