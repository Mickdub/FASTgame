from slandscapes.landscapes import landscape
import numpy as np

def rugged_landscape(grid_size=(100,30),
                     noise=True,
                     backtrack=False,
                     diagonals=False,
                     b_height=5,
                     b_width=2,
                     b_length=1,
                     num_barrs = 5):
    """Generate a map for gameplay. A map is a grid of discrete points with transition
       probabilities between points. Addition of noise and barriers makes the mazes interesting   

    Keyword arguments:
    noise -- Alter transition probabilities on grid from flat to noisy (default True)
    backtrack -- Force maps to contain trap regions where a player needs 
    to back track to progress (default False)
    diagonals -- Make barriers angled instead of only 90/180 degrees
    b_height -- Value (in kcal/mol) is proportional to how unlikely it is to cross a
    barrier (default = 5)
    b_width -- Width of barriers in grid pixels (default 2)
    b_length -- Length of barriers in units of 1/3 the width of the map (default 1)
    num_barrs --  number of barriers (deafult 5)
    """
    x_dim = grid_size[0]
    y_dim = grid_size[1]
    l = landscape(grid_size)
    if noise:
        l = l.add_noise(gaussians_per_axis=int(0.5*y_dim),height_range=[0.5,0.5],width_range=[-2,2])
    #Add in barriers 
    #Distribution to draw barrier segment lengths from
    mu_d = (np.min(grid_size) / 3) * b_length
    sig_d = (np.min(grid_size) / 5) * b_length
    num_barrs = instructions[key]
    all_barrs = []
    x_spacing = x_dim / num_barrs
    for b in range(num_barrs):
        y = np.random.randint(y_dim)
        x = np.random.randint(b*(x_spacing),(b+1)*(x_spacing)) #along x-axis
        start = [y,x]
        dist = np.random.normal(mu_d,sig_d, 1)[0]
        if diagonals:
            angle = np.random.randint(360)
        else:
            angle = np.random.choice([0,90,180,270])
        if backtrack and np.random.random(1)[0] > 0.95:
        # make the barrier long enough to definitely reach edge
            dist = y_dim
            if start[0] <= (y_dim / 2):
                angle = np.random.randint(40,70)
                print(angle,start)
            else:
                angle = np.random.randint(290,320)
                print(angle,start)
        points = l.add_barrier(height=b_height,width=b_width,start=start,dist=dist,angle=angle,draw=False)
        all_barrs.append(points)
        uniq_barrs = np.unique(np.concatenate(all_barrs),axis=0)
        for p in uniq_barrs:
            l.values[p[0],p[1]] = b_height
    return l
