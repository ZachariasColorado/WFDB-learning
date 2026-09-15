import base64
from io import BytesIO

from flask import Flask, url_for, render_template

from matplotlib.figure import Figure

app = Flask(__name__)
#url_for('static', filename='style.css')



if __name__ == "__main__":
    app.run(debug=True)

@app.route("/")
def draw_graph(fig: Figure):
    # Generate the figure **without using pyplot**.
    #fig = Figure()
    #ax = fig.subplots()
    #ax.plot([1, 2])
    # Save it to a temporary buffer.
    buf = BytesIO()
    fig.savefig(buf, format="png")
    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return render_template("graph_view.html", data=data)