import scipy.optimize
import numpy as np
from matplotlib import pyplot as plt
import pandas as pd
import functions as func

df = pd.read_csv('static/tables/antconst.csv')
names_antoine = list(df['Name'])

def get_diagrams(species_one, species_two, q, f, distillate, bottoms, R):
    x_values_line = [0, 1]
    y_values_line = [0, 1]
    

    index_one = df[df['Name'] == species_one].index.values
    index_two = df[df['Name'] == species_two].index.values
    ABC_one = df.iloc[index_one, 2:5].values.tolist()
    ABC_two = df.iloc[index_two, 2:5].values.tolist()
    print()
    print(ABC_one)
    print(df.iloc[index_one, 7].values)
    print()
    bp_one = float(df.iloc[index_one, 7].values)
    bp_two = float(df.iloc[index_two, 7].values)

    if bp_one < bp_two:
        # species one is light key
        species_light = species_one
        species_heavy = species_two
        step = (bp_two - bp_one) / 10
        bp_low = bp_one
        bp_high = bp_two
        ABC_low = ABC_one
        ABC_high = ABC_two
    else:
        # species two is light key
        species_light = species_two
        species_heavy = species_one
        step = (bp_one - bp_two) / 10
        bp_low = bp_two
        bp_high = bp_one
        ABC_low = ABC_two
        ABC_high = ABC_one

    temp_values = []
    pvap_light = []
    pvap_heavy = []
    x_one = []
    x_two = []
    y_one = []
    y_two = []

    for i in range(11):
        temp_values.append(bp_low + step * i)
        pvap_light.append(func.calculate_antoine(species_light, temp_values[i]))
        pvap_heavy.append(func.calculate_antoine(species_heavy, temp_values[i]))
    if min(pvap_light) > max(pvap_heavy):
        pvap_total = min(pvap_light)
    else:
        pvap_total = max(pvap_heavy)
    for i in range(11):
        x_one.append((pvap_total - pvap_heavy[i]) / (pvap_light[i] - pvap_heavy[i]))
        x_two.append(1 - x_one[i])
        y_one.append(x_one[i] * (pvap_light[i] / pvap_total))
        y_two.append(1 - y_one[i])

    




    x_one = np.asarray(x_one)
    y_one = np.asarray(y_one)

    coef = np.polyfit(x_one,y_one, 4)


    if q != 1 :

        roots_polynomial = np.roots([coef[0],coef[1],coef[2],coef[3]-(q/(q-1)),(f/(q-1))])

        x_rect_q = ((-f/(q-1))-((1/(R+1))*distillate))/((R/(R+1))-(q/(q-1)))
        y_rect_q = func.rectifying_line(R,x_rect_q,distillate)
        print(y_rect_q)





    # find the correct root
        for root in roots_polynomial:
            if root > 0:
                if root < 1:
                    correct_root = root

        poly_q_x = float(correct_root)
        poly_q_y = func.q_line(poly_q_x,f,q)




        q_x_values = np.linspace(f,poly_q_x, 100)


    else:
        x_rect_q = f
        y_rect_q = func.rectifying_line(R,x_rect_q,distillate)
        print('onion')



    def equation(x):
        y = coef[0]*x**4 + coef[1]*x**3 + coef[2]*x**2 + coef[3]*x
        return y
    rect_x_values = np.linspace(0, distillate, 100)
    eqlm_x_values = np.linspace(0,1,100)

    
    rect_y_values = func.rectifying_line(R, rect_x_values, distillate)
    eqlm_y_values = equation(eqlm_x_values)
    strip_x_values = [bottoms, x_rect_q]
    strip_y_values = [bottoms,y_rect_q]
    fortyfive_x_values = [0,1]
    fortyfive_y_values = [0,1]

    if q == 1:
        q_x_values = [f,f]
        q_y_values = [f,equation(f)]
    else:
        q_y_values = func.q_line(q_x_values, f, q)

    return species_light, rect_x_values ,rect_y_values, eqlm_x_values, eqlm_y_values, strip_x_values, strip_y_values, fortyfive_x_values, fortyfive_y_values, q_x_values, q_y_values


#
#
    #plt.plot(eqlm_x_values, equation(eqlm_x_values)) #Plots EQLM Line
    #plt.plot([0,1],[0,1]) #Plots 45 line
    #if q == 1:
    #    plt.plot([f,f],[f,equation(f)]) #plots q line
    #else:
    #    plt.plot(q_x_values, func.q_line(q_x_values,f,q))
#
    #plt.plot(rect_x_values,func.rectifying_line(R,rect_x_values,distillate))# Plots Rectifying line
    #plt.plot([bottoms,x_rect_q],[bottoms,y_rect_q]) # plots stripping line
    #plt.axis(xmin=0,xmax=1,ymin=0,ymax=1)
    #plt.xlabel('x fraction')
    #plt.ylabel('y fraction')
    #plt.title(str('xy '+species_light))
    #plt.xticks(np.arange(0,1,0.1))
    #plt.yticks(np.arange(0,1,0.1))
    #plt.grid()
    #plt.show()
