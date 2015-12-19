# svgchart
Simple Python SVG (as HTML embedded, not SVG file) chart creator with no external dependencies

Currently just 1 function intended to be called directly, linechart:

def linechart(dataset, h=default_height, w=default_width, linew=default_linewidth, borderw=default_border_width, bordercolor=default_border_color, background=default_background, yvals=default_yvals, xvals=default_xvals, ylabel=default_ylabel, xlabel=default_xlabel, textcolor=default_textcolor, graphtitle=default_graphtitle, textsize=default_textsize, tickinterval=default_tickinterval)

The only required argument is dataset, which is a dict containing the data series to be plotted formatted as such:

{'seriesname1': [(xval1, yval1), (xval2, yval2), ...], 'seriesname2': ...}

All other arguments control the look/feel of the chart.  You get back the HTML-ized SVG that can then be included inline in other HTML.

Notes and Caveats:

- Only positive data works correctly - no negative numbers for X or Y values, I mainly wrote this for some data where negatives do not exist
- Data points must be ordered along the X value
- Text scaling is basically nonexistent beyond the textsize parameter, nothing adjusts around the font size of the text.  Choosing a large text size may have unpleasant results
- No legend yet
