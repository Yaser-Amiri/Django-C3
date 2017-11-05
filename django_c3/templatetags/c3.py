from django import template
from django.utils.safestring import mark_safe
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.conf import settings

register = template.Library()

# read setting file
try:
    import_by_developer = not bool(settings.C3_IMPORT)
except AttributeError:
    import_by_developer = False

###############################################################################


def import_c3():
    """Generates 'script' tags to import C3 files.

        Uses 'static' function and creates urls of C3 static files, then
        uses them in 'script' and 'link' HTML elements.

        Returns:
            A string that contains two script and one linke HTML element.
    """
    # checks setting and returns empty string if user
    #   imports static files himself (no import occurs)
    if import_by_developer:
        return str()

    import_c3_css = '<link type="text/css" rel="stylesheet" href="%s"/>' \
        % static('django_c3/css/c3.min.css')
    import_js_d3 = '<script type="text/javascript" src="%s"></script>' % \
        static('django_c3/js/d3.v3.min.js')
    import_js_c3 = '<script type="text/javascript" src="%s"></script>' % \
        static('django_c3/js/c3.min.js')

    return '%s\n%s\n%s' % (import_c3_css, import_js_d3, import_js_c3)

###############################################################################


@register.simple_tag(takes_context=True)
def step(
        context, bind_to, data, title='', area=False, x_is_category=False,
        labels=False, vertical_grid_line=False, horizontal_grid_line=False,
        show_legend=True, zoom=False, group_tooltip=True, height=None,
        width=None
        ):

    """Generates javascript code to show a 'step' chart.

        Args:
            context: Context of template.
            bind_to: A string that specifics an HTML element (eg: id or class)
                that chart will be shown in that. (like: '#chart')
            data: It is dictinary that contains data of chart, some
                informations about extra lines, grouping of data and
                chart axis labels. eg:
                {
                    'x': ['2017-5-19', '2017-5-20', '2017-5-21', '2017-5-22'],
                    'horizontal_lines': [40],
                    # 'vertical_lines': [40],
                    'data': [
                        {'title': 'A', 'values': [26, 35, 52, 34, 45, 74],
                            'color': '#FF34FF'},
                        # {'title': 'B', 'values': [54, 25, 52, 26, 20, 89]},
                    ],
                    # 'groups': [('A', 'B')]
                }
                vertical_lines works just if x_is_category seted to False.
            title: A string that will be shown on top of the chart.
            area: It's a boolean option. If true, the area under the curve
                will be colored.
            x_is_category: It's a boolean option. If false, labels of X axis
                will be considered as real number and sortable. (they will
                be sorted automatically)
            labels: It's a boolean option. If true, value of record will be
                shown on column.
            vertical_grid_line: It's boolean option, If true some vertical rows
                will be drawn in chart. (grid lines)
            horizontal_grid_line: It's boolean option, If true some horizontal
                rows will be drawn in chart. (grid lines)
            show_legend: It's boolean option, If false, legends of the chart
                will be hidden.
            zoom: It's boolean option, If true, end user can scroll on
                chart to zoom in and zoom out.
            group_tooltip: It's boolean option, If true, data of all records
                in that point whill be shown to gather.
            height: It's an integer option, it will determine heigth of chart
                in pixel.
            width: It's an integer option, it will determine width of chart
                in pixel.

    Returns:
        A string contains chart js code and import code of C3 static files, if
        it did not imported yet.
        You can see structure of chart in chart_structur variable.

    """

    # step chart structure in JS
    chart_structur = (
        '\n<script type="text/javascript">'
        '\n     var chart = c3.generate({'
        '\n         bindto: "%s",'
        '\n         data: {'
        '\n             x: %s,'
        '\n             columns: ['
        '\n                 %s'
        '\n             ],'
        '\n             type : "%s",'
        '\n             colors: {'
        '\n                 %s'
        '\n             },'
        '\n             groups: ['
        '\n                 %s'
        '\n             ],'
        '\n             labels : %s'
        '\n         },'
        '\n         title: { text: "%s"},'
        '\n         axis: { x: { type: "%s" } },'
        '\n         grid: {'
        '\n             x: { show: %s ,lines: [%s] },'
        '\n             y: { show: %s ,lines: [%s] },'
        '\n         },'
        '\n         legend: { show: %s },'
        '\n         zoom: { enabled: %s },'
        '\n         tooltip: { grouped: %s },'
        '\n         size: { height: %s, width: %s }'
        '\n     });'
        '\n</script>'
    )

    # convert parameters to strings to be acceptable in JS and C3 syntax.
    if area:
        _type = 'area-step'
    else:
        _type = 'step'

    if x_is_category:
        x_type = 'category'
    else:
        x_type = ''

    if labels:
        labels = 'true'
    else:
        labels = 'false'

    if vertical_grid_line:
        vertical_grid_line = 'true'
    else:
        vertical_grid_line = 'false'

    if horizontal_grid_line:
        horizontal_grid_line = 'true'
    else:
        horizontal_grid_line = 'false'

    if show_legend:
        show_legend = 'true'
    else:
        show_legend = 'false'

    if zoom:
        zoom = 'true'
    else:
        zoom = 'false'

    if group_tooltip:
        group_tooltip = 'true'
    else:
        group_tooltip = 'false'

    if height is not None:
        height = int(height)
    else:
        height = 'null'

    if width is not None:
        width = int(width)
    else:
        width = 'null'

    # read horizontal line points from data
    horizontal_lines = str()
    if 'horizontal_lines' in data.keys():
        for line in data['horizontal_lines']:
            horizontal_lines = ''.join([horizontal_lines,
                                        '{ value: %s}' % line, ','])

    # read vertical line points from data
    # raise an exception if x_is_category set to true and vertical_lines exists
    vertical_lines = str()
    if 'vertical_lines' in data.keys():
        if x_is_category:
            raise Exception(
                "It's meaningless to use vertical_lines with x_is_category."
                )
        for line in data['vertical_lines']:
            vertical_lines = ''.join(
                                [vertical_lines, '{ value: %s}' % line, ','])

    # reads 'x' field of data and creates X axis labels.
    # a hash is used to naming X axis labels
    x_labels = str()
    if 'x' in data.keys():
        if x_is_category:
            x_labels = data['x']
        else:
            x_labels = list(filter(lambda x: int(x), data['x']))
        x_labels = ','.join([repr(str(label)) for label in x_labels])
        x_labels = '["2d2014226823e74c2accfcce8e0ca141", %s],' % x_labels
        x_label_list_name = '"2d2014226823e74c2accfcce8e0ca141"'
    else:
        x_labels = ''
        x_label_list_name = "null"

    # read records points to draw on chart
    data_title_list = list()
    chart_data = str()
    for item in data['data']:
        values = ','.join([str(v) for v in item['values']])
        item_data = '["%s", %s], ' % (item['title'], values)
        chart_data = ' '.join([chart_data, item_data])
        data_title_list.append(item['title'])
    # add X axis labels to chart data
    chart_data = ''.join([chart_data, x_labels])

    # read colors of data
    chart_color = str()
    for item in data['data']:
        if 'color' in item.keys():
            item_color = '"%s": "%s", ' % (item['title'], item['color'])
            chart_color = ' '.join([chart_color, item_color])

    # read grouping details of data
    total_group_string = str()
    if 'groups' in data.keys():
        for group in data['groups']:
            group_string = str()
            for item in group:
                # raise an exception if mentioned key were not exist in data
                if item not in data_title_list:
                    raise ValueError("%s is not exists in your data!" % item)
                group_string = ''.join([group_string, ',', repr(item)])
            total_group_string = ''.join(
                            [total_group_string, '[', group_string, ']', ','])

    # pass arguments to chart structure
    chart = chart_structur % (
            bind_to, x_label_list_name,
            chart_data, _type, chart_color, total_group_string, labels,
            title, x_type, vertical_grid_line, vertical_lines,
            horizontal_grid_line, horizontal_lines, show_legend, zoom,
            group_tooltip, height, width
        )

    # add import C3 elements to it, if it does not imported yet and return it.
    if not ('import_js_c3' in context and context['import_js_c3']):
        context['import_js_c3'] = True
        return mark_safe('%s\n%s' % (import_c3(), chart))
    else:
        return mark_safe(chart)

###############################################################################


@register.simple_tag(takes_context=True)
def line_xy(
        context, bind_to, data, title='', angle=True, area=False,
        labels=False, vertical_grid_line=False, horizontal_grid_line=False,
        show_legend=True, zoom=False, show_points=True, group_tooltip=True,
        height=None, width=None
        ):

    """Generates javascript code to show a 'bar' chart.

        Args:
            context: Context of template.
            bind_to: A string that specifics an HTML element (eg: id or class)
                that chart will be shown in that. (like: '#chart')
            data: It is dictinary that contains data of chart, some
                informations about extra lines, grouping of data and
                chart axis labels. eg:
                {
                    'horizontal_lines': [5],
                    'vertical_lines': [5],
                    'data': [
                        {'title': 'A', 'values': [
                            (1, 2), (2, 4), (3, 9),
                            (4, 4), (5, 3), (6, 2), (7, 1)]},
                        {'title': 'B', 'values': [
                            (3, 6), (5, 5), (7, 9), (6, 4),
                            (3, 3), (1, 2), (2, 7)],
                            'color': '#CCCCC'},
                    ],
                    # 'groups': [('A', 'B')]
                }
            title: A string that will be shown on top of the chart.
            area: It's a boolean option. If true, the area under the curve
                will be colored.
            angle: It's a boolean option. If false, chart type will be spline.
            labels: It's a boolean option. If true, value of record will be
                shown on column.
            vertical_grid_line: It's boolean option, If true some vertical rows
                will be drawn in chart. (grid lines)
            horizontal_grid_line: It's boolean option, If true some horizontal
                rows will be drawn in chart. (grid lines)
            show_legend: It's boolean option, If false, legends of the chart
                will be hidden.
            zoom: It's boolean option, If true, end user can scroll on
                chart to zoom in and zoom out.
            group_tooltip: It's boolean option, If true, data of all records
                in that point whill be shown to gather.
            show_points: It's boolean option, If false, points of
                record will be hidden.
            height: It's an integer option, It will determine heigth of chart
                in pixel.
            width: It's an integer option, It will determine width of chart
                in pixel

    Returns:
        A string contains chart js code and import code of C3 static files, if
        it did not imported yet.
        You can see structure of chart in chart_structur variable.

    """
    # line (X,Y) chart structure in JS
    chart_structur = (
        '\n<script type="text/javascript">'
        '\n     var chart = c3.generate({'
        '\n         bindto: "%s",'
        '\n         data: {'
        '\n             xs: { %s },'
        '\n             columns: [ %s ],'
        '\n             type : "%s",'
        '\n             colors: { %s },'
        '\n             groups: ['
        '\n                 %s'
        '\n             ],'
        '\n             labels : %s'
        '\n         },'
        '\n         title: { text: "%s"},'
        '\n         grid: {'
        '\n             x: { show: %s ,lines: [%s] },'
        '\n             y: { show: %s ,lines: [%s] },'
        '\n         },'
        '\n         legend: { show: %s },'
        '\n         zoom: { enabled: %s },'
        '\n         point: { show: %s },'
        '\n         tooltip: { grouped: %s },'
        '\n         size: { height: %s, width: %s }'
        '\n     });'
        '\n</script>'
    )

    # convert parameters to strings to be acceptable in JS and C3 syntax.
    if angle and not area:
        _type = 'line'
    elif angle and area:
        _type = 'area'
    elif not angle and not area:
        _type = 'spline'
    elif not angle and area:
        _type = 'area-spline'
    else:
        _type = 'line'

    if labels:
        labels = 'true'
    else:
        labels = 'false'

    if vertical_grid_line:
        vertical_grid_line = 'true'
    else:
        vertical_grid_line = 'false'

    if horizontal_grid_line:
        horizontal_grid_line = 'true'
    else:
        horizontal_grid_line = 'false'

    if show_legend:
        show_legend = 'true'
    else:
        show_legend = 'false'

    if zoom:
        zoom = 'true'
    else:
        zoom = 'false'

    if show_points:
        show_points = 'true'
    else:
        show_points = 'false'

    if group_tooltip:
        group_tooltip = 'true'
    else:
        group_tooltip = 'false'

    if height is not None:
        height = int(height)
    else:
        height = 'null'

    if width is not None:
        width = int(width)
    else:
        width = 'null'

    # read horizontal line points from data
    horizontal_lines = str()
    if 'horizontal_lines' in data.keys():
        for line in data['horizontal_lines']:
            horizontal_lines = ''.join(
                                [horizontal_lines, '{ value: %s}' % line, ','])

    # read vertical line points from data
    vertical_lines = str()
    if 'vertical_lines' in data.keys():
        for line in data['vertical_lines']:
            vertical_lines = ''.join(
                                [vertical_lines, '{ value: %s}' % line, ','])

    # read records points to draw on chart
    xy_mapping = str()
    data_title_list = list()
    chart_data = str()
    for item in data['data']:
        y_values = ','.join([str(v[1]) for v in item['values']])
        item_data = '["%s", %s], ' % (item['title'], y_values)
        chart_data = ' '.join([chart_data, item_data])
        data_title_list.append(item['title'])
        x_values = ','.join([str(v[0]) for v in item['values']])
        item_data = '["%s", %s], ' % (item['title']+'_x', x_values)
        chart_data = ' '.join([chart_data, item_data])
        xy_mapping = ''.join(
                [xy_mapping, '"%s": "%s"' %
                    (item['title'], item['title']+'_x'), ','])

    # read colors of data
    chart_color = str()
    for item in data['data']:
        if 'color' in item.keys():
            item_color = '"%s": "%s", ' % (item['title'], item['color'])
            chart_color = ' '.join([chart_color, item_color])

    # read grouping details of data
    total_group_string = str()
    if 'groups' in data.keys():
        for group in data['groups']:
            group_string = str()
            for item in group:
                # raise an exception if mentioned key were not exist in data
                if item not in data_title_list:
                    raise ValueError("%s is not exists in your data!" % item)
                group_string = ''.join([group_string, ',', repr(item)])
            total_group_string = ''.join(
                            [total_group_string, '[', group_string, ']', ','])

    # pass arguments to chart structure
    chart = chart_structur % (
            bind_to, xy_mapping, chart_data, _type,
            chart_color, total_group_string, labels, title,
            vertical_grid_line, vertical_lines, horizontal_grid_line,
            horizontal_lines, show_legend, zoom, show_points, group_tooltip,
            height, width
            )

    # add import C3 elements to it, if it does not imported yet and return it.
    if not ('import_js_c3' in context and context['import_js_c3']):
        return mark_safe('%s\n%s' % (import_c3(), chart))
    else:
        return mark_safe(chart)

###############################################################################


@register.simple_tag(takes_context=True)
def line(
        context, bind_to, data, title='', angle=True, area=False,
        x_is_category=False, labels=False, vertical_grid_line=False,
        horizontal_grid_line=False, show_legend=True, zoom=False,
        show_points=True, group_tooltip=True, height=None, width=None
        ):

    """Generates javascript code to show a 'bar' chart.

        Args:
            context: Context of template.
            bind_to: A string that specifics an HTML element (eg: id or class)
                that chart will be shown in that. (like: '#chart')
            data: It is dictinary that contains data of chart, some
                informations about extra lines, grouping of data and
                chart axis labels. eg:
                {
                    'x': ['2017-5-19', '2017-5-20', '2017-5-21', '2017-5-22'],
                    'horizontal_lines': [40],
                    # 'vertical_lines': [40],
                    'data': [
                        {'title': 'A', 'values': [26, 5, 52, 74]},
                        {'title': 'B', 'values': [54, 21, 40, 26]},
                        {'title': 'C', 'values': [63, 14, 25, 11]},
                    ],
                    # 'groups': [('B', 'C')]
                }
                vertical_lines works just if x_is_category seted to False.
            title: A string that will be shown on top of the chart.
            area: It's a boolean option. If true, the area under the curve
                will be colored.
            angle: It's a boolean option. If false, chart type will be spline.
            x_is_category: It's a boolean option. If false, labels of X axis
                will be considered as real number and sortable. (they will
                be sorted automatically)
            labels: It's a boolean option. If true, value of record will be
                shown on column.
            vertical_grid_line: It's boolean option, If true some vertical rows
                will be drawn in chart. (grid lines)
            horizontal_grid_line: It's boolean option, If true some horizontal
                rows will be drawn in chart. (grid lines)
            show_legend: It's boolean option, If false, legends of the chart
                will be hidden.
            zoom: It's boolean option, If true, end user can scroll on
                chart to zoom in and zoom out.
            group_tooltip: It's boolean option, If true, data of all records
                in that point whill be shown to gather.
            show_points: It's boolean option, If false, points of
                record will be hidden.
            height: It's an integer option, It will determine heigth of chart
                in pixel.
            width: It's an integer option, It will determine width of chart
                in pixel

    Returns:
        A string contains chart js code and import code of C3 static files, if
        it did not imported yet.
        You can see structure of chart in chart_structur variable.

    """
    # line/spline chart structure in JS
    chart_structur = (
        '\n<script type="text/javascript">'
        '\n     var chart = c3.generate({'
        '\n         bindto: "%s",'
        '\n         data: {'
        '\n             x: %s,'
        '\n             columns: [ %s ],'
        '\n             type : "%s",'
        '\n             colors: { %s },'
        '\n             groups: ['
        '\n                 %s'
        '\n             ],'
        '\n             labels : %s'
        '\n         },'
        '\n         title: { text: "%s"},'
        '\n         axis: { x: { type: "%s" } },'
        '\n         grid: {'
        '\n             x: { show: %s ,lines: [%s] },'
        '\n             y: { show: %s ,lines: [%s] },'
        '\n         },'
        '\n         legend: { show: %s },'
        '\n         zoom: { enabled: %s },'
        '\n         point: { show: %s },'
        '\n         tooltip: { grouped: %s },'
        '\n         size: { height: %s, width: %s }'
        '\n     });'
        '\n</script>'
    )

    # convert parameters to strings to be acceptable in JS and C3 syntax.
    if angle and not area:
        _type = 'line'
    elif angle and area:
        _type = 'area'
    elif not angle and not area:
        _type = 'spline'
    elif not angle and area:
        _type = 'area-spline'
    else:
        _type = 'line'

    if x_is_category:
        x_type = 'category'
    else:
        x_type = ''

    if labels:
        labels = 'true'
    else:
        labels = 'false'

    if vertical_grid_line:
        vertical_grid_line = 'true'
    else:
        vertical_grid_line = 'false'

    if horizontal_grid_line:
        horizontal_grid_line = 'true'
    else:
        horizontal_grid_line = 'false'

    if show_legend:
        show_legend = 'true'
    else:
        show_legend = 'false'

    if zoom:
        zoom = 'true'
    else:
        zoom = 'false'

    if show_points:
        show_points = 'true'
    else:
        show_points = 'false'

    if group_tooltip:
        group_tooltip = 'true'
    else:
        group_tooltip = 'false'

    if height is not None:
        height = int(height)
    else:
        height = 'null'

    if width is not None:
        width = int(width)
    else:
        width = 'null'

    # read horizontal line points from data
    horizontal_lines = str()
    if 'horizontal_lines' in data.keys():
        for line in data['horizontal_lines']:
            horizontal_lines = ''.join(
                                [horizontal_lines, '{ value: %s}' % line, ','])

    # read vertical line points from data
    # raise an exception if x_is_category set to true and vertical_lines exists
    vertical_lines = str()
    if 'vertical_lines' in data.keys():
        if x_is_category:
            raise Exception(
                "It's meaningless to use vertical_lines with x_is_category.")
        for line in data['vertical_lines']:
            vertical_lines = ''.join(
                                [vertical_lines, '{ value: %s}' % line, ','])

    # reads 'x' field of data and creates X axis labels.
    # a hash is used to naming X axis labels
    x_labels = str()
    if 'x' in data.keys():
        if x_is_category:
            x_labels = data['x']
        else:
            x_labels = list(filter(lambda x: int(x), data['x']))

        x_labels = ','.join([repr(str(label)) for label in x_labels])
        x_labels = '["2d2014226823e74c2accfcce8e0ca141", %s],' % x_labels
        x_label_list_name = '"2d2014226823e74c2accfcce8e0ca141"'
    else:
        x_labels = ''
        x_label_list_name = "null"

    # read records points to draw on chart
    data_title_list = list()
    chart_data = str()
    for item in data['data']:
        values = ','.join([str(v) for v in item['values']])
        item_data = '["%s", %s], ' % (item['title'], values)
        chart_data = ' '.join([chart_data, item_data])
        data_title_list.append(item['title'])
    # add X axis labels to chart data
    chart_data = ''.join([chart_data, x_labels])

    # read colors of data
    chart_color = str()
    for item in data['data']:
        if 'color' in item.keys():
            item_color = '"%s": "%s", ' % (item['title'], item['color'])
            chart_color = ' '.join([chart_color, item_color])

    # read grouping details of data
    total_group_string = str()
    if 'groups' in data.keys():
        for group in data['groups']:
            group_string = str()
            for item in group:
                # raise an exception if mentioned key were not exist in data
                if item not in data_title_list:
                    raise ValueError("%s is not exists in your data!" % item)
                group_string = ''.join([group_string, ',', repr(item)])
            total_group_string = ''.join(
                            [total_group_string, '[', group_string, ']', ','])

    # pass arguments to chart structure
    chart = chart_structur % (
            bind_to, x_label_list_name, chart_data, _type,
            chart_color, total_group_string, labels, title, x_type,
            vertical_grid_line, vertical_lines, horizontal_grid_line,
            horizontal_lines, show_legend, zoom, show_points, group_tooltip,
            height, width
            )

    # add import C3 elements to it, if it does not imported yet and return it.
    if not ('import_js_c3' in context and context['import_js_c3']):
        return mark_safe('%s\n%s' % (import_c3(), chart))
    else:
        return mark_safe(chart)

##############################################################################


@register.simple_tag(takes_context=True)
def bar(
        context, bind_to, data, title='', x_is_category=False, labels=False,
        vertical_grid_line=False, horizontal_grid_line=False, show_legend=True,
        zoom=False, group_tooltip=True, column_width=None, height=None,
        width=None
        ):

    """Generates javascript code to show a 'bar' chart.

    Args:
        context: Context of template.
        bind_to: A string that specifics an HTML element (eg: id or class)
            that chart will be shown in that. (like: '#chart')
        data: It is dictinary that contains data of chart, some
            informations about extra lines, grouping of data and
            chart axis labels. eg:
            {
                'x': ['2017-5-19', '2017-5-20', '2017-5-21', '2017-5-22'],
                'horizontal_lines': [40],
                # 'vertical_lines': [40],
                'data': [
                    {'title': 'A', 'values': [26, 5, 52, 74]},
                    {'title': 'B', 'values': [54, 21, 40, 26]},
                    {'title': 'C', 'values': [63, 14, 25, 11],
                        'color': '#FF34FF'},
                ],
                # 'groups': [('B', 'C')]
            }
            vertical_lines works just if x_is_category seted to False.
        title: A string that will be shown on top of the chart.
        column_width: It's an integer option. It will determine width of chart
            columns in pixel.
        x_is_category: It's a boolean option. If false, labels of X axis
            will be considered as real number and sortable. (they will
            be sorted automatically)
        labels: It's a boolean option. If true, value of record will be
            shown on column.
        vertical_grid_line: It's boolean option, If true some vertical rows
            will be drawn in chart. (grid lines)
        horizontal_grid_line: It's boolean option, If true some horizontal
            rows will be drawn in chart. (grid lines)
        show_legend: It's boolean option, If false, legends of the chart
            will be hidden.
        zoom: It's boolean option, If true, end user can scroll on
            chart to zoom in and zoom out.
        group_tooltip: It's boolean option, If true, data of all records
            in that point whill be shown to gather.
        height: It's an integer option, It will determine heigth of chart
            in pixel.
        width: It's an integer option, It will determine width of chart
            in pixel.

    Returns:
        A string contains chart js code and import code of C3 static files, if
        it did not imported yet.
        You can see structure of chart in chart_structur variable.

    """
    # bar chart structure in JS
    chart_structur = (
        '\n<script type="text/javascript">'
        '\n     var chart = c3.generate({'
        '\n         bindto: "%s",'
        '\n         data: {'
        '\n             x: %s,'
        '\n             columns: ['
        '\n                 %s'
        '\n             ],'
        '\n             type : "bar",'
        '\n             colors: { %s },'
        '\n             groups: ['
        '\n                 %s'
        '\n             ],'
        '\n             labels : %s'
        '\n         },'
        '\n         title: { text: "%s"},'
        '\n         axis: { x: { type: "%s" } },'
        '\n         bar: { width: %s },'
        '\n         grid: {'
        '\n             x: { show: %s ,lines: [%s] },'
        '\n             y: { show: %s ,lines: [%s] },'
        '\n         },'
        '\n         legend: { show: %s },'
        '\n         zoom: { enabled: %s },'
        '\n         tooltip: { grouped: %s },'
        '\n         size: { height: %s, width: %s }'
        '\n     });'
        '\n</script>'
    )

    # reads 'x' field of data and creates X axis labels.
    # a hash is used to naming X axis labels
    x_labels = str()
    if 'x' in data.keys():
        if x_is_category:
            x_labels = data['x']
        else:
            x_labels = list(filter(lambda x: int(x), data['x']))

        x_labels = ','.join([repr(str(label)) for label in x_labels])
        x_labels = '["2d2014226823e74c2accfcce8e0ca141", %s],' % x_labels
        x_label_list_name = '"2d2014226823e74c2accfcce8e0ca141"'
    else:
        x_labels = ''
        x_label_list_name = "null"

    # convert parameters to strings to be acceptable in JS and C3 syntax.
    if x_is_category:
        x_type = 'category'
    else:
        x_type = ''

    if labels:
        labels = 'true'
    else:
        labels = 'false'

    if vertical_grid_line:
        vertical_grid_line = 'true'
    else:
        vertical_grid_line = 'false'

    if horizontal_grid_line:
        horizontal_grid_line = 'true'
    else:
        horizontal_grid_line = 'false'

    if show_legend:
        show_legend = 'true'
    else:
        show_legend = 'false'

    if zoom:
        zoom = 'true'
    else:
        zoom = 'false'

    if group_tooltip:
        group_tooltip = 'true'
    else:
        group_tooltip = 'false'

    if height is not None:
        height = int(height)
    else:
        height = 'null'

    if width is not None:
        width = int(width)
    else:
        width = 'null'

    if column_width is not None:
        column_width = int(column_width)
    else:
        column_width = 'null'

    # read records points to draw on chart
    data_title_list = list()
    chart_data = str()
    for item in data['data']:
        values = ','.join([str(v) for v in item['values']])
        item_data = '["%s", %s], ' % (item['title'], values)
        chart_data = ' '.join([chart_data, item_data])
        data_title_list.append(item['title'])
    # add X axis labels to chart data
    chart_data = ''.join([chart_data, x_labels])

    # read colors of data
    chart_color = str()
    for item in data['data']:
        if 'color' in item.keys():
            item_color = '"%s": "%s", ' % (item['title'], item['color'])
            chart_color = ' '.join([chart_color, item_color])

    # read horizontal line points from data
    horizontal_lines = str()
    if 'horizontal_lines' in data.keys():
        for line in data['horizontal_lines']:
            horizontal_lines = ''.join(
                                [horizontal_lines, '{ value: %s}' % line, ','])

    # read vertical line points from data
    # raise an exception if x_is_category set to true and vertical_lines exists
    vertical_lines = str()
    if 'vertical_lines' in data.keys():
        if x_is_category:
            raise Exception(
                "It's meaningless to use vertical_lines with x_is_category.")
        for line in data['vertical_lines']:
            vertical_lines = ''.join(
                                [vertical_lines, '{ value: %s}' % line, ','])

    # read grouping details of data
    total_group_string = str()
    if 'groups' in data.keys():
        for group in data['groups']:
            group_string = str()
            for item in group:
                # raise an exception if mentioned key were not exist in data
                if item not in data_title_list:
                    raise ValueError("%s is not exists in your data!" % item)
                group_string = ''.join([group_string, ',', repr(item)])
            total_group_string = ''.join(
                            [total_group_string, '[', group_string, ']', ','])

    # pass arguments to chart structure
    chart = chart_structur % (
        bind_to, x_label_list_name, chart_data, chart_color,
        total_group_string, labels, title, x_type, column_width,
        vertical_grid_line, vertical_lines, horizontal_grid_line,
        horizontal_lines, show_legend, zoom, group_tooltip, height, width
        )

    # add import C3 elements to it, if it does not imported yet and return it.
    if not ('import_js_c3' in context and context['import_js_c3']):
        context['import_js_c3'] = True
        return mark_safe('%s\n%s' % (import_c3(), chart))
    else:
        return mark_safe(chart)

###############################################################################


@register.simple_tag(takes_context=True)
def pie(
        context, bind_to, data, title='', show_legend=True, height=None,
        width=None
        ):

    """Generates javascript code to show a 'pie' chart.

    Args:
        context: Context of template.
        bind_to: A string that specifics an HTML element (eg: id or class)
            that chart will be shown in that. (like: '#chart')
        data: It is dictinary that contains data of chart. Eg:
            [
                {'title': 'A', 'value': 6},
                {'title': 'B', 'value': 10},
                {'title': 'C', 'value': 84},
            ]
        title: A string that will be shown on top of the chart.
        show_legend: It's boolean option, If false, legends of the chart
            will be hidden.
        height: It's an integer option, It will determine heigth of chart
            in pixel.
        width: It's an integer option, It will determine width of chart
            in pixel.

    Returns:
        A string contains chart js code and import code of C3 static files, if
        it did not imported yet.
        You can see structure of chart in chart_structur variable.
    """

    # pie chart structure in JS
    chart_structur = (
        '\n<script type="text/javascript">'
        '\n     var chart = c3.generate({'
        '\n         bindto: "%s",'
        '\n         data: {'
        '\n             columns: [ %s ],'
        '\n             type : "pie",'
        '\n             colors: { %s }'
        '\n         },'
        '\n         title: { text: "%s"},'
        '\n         legend: { show: %s },'
        '\n         size: { height: %s, width: %s }'
        '\n     });'
        '\n</script>'
    )

    # convert parameters to strings to be acceptable in JS and C3 syntax.
    if show_legend:
        show_legend = 'true'
    else:
        show_legend = 'false'

    if height is not None:
        height = int(height)
    else:
        height = 'null'

    if width is not None:
        width = int(width)
    else:
        width = 'null'

    # read records points to draw on chart
    chart_data = str()
    for item in data:
        item_data = '["%s", %s], ' % (item['title'], item['value'])
        chart_data = ' '.join([chart_data, item_data])

    # read colors of data
    chart_color = str()
    for item in data:
        if 'color' in item.keys():
            item_color = '"%s": "%s", ' % (item['title'], item['color'])
            chart_color = ' '.join([chart_color, item_color])

    # pass arguments to chart structure
    chart = chart_structur % (
            bind_to, chart_data, chart_color, title,
            show_legend, height, width
            )

    # add import C3 elements to it, if it does not imported yet and return it.
    if not ('import_js_c3' in context and context['import_js_c3']):
        context['import_js_c3'] = True
        return mark_safe('%s\n%s' % (import_c3(), chart))
    else:
        return mark_safe(chart)

###############################################################################


@register.simple_tag(takes_context=True)
def donut(
        context, bind_to, data, inner_title='', outer_title='',
        show_legend=True, height=None, width=None
        ):

    """Generates javascript code to show a 'donut' chart.

    Args:
        context: Context of template.
        bind_to: A string that specifics an HTML element (eg: id or class)
            that chart will be shown in that. (like: '#chart')
        data: It is dictinary that contains data of chart. Eg:
            [
                {'title': 'A', 'value': 6},
                {'title': 'B', 'value': 10},
                {'title': 'C', 'value': 84},
            ]
        inner_title: A string that will be shown in the chart.
        outer_title: A string that will be shown on top of the chart.
        show_legend: It's boolean option, If false, legends of the chart
            will be hidden.
        height: It's an integer option, It will determine heigth of chart
            in pixel.
        width: It's an integer option, It will determine width of chart
            in pixel.

    Returns:
        A string contains chart js code and import code of C3 static files, if
        it did not imported yet.
        You can see structure of chart in chart_structur variable.

    """
    # donut chart structure in JS
    chart_structur = (
        '\n<script type="text/javascript">'
        '\n     var chart = c3.generate({'
        '\n         bindto: "%s",'
        '\n         data: {'
        '\n             columns: [ %s ],'
        '\n             type : "donut",'
        '\n             colors: { %s }'
        '\n         },'
        '\n         title: { text: "%s"},'
        '\n         donut: { title: "%s"},'
        '\n         legend: { show: %s },'
        '\n         size: { height: %s, width: %s }'
        '\n     });'
        '\n</script>'
    )

    # convert parameters to strings to be acceptable in JS and C3 syntax.
    if height is not None:
        height = int(height)
    else:
        height = 'null'

    if width is not None:
        width = int(width)
    else:
        width = 'null'

    if show_legend:
        show_legend = 'true'
    else:
        show_legend = 'false'

    # read records points to draw on chart
    chart_data = str()
    for item in data:
        item_data = '["%s", %s], ' % (item['title'], item['value'])
        chart_data = ' '.join([chart_data, item_data])

    # read colors of data
    chart_color = str()
    for item in data:
        if 'color' in item.keys():
            item_color = '"%s": "%s", ' % (item['title'], item['color'])
            chart_color = ' '.join([chart_color, item_color])

    # pass arguments to chart structure
    chart = chart_structur % (
                bind_to, chart_data, chart_color, outer_title, inner_title,
                show_legend, height, width
                )

    # add import C3 elements to it, if it does not imported yet and return it.
    if not ('import_js_c3' in context and context['import_js_c3']):
        context['import_js_c3'] = True
        return mark_safe('%s\n%s' % (import_c3(), chart))
    else:
        return mark_safe(chart)
