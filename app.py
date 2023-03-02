from flask import Flask, render_template, url_for, request, redirect, Response
import Distillation as d
import pandas as pd
import io
import numpy as np
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure


app = Flask(__name__)



#dist.get_diagrams()

df = pd.read_csv('static/tables/antconst.csv')
names_antoine = list(df['Name'])



@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            species_1 = request.form.get('species1')
            species_2 = request.form.get('species2')
            q_val = float(request.form.get('q_val'))
            feed = float(request.form.get('feed'))
            dist = float(request.form.get('dist'))
            bott = float(request.form.get('bott'))
            reflux = float(request.form.get('reflux'))

            
            global species_light, rect_x_values ,rect_y_values, eqlm_x_values, eqlm_y_values, strip_x_values, strip_y_values, fortyfive_x_values, fortyfive_y_values, q_x_values, q_y_values
            species_light, rect_x_values ,rect_y_values, eqlm_x_values, eqlm_y_values, strip_x_values, strip_y_values, fortyfive_x_values, fortyfive_y_values, q_x_values, q_y_values = d.get_diagrams(species_1, species_2, q_val, feed, dist, bott, reflux)


            return redirect('/plot.png')
        except:
            return redirect('/')
    else:
        return render_template('index.html',names=names_antoine)

@app.route('/plot.png')
def plot_png():
    fig = create_figure()
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

def create_figure():
    try:
        fig = Figure()
        axis = fig.add_subplot(1, 1, 1)
        axis.plot(fortyfive_x_values,fortyfive_y_values)
        axis.plot(eqlm_x_values, eqlm_y_values)
        axis.plot(q_x_values,q_y_values)
        axis.plot(rect_x_values,rect_y_values)
        axis.plot(strip_x_values,strip_y_values)
        axis.set_title('xy '+ str(species_light))
        axis.set_xlabel('x fraction')
        axis.set_ylabel('y fraction')
        axis.set_xticks(np.arange(0,1.1,0.1))
        axis.set_yticks(np.arange(0,1.1,0.1))
        axis.set_xlim(0,1)
        axis.set_ylim(0,1)
        axis.grid()
        return fig
    except:
        return render_template('index.html', names=names_antoine)

if __name__ == "__main__":
    app.run()