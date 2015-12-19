# Default values

default_height = 250
default_width = 600
default_linewidth = 1
default_border_width = 1
default_border_color = 'black'
default_background = 'white'
default_yvals = True
default_xvals = True
default_ylabel = ''
default_xlabel = ''
default_textcolor = 'black'
default_graphtitle = ''
default_textsize = 12
default_tickinterval = 100

# SVG string patterns

svg_start_tag = '<svg height="{}" width="{}" viewbox="{} {} {} {}" {}>'
svg_end_tag = '</svg>'
svg_style_block = 'style="background:{};border:{}px solid {}"'
svg_line_tag = '<line x1="{}" y1="{}" x2="{}" y2="{}" stroke="{}" stroke-width="{}" />'
svg_text_tag = '<text x="{}" y="{}" font-family="Verdana", font-size="{}" fill="{}">{}</text>'
svg_vert_text_tag = '<text x="{}" y="{}" font-family="Verdana", font-size="{}" fill="{}" transform="rotate({} {}, {})">{}</text>'

# Linechart takes a dict arranged as {'seriesname1': [(xval1, yval1), (xval2, yval2), ...], 'seriesname2': ...} and returns HTML SVG code for a line chart.  Several display options available, those should be self explanatory 

def linechart(dataset, h=default_height, w=default_width, linew=default_linewidth, borderw=default_border_width, bordercolor=default_border_color, background=default_background, yvals=default_yvals, xvals=default_xvals, ylabel=default_ylabel, xlabel=default_xlabel, textcolor=default_textcolor, graphtitle=default_graphtitle, textsize=default_textsize, tickinterval=default_tickinterval):
  linecolors=['#FF0000', '#00FF00', '#0000FF', '#000000', '#880000', '#FF00FF', '#008888', '#001188']
  colorcycle = list(linecolors)
  output = svg_start_tag.format(h, w, '0', '0', w, h, svg_style_block.format(background, borderw, bordercolor))
  x_left_offset = 0
  y_bottom_offset = 0
  y_top_offset = 0
  x_right_offset = 0
  if xvals:
    y_bottom_offset += 40
  if yvals:
    x_left_offset += 40
    x_right_offset += 20
  if xlabel != '':
    y_bottom_offset += 20
  if ylabel != '':
    x_left_offset += 20
  if graphtitle != '':
    y_top_offset += 30
  chartw = w - x_left_offset - x_right_offset
  charth = h - y_top_offset - y_bottom_offset
  scaleddata = scaler(dataset, h=charth, w=chartw, target_interval=tickinterval)
  for series in sorted(scaleddata['series'].keys()):
    if len(colorcycle) == 0:
      colorcycle = list(linecolors)
    output += '<polyline fill="none" stroke="{}" stroke-width="{}" points="'.format(colorcycle.pop(0), linew)
    for p in scaleddata['series'][series]:
      output += '{},{} '.format(p[0] + x_left_offset, p[1] + y_top_offset)
    output += '" />'
  output += '<polyline fill="none" stroke="{}" stroke-width="{}" points="'.format(bordercolor, borderw)
  chartborderpoints = '{}, {} {}, {} {}, {} {}, {} {}, {}'.format(x_left_offset, y_top_offset, x_left_offset, h - y_bottom_offset, w - x_right_offset, h - y_bottom_offset, w - x_right_offset, y_top_offset, x_left_offset, y_top_offset)
  output += chartborderpoints
  output += '" />'
  if yvals:
    for yv in scaleddata['yaxis']:
#      print(str(yv))
      output += svg_line_tag.format(x_left_offset, h - y_bottom_offset - yv[1], x_left_offset - 10, h - y_bottom_offset - yv[1], bordercolor, borderw)
      output += svg_text_tag.format(x_left_offset - 35, h - y_bottom_offset - yv[1] + 5, textsize, textcolor, yv[0])
  if xvals:
    for xv in scaleddata['xaxis']:
#      print(str(xv))
      output += svg_line_tag.format(x_left_offset + xv[1], h - y_bottom_offset, x_left_offset + xv[1], h - y_bottom_offset + 10, bordercolor, borderw)
      output += svg_text_tag.format(x_left_offset - 3 + xv[1] - (len(str(xv[0])) - 1) * 5, h - y_bottom_offset + 30, textsize, textcolor, xv[0])
  if xlabel != '':
    output += svg_text_tag.format(x_left_offset + chartw / 2 - len(xlabel) / 2 * 5, h - 10, textsize, textcolor, xlabel)
  if ylabel != '':
    output += svg_vert_text_tag.format(15, charth / 2 + len(ylabel) / 2 * 5, textsize, textcolor, 270, 15, charth / 2 + len(ylabel) / 2 * 5, ylabel) 
  if graphtitle != '':
    output += svg_text_tag.format(w / 2 - len(graphtitle) / 2 * 5, 15, textsize + 2, textcolor, graphtitle)
  output += svg_end_tag
  return output

# Scaler transforms the dataset into the positional coordinate range of the chart area.  It also calls axisval to generate the x and y axis tick values and positional scaling.  This is a little messy as we're just passing the axis tick target_interval through like some sort of jerk.  This probably means I have chosen poorly in how I arranged these functions and I should probably revisit the workflow.

def scaler(dataset, h=default_height, w=default_width, x_left_offset=0, x_right_offset=0, y_top_offset=0, y_bottom_offset=0, target_interval=default_tickinterval):
  output = {'series':{}}
  true_xmin = None
  true_ymin = None
  true_xmax = None
  true_ymax = None
  for series in dataset:
    xmin = min([p[0] for p in dataset[series]])
    ymin = min([p[1] for p in dataset[series]])
    xmax = max([p[0] for p in dataset[series]])
    ymax = max([p[1] for p in dataset[series]])
    if true_xmin is None:
      true_xmin = xmin
    elif xmin < true_xmin:
      true_xmin = xmin
    if true_xmax is None:
      true_xmax = xmax
    elif xmax > true_xmax:
      true_xmax = xmax
    if true_ymin is None:
      true_ymin = ymin
    elif ymin < true_ymin:
      true_ymin = ymin
    if true_ymax is None:
      true_ymax = ymax
    elif ymax > true_ymax:
      true_ymax = ymax
  output['xmin'] = true_xmin
  output['xmax'] = true_xmax
  output['ymin'] = true_ymin
  output['ymax'] = true_ymax
  xscale = float(w) / float((true_xmax - true_xmin))
  yscale = float(h) / float((true_ymax - true_ymin))
  av = axisvals(true_ymin, true_ymax, true_xmin, true_xmax, h=h, w=w, target_interval=target_interval)
  output['xaxis'] = av['x']
  output['yaxis'] = av['y']
  for series in dataset:
    scaled_points = []
    firstx = None
    firsty = None
    for p in dataset[series]:
      newx = int((float(p[0] - true_xmin) * xscale))
      newy = h - int((float(p[1] - true_ymin) * yscale))
      if firstx == None:
        firstx = newx
      if firsty == None:
        firsty = newy
      scaled_points.append((newx, newy))
    scaled_points.append((w, h))
    scaled_points.append((0, h))
    scaled_points.append((firstx, firsty))
    output['series'][series] = scaled_points
  return output

# Axisvals generates the value and positions of the x and y axis tickmarks

def axisvals(ymin, ymax, xmin, xmax, h=default_height, w=default_width, target_interval=default_tickinterval):
  x_seg_count = w / target_interval
  y_seg_count = h / target_interval
#  print('{} {} {} {} {} {} {} {}'.format(ymin, ymax, xmin, xmax, h, w, x_seg_count, y_seg_count))
  xval_interval = float(xmax - xmin) / float(x_seg_count)
  yval_interval = float(ymax - ymin) / float(y_seg_count)
  xpos_interval = float(w) / float(x_seg_count)
  ypos_interval = float(h) / float(y_seg_count)
  output = {'x':[], 'y':[]}
  for i in range(1, x_seg_count + 1):
    output['x'].append((int(i * xval_interval), int(i * xpos_interval)))
  for i in range(1, y_seg_count + 1):
    output['y'].append((int(i * yval_interval), int(i * ypos_interval)))
  return output
  

























    


