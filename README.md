# svgchart
Simple Python SVG (as HTML embedded, not SVG file) chart creator with no external dependencies

Currently just 1 function intended to be called directly, linechart:

def linechart(dataset, h=default_height, w=default_width, linew=default_linewidth, borderw=default_border_width, bordercolor=default_border_color, background=default_background, yvals=default_yvals, xvals=default_xvals, ylabel=default_ylabel, xlabel=default_xlabel, textcolor=default_textcolor, graphtitle=default_graphtitle, textsize=default_textsize, tickinterval=default_tickinterval)

The only required argument is dataset, which is a dict containing the data series to be plotted formatted as such:

{'seriesname1': [(xval1, yval1), (xval2, yval2), ...], 'seriesname2': ...}

All other arguments control the look/feel of the chart.  You get back the HTML-ized SVG that can then be included inline in other HTML.

h: Height of the image, in pixels. Default 250

w: Width of the image, in pixels. Default 600

linew: Width of graph lines, in pixels. Default 1

borderw: Width of border lines, in pixels. default 1

bordercolor: Color of border lines, HTML color code/name. Default 'black'

background: Background color, HTML color code/name. Default 'white'

yvals: Set to True to enable Y axis value tick marks, default True

xvals: Set to True to enable X axis value tick marks, default True

ylabel: String label for Y axis, set to '' (default) to disable

xlabel: String label for X axis, set to '' (default) to disable

textcolor: Text color, HTML color code/name, default 'black'

graphtitle: String to show at the top of the graph, set to '' (default) to disable

textsize: Font size (pt), default 12

ts_mode: Interpret X axis values as a time series expressed in epoch seconds, X axis values will be displayed as HH:MM

gridline_enable: Adds light gray dashed gridlines to the chart

Notes and Caveats:

- Only positive data works correctly - no negative numbers for X or Y values, I mainly wrote this for some data where negatives do not exist
- Data points must be ordered along the X value
- Text scaling is basically nonexistent beyond the textsize parameter, nothing adjusts around the font size of the text.  Choosing a large text size may have unpleasant results < -- SOMEWHAT better now, have rudimentary auto-scaling with text size and positioning (mostly) works for sane values.
