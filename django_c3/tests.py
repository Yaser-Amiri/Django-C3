from django.test import SimpleTestCase
from django.template import Context, Template

###############################################################################


class DonutChartTest(SimpleTestCase):

    def setUp(self):
        self.chart_data = [
            {'title': 'A', 'value': 6},
            {'title': 'B', 'value': 10, 'color': 'red'},
            {'title': 'C', 'value': 84},
        ]
        self.context = Context({'pie_chart': self.chart_data})
        self.tag_arguments = {
            'bind_element': '#chart',
            'inner_title': 'my_inner_title',
            'outer_title': 'my_outer_title',
            'show_legend': False,
            'height': 130,
            'width': 120
        }
        self.template = (
            '{%% load c3 %%}'
            '{%% donut "%(bind_element)s" pie_chart '
            'inner_title="%(inner_title)s" outer_title="%(outer_title)s" '
            'show_legend=%(show_legend)s height=%(height)s '
            'width=%(width)s %%}'
        )

    def test_bind_element(self):
        self.template_to_render = Template(self.template % self.tag_arguments)
        rendered_template = self.template_to_render.render(self.context)
        bind_to_rgx = r'bindto:\s+"%s"' % self.tag_arguments['bind_element']
        self.assertRegex(rendered_template, bind_to_rgx)

    def test_colors(self):
        self.template_to_render = Template(self.template % self.tag_arguments)
        rendered_template = self.template_to_render.render(self.context)
        rgx = r'colors: {.*"B"\:.*"red"'
        self.assertRegex(rendered_template, rgx)

    def test_data(self):
        self.template_to_render = Template(self.template % self.tag_arguments)
        rendered_template = self.template_to_render.render(self.context)
        self.assertRegex(rendered_template, r'columns\:\s+\[.*\[\"A\",\s+6\]')
        self.assertRegex(rendered_template, r'columns\:\s+\[.*\[\"B\",\s+10\]')
        self.assertRegex(rendered_template, r'columns\:\s+\[.*\[\"C\",\s+84\]')

    def test_chart_inner_title(self):
        self.tag_arguments['inner_title'] = 'mytitle'
        self.template_to_render = Template(self.template % self.tag_arguments)
        rendered_template = self.template_to_render.render(self.context)
        rgx = r'donut: { title: "%s"}' % 'mytitle'
        self.assertRegex(rendered_template, rgx)

    def test_chart_outer_title(self):
        self.tag_arguments['outer_title'] = 'mytitle'
        self.template_to_render = Template(self.template % self.tag_arguments)
        rendered_template = self.template_to_render.render(self.context)
        rgx = r'title: { text: "%s"}' % 'mytitle'
        self.assertRegex(rendered_template, rgx)

    def test_chart_legend_true(self):
        self.tag_arguments['show_legend'] = True
        self.template_to_render = Template(self.template % self.tag_arguments)
        rendered_template = self.template_to_render.render(self.context)
        rgx = r'legend: { show: true }'
        self.assertRegex(rendered_template, rgx)

    def test_chart_legend_false(self):
        self.tag_arguments['show_legend'] = False
        self.template_to_render = Template(self.template % self.tag_arguments)
        rendered_template = self.template_to_render.render(self.context)
        rgx = r'legend: { show: false }'
        self.assertRegex(rendered_template, rgx)

    def test_chart_height(self):
        self.tag_arguments['height'] = 500
        self.template_to_render = Template(self.template % self.tag_arguments)
        rendered_template = self.template_to_render.render(self.context)
        rgx = r'size: { height: %s' % self.tag_arguments['height']
        self.assertRegex(rendered_template, rgx)

    def test_chart_width(self):
        self.tag_arguments['width'] = 402
        self.template_to_render = Template(self.template % self.tag_arguments)
        rendered_template = self.template_to_render.render(self.context)
        rgx = r'size: { height: 130, width: %s }' % self.tag_arguments['width']
        self.assertRegex(rendered_template, rgx)

###############################################################################


class PieChartTest(SimpleTestCase):

    def setUp(self):
        self.pie_chart_data = [
                {'title': 'A', 'value': 6},
                {'title': 'B', 'value': 10, 'color': 'red'},
                {'title': 'C', 'value': 84},
            ]
        self.context = Context({'pie_chart': self.pie_chart_data})
        self.tag_arguments = {
            'bind_element': '#chart',
            'title': 'pie-lchart',
            'show_legend': False,
            'height': 130,
            'width': 120
        }

        self.template = (
                '{%% load c3 %%}'
                '{%% pie "%(bind_element)s" pie_chart title="%(title)s" '
                'show_legend=%(show_legend)s height=%(height)s '
                'width=%(width)s %%}'
                )

    def test_bind_element(self):
        self.template_to_render = Template(self.template % self.tag_arguments)
        rendered_template = self.template_to_render.render(self.context)
        bind_to_rgx = r'bindto:\s+"%s"' % self.tag_arguments['bind_element']
        self.assertRegex(rendered_template, bind_to_rgx)

    def test_colors(self):
        self.template_to_render = Template(self.template % self.tag_arguments)
        rendered_template = self.template_to_render.render(self.context)
        rgx = r'colors: {.*"B"\:.*"red"'
        self.assertRegex(rendered_template, rgx)

    def test_data(self):
        self.template_to_render = Template(self.template % self.tag_arguments)
        rendered_template = self.template_to_render.render(self.context)
        self.assertRegex(rendered_template, r'columns\:\s+\[.*\[\"A\",\s+6\]')
        self.assertRegex(rendered_template, r'columns\:\s+\[.*\[\"B\",\s+10\]')
        self.assertRegex(rendered_template, r'columns\:\s+\[.*\[\"C\",\s+84\]')

    def test_chart_title(self):
        self.tag_arguments['title'] = 'mytitle'
        self.template_to_render = Template(self.template % self.tag_arguments)
        rendered_template = self.template_to_render.render(self.context)
        rgx = r'title: { text: "%s"}' % 'mytitle'
        self.assertRegex(rendered_template, rgx)

    def test_chart_legend_true(self):
        self.tag_arguments['show_legend'] = True
        self.template_to_render = Template(self.template % self.tag_arguments)
        rendered_template = self.template_to_render.render(self.context)
        rgx = r'legend: { show: true }'
        self.assertRegex(rendered_template, rgx)

    def test_chart_legend_false(self):
        self.tag_arguments['show_legend'] = False
        self.template_to_render = Template(self.template % self.tag_arguments)
        rendered_template = self.template_to_render.render(self.context)
        rgx = r'legend: { show: false }'
        self.assertRegex(rendered_template, rgx)

    def test_chart_height(self):
        self.tag_arguments['height'] = 500
        self.template_to_render = Template(self.template % self.tag_arguments)
        rendered_template = self.template_to_render.render(self.context)
        rgx = r'size: { height: %s' % self.tag_arguments['height']
        self.assertRegex(rendered_template, rgx)

    def test_chart_width(self):
        self.tag_arguments['width'] = 402
        self.template_to_render = Template(self.template % self.tag_arguments)
        rendered_template = self.template_to_render.render(self.context)
        rgx = r'size: { height: 130, width: %s }' % self.tag_arguments['width']
        self.assertRegex(rendered_template, rgx)

###############################################################################


class StepChartTest(SimpleTestCase):

    def setUp(self):
        self.step_chart_data = {
            'x': ['2017-5-19', '2017-5-20', '2017-5-21', '2017-5-22'],
            'horizontal_lines': [40],
            # 'vertical_lines': [40],
            'data': [
                {'title': 'A', 'values': [26, 35, 52, 34, 45, 74],
                    'color': '#FF34FF'},
            ],
            # 'groups': [('A',)]
        }

        self.context = Context({'step_chart': self.step_chart_data})
        self.tag_arguments = {
            'bind_element': '#chart',
            'title': 'step-chart',
            'area': False,
            'x_is_category': True,
            'labels': False,
            'vertical_grid_line': False,
            'horizontal_grid_line': False,
            'zoom': False,
            'show_legend': False,
            'group_tooltip': True,
            'height': 130,
            'width': 120
        }

        self.template = (
                '{%% load c3 %%}'
                '{%% step "%(bind_element)s" step_chart title="%(title)s" '
                'area=%(area)s x_is_category=%(x_is_category)s '
                'labels=%(labels)s vertical_grid_line=%(vertical_grid_line)s '
                'horizontal_grid_line=%(horizontal_grid_line)s '
                'show_legend=%(show_legend)s zoom=%(zoom)s '
                'group_tooltip=%(group_tooltip)s '
                'height=%(height)s width=%(width)s %%}'
                )

    def test_bind_element(self):
        self.template_to_render = Template(self.template % self.tag_arguments)
        rendered_template = self.template_to_render.render(self.context)
        bind_to_rgx = r'bindto:\s+"%s"' % self.tag_arguments['bind_element']
        self.assertRegex(rendered_template, bind_to_rgx)

    def test_chart_title(self):
        self.tag_arguments['title'] = 'mytitle'
        self.template_to_render = Template(self.template % self.tag_arguments)
        rendered_template = self.template_to_render.render(self.context)
        rgx = r'title: { text: "%s"}' % 'mytitle'
        self.assertRegex(rendered_template, rgx)

    def test_chart_area_true(self):
        self.tag_arguments['area'] = True
        self.template_to_render = Template(self.template % self.tag_arguments)
        rendered_template = self.template_to_render.render(self.context)
        rgx = r'type : "area-step"'
        self.assertRegex(rendered_template, rgx)

    def test_chart_area_false(self):
        self.tag_arguments['area'] = False
        self.template_to_render = Template(self.template % self.tag_arguments)
        rendered_template = self.template_to_render.render(self.context)
        rgx = r'type : "step"'
        self.assertRegex(rendered_template, rgx)

    def test_chart_labels_true(self):
        self.tag_arguments['labels'] = True
        self.template_to_render = Template(self.template % self.tag_arguments)
        rendered_template = self.template_to_render.render(self.context)
        rgx = r'labels : true'
        self.assertRegex(rendered_template, rgx)

    def test_chart_labels_false(self):
        self.tag_arguments['labels'] = False
        self.template_to_render = Template(self.template % self.tag_arguments)
        rendered_template = self.template_to_render.render(self.context)
        rgx = r'labels : false'
        self.assertRegex(rendered_template, rgx)

    def test_chart_legend_true(self):
        self.tag_arguments['show_legend'] = True
        self.template_to_render = Template(self.template % self.tag_arguments)
        rendered_template = self.template_to_render.render(self.context)
        rgx = r'legend: { show: true }'
        self.assertRegex(rendered_template, rgx)

    def test_chart_legend_false(self):
        self.tag_arguments['show_legend'] = False
        self.template_to_render = Template(self.template % self.tag_arguments)
        rendered_template = self.template_to_render.render(self.context)
        rgx = r'legend: { show: false }'
        self.assertRegex(rendered_template, rgx)

    def test_chart_vertical_grid_line_true(self):
        self.tag_arguments['vertical_grid_line'] = True
        self.template_to_render = Template(self.template % self.tag_arguments)
        rendered_template = self.template_to_render.render(self.context)
        rgx = r'x: { show: true ,lines'
        self.assertRegex(rendered_template, rgx)

    def test_chart_vertical_grid_line_false(self):
        self.tag_arguments['vertical_grid_line'] = False
        self.template_to_render = Template(self.template % self.tag_arguments)
        rendered_template = self.template_to_render.render(self.context)
        rgx = r'x: { show: false ,lines'
        self.assertRegex(rendered_template, rgx)

    def test_chart_horizontal_grid_line_true(self):
        self.tag_arguments['horizontal_grid_line'] = True
        self.template_to_render = Template(self.template % self.tag_arguments)
        rendered_template = self.template_to_render.render(self.context)
        rgx = r'y: { show: true ,lines'
        self.assertRegex(rendered_template, rgx)

    def test_chart_horizontal_grid_line_false(self):
        self.tag_arguments['horizontal_grid_line'] = False
        self.template_to_render = Template(self.template % self.tag_arguments)
        rendered_template = self.template_to_render.render(self.context)
        rgx = r'zoom: { enabled: false },'
        self.assertRegex(rendered_template, rgx)

    def test_chart_zoom_true(self):
        self.tag_arguments['zoom'] = True
        self.template_to_render = Template(self.template % self.tag_arguments)
        rendered_template = self.template_to_render.render(self.context)
        rgx = r'zoom: { enabled: true },'
        self.assertRegex(rendered_template, rgx)

    def test_chart_zoom_false(self):
        self.tag_arguments['zoom'] = False
        self.template_to_render = Template(self.template % self.tag_arguments)
        rendered_template = self.template_to_render.render(self.context)
        rgx = r'y: { show: false ,lines'
        self.assertRegex(rendered_template, rgx)

    def test_chart_group_tooltip_true(self):
        self.tag_arguments['group_tooltip'] = True
        self.template_to_render = Template(self.template % self.tag_arguments)
        rendered_template = self.template_to_render.render(self.context)
        rgx = r'tooltip: { grouped: true },'
        self.assertRegex(rendered_template, rgx)

    def test_chart_group_tooltip_false(self):
        self.tag_arguments['group_tooltip'] = False
        self.template_to_render = Template(self.template % self.tag_arguments)
        rendered_template = self.template_to_render.render(self.context)
        rgx = r'tooltip: { grouped: false },'
        self.assertRegex(rendered_template, rgx)

    def test_chart_height(self):
        self.tag_arguments['height'] = 500
        self.template_to_render = Template(self.template % self.tag_arguments)
        rendered_template = self.template_to_render.render(self.context)
        rgx = r'size: { height: %s' % self.tag_arguments['height']
        self.assertRegex(rendered_template, rgx)

    def test_chart_width(self):
        self.tag_arguments['width'] = 402
        self.template_to_render = Template(self.template % self.tag_arguments)
        rendered_template = self.template_to_render.render(self.context)
        rgx = r'size: { height: 130, width: %s }' % self.tag_arguments['width']
        self.assertRegex(rendered_template, rgx)

    def test_colors(self):
        self.template_to_render = Template(self.template % self.tag_arguments)
        rendered_template = self.template_to_render.render(self.context)
        rgx = r'"A": "#FF34FF",'
        self.assertRegex(rendered_template, rgx)

    def test_x_is_category(self):
        self.tag_arguments['x_is_category'] = False
        self.template_to_render = Template(self.template % self.tag_arguments)
        self.assertRaises(
            ValueError, self.template_to_render.render, self.context)

    def test_data(self):
        self.template_to_render = Template(self.template % self.tag_arguments)
        rendered_template = self.template_to_render.render(self.context)
        self.assertTrue('["A", 26,35,52,34,45,74]' in rendered_template)
        self.assertRegex(
            rendered_template, r'x: "2d2014226823e74c2accfcce8e0ca141",')

        columns = (
                    '["2d2014226823e74c2accfcce8e0ca141", '
                    '\'2017-5-19\',\'2017-5-20\',\'2017-5-21\',\'2017-5-22\']'
                    )
        self.assertTrue(columns in rendered_template)

###############################################################################


class LineXYChartTest(SimpleTestCase):

    def setUp(self):
        self.line_xy_chart_data = {
            'horizontal_lines': [40],
            'data': [
                {'title': 'A',
                    'values': [(i, i*2) for i in range(3)], "color": "blue"},

            ],
            # 'groups': [('A', 'B')]
        }

        self.context = Context({'line_xy_chart': self.line_xy_chart_data})
        self.tag_arguments = {
            'bind_element': '#chart',
            'title': 'step-chart',
            'area': False,
            'labels': False,
            'vertical_grid_line': False,
            'horizontal_grid_line': False,
            'zoom': False,
            'show_legend': False,
            'group_tooltip': True,
            'height': 130,
            'width': 120,
            'show_points': True,
            'angle': True,
        }

        self.template = (
                '{%% load c3 %%}'
                '{%% line_xy "%(bind_element)s" '
                'line_xy_chart title="%(title)s" '
                'area=%(area)s '
                'labels=%(labels)s vertical_grid_line=%(vertical_grid_line)s '
                'horizontal_grid_line=%(horizontal_grid_line)s '
                'show_legend=%(show_legend)s zoom=%(zoom)s '
                'group_tooltip=%(group_tooltip)s '
                'height=%(height)s width=%(width)s '
                'show_points=%(show_points)s angle=%(angle)s %%}'
                )

    def test_bind_element(self):
        self.template_to_render = Template(self.template % self.tag_arguments)
        rendered_template = self.template_to_render.render(self.context)
        bind_to_rgx = r'bindto:\s+"%s"' % self.tag_arguments['bind_element']
        self.assertRegex(rendered_template, bind_to_rgx)

    def test_chart_title(self):
        self.tag_arguments['title'] = 'mytitle'
        self.template_to_render = Template(self.template % self.tag_arguments)
        rendered_template = self.template_to_render.render(self.context)
        rgx = r'title: { text: "%s"}' % 'mytitle'
        self.assertRegex(rendered_template, rgx)

    def test_chart_area_true(self):
        self.tag_arguments['area'] = True
        self.template_to_render = Template(self.template % self.tag_arguments)
        rendered_template = self.template_to_render.render(self.context)
        rgx = r'type : "area"'
        self.assertRegex(rendered_template, rgx)

    def test_chart_area_false(self):
        self.tag_arguments['area'] = False
        self.template_to_render = Template(self.template % self.tag_arguments)
        rendered_template = self.template_to_render.render(self.context)
        rgx = r'type : "line"'
        self.assertRegex(rendered_template, rgx)

    def test_chart_labels_true(self):
        self.tag_arguments['labels'] = True
        self.template_to_render = Template(self.template % self.tag_arguments)
        rendered_template = self.template_to_render.render(self.context)
        rgx = r'labels : true'
        self.assertRegex(rendered_template, rgx)

    def test_chart_labels_false(self):
        self.tag_arguments['labels'] = False
        self.template_to_render = Template(self.template % self.tag_arguments)
        rendered_template = self.template_to_render.render(self.context)
        rgx = r'labels : false'
        self.assertRegex(rendered_template, rgx)

    def test_chart_legend_true(self):
        self.tag_arguments['show_legend'] = True
        self.template_to_render = Template(self.template % self.tag_arguments)
        rendered_template = self.template_to_render.render(self.context)
        rgx = r'legend: { show: true }'
        self.assertRegex(rendered_template, rgx)

    def test_chart_legend_false(self):
        self.tag_arguments['show_legend'] = False
        self.template_to_render = Template(self.template % self.tag_arguments)
        rendered_template = self.template_to_render.render(self.context)
        rgx = r'legend: { show: false }'
        self.assertRegex(rendered_template, rgx)

    def test_chart_vertical_grid_line_true(self):
        self.tag_arguments['vertical_grid_line'] = True
        self.template_to_render = Template(self.template % self.tag_arguments)
        rendered_template = self.template_to_render.render(self.context)
        rgx = r'x: { show: true ,lines'
        self.assertRegex(rendered_template, rgx)

    def test_chart_vertical_grid_line_false(self):
        self.tag_arguments['vertical_grid_line'] = False
        self.template_to_render = Template(self.template % self.tag_arguments)
        rendered_template = self.template_to_render.render(self.context)
        rgx = r'x: { show: false ,lines'
        self.assertRegex(rendered_template, rgx)

    def test_chart_horizontal_grid_line_true(self):
        self.tag_arguments['horizontal_grid_line'] = True
        self.template_to_render = Template(self.template % self.tag_arguments)
        rendered_template = self.template_to_render.render(self.context)
        rgx = r'y: { show: true ,lines'
        self.assertRegex(rendered_template, rgx)

    def test_chart_horizontal_grid_line_false(self):
        self.tag_arguments['horizontal_grid_line'] = False
        self.template_to_render = Template(self.template % self.tag_arguments)
        rendered_template = self.template_to_render.render(self.context)
        rgx = r'zoom: { enabled: false },'
        self.assertRegex(rendered_template, rgx)

    def test_chart_zoom_true(self):
        self.tag_arguments['zoom'] = True
        self.template_to_render = Template(self.template % self.tag_arguments)
        rendered_template = self.template_to_render.render(self.context)
        rgx = r'zoom: { enabled: true },'
        self.assertRegex(rendered_template, rgx)

    def test_chart_zoom_false(self):
        self.tag_arguments['zoom'] = False
        self.template_to_render = Template(self.template % self.tag_arguments)
        rendered_template = self.template_to_render.render(self.context)
        rgx = r'y: { show: false ,lines'
        self.assertRegex(rendered_template, rgx)

    def test_chart_group_tooltip_true(self):
        self.tag_arguments['group_tooltip'] = True
        self.template_to_render = Template(self.template % self.tag_arguments)
        rendered_template = self.template_to_render.render(self.context)
        rgx = r'tooltip: { grouped: true },'
        self.assertRegex(rendered_template, rgx)

    def test_chart_group_tooltip_false(self):
        self.tag_arguments['group_tooltip'] = False
        self.template_to_render = Template(self.template % self.tag_arguments)
        rendered_template = self.template_to_render.render(self.context)
        rgx = r'tooltip: { grouped: false },'
        self.assertRegex(rendered_template, rgx)

    def test_chart_show_points_true(self):
        self.tag_arguments['show_points'] = True
        self.template_to_render = Template(self.template % self.tag_arguments)
        rendered_template = self.template_to_render.render(self.context)
        rgx = r'point: { show: true },'
        self.assertRegex(rendered_template, rgx)

    def test_chart_show_points_false(self):
        self.tag_arguments['show_points'] = False
        self.template_to_render = Template(self.template % self.tag_arguments)
        rendered_template = self.template_to_render.render(self.context)
        rgx = r'point: { show: false },'
        self.assertRegex(rendered_template, rgx)

    def test_chart_show_angle_true(self):
        self.tag_arguments['angle'] = True
        self.template_to_render = Template(self.template % self.tag_arguments)
        rendered_template = self.template_to_render.render(self.context)
        rgx = r'type : "line"'
        self.assertRegex(rendered_template, rgx)

    def test_chart_angle_false(self):
        self.tag_arguments['angle'] = False
        self.template_to_render = Template(self.template % self.tag_arguments)
        rendered_template = self.template_to_render.render(self.context)
        rgx = r'type : "spline"'
        self.assertRegex(rendered_template, rgx)

    def test_chart_height(self):
        self.tag_arguments['height'] = 500
        self.template_to_render = Template(self.template % self.tag_arguments)
        rendered_template = self.template_to_render.render(self.context)
        rgx = r'size: { height: %s' % self.tag_arguments['height']
        self.assertRegex(rendered_template, rgx)

    def test_chart_width(self):
        self.tag_arguments['width'] = 402
        self.template_to_render = Template(self.template % self.tag_arguments)
        rendered_template = self.template_to_render.render(self.context)
        rgx = r'size: { height: 130, width: %s }' % self.tag_arguments['width']
        self.assertRegex(rendered_template, rgx)

    def test_colors(self):
        self.template_to_render = Template(self.template % self.tag_arguments)
        rendered_template = self.template_to_render.render(self.context)
        rgx = r'colors: {  "A": "blue",  }'
        self.assertRegex(rendered_template, rgx)

    def test_data(self):
        self.template_to_render = Template(self.template % self.tag_arguments)
        rendered_template = self.template_to_render.render(self.context)
        self.assertTrue(
            'columns: [  ["A", 0,2,4],  ["A_x", 0,1,2],  ]' in
            rendered_template)

###############################################################################


class BarChartTest(SimpleTestCase):

    def setUp(self):
        self.bar_chart_data = {
            'x': ['2017-5-19', '2017-5-20', '2017-5-21', '2017-5-22'],
            'horizontal_lines': [40],
            'data': [
                {'title': 'A', 'values': [26, 5, 52, 74]},
                {'title': 'B', 'values': [54, 21, 40, 26], 'color': 'red'},
                {'title': 'C', 'values': [63, 14, 25, 11]},
            ],
            # 'groups': [('B', 'C')]
        }

        self.context = Context({'bar_chart': self.bar_chart_data})
        self.tag_arguments = {
            'bind_element': '#chart',
            'title': 'step-chart',
            'x_is_category': True,
            'labels': False,
            'vertical_grid_line': False,
            'horizontal_grid_line': False,
            'zoom': False,
            'show_legend': False,
            'group_tooltip': True,
            'height': 130,
            'width': 120,
            'column_width': 35
        }

        self.template = (
                '{%% load c3 %%}'
                '{%% bar "%(bind_element)s" bar_chart title="%(title)s" '
                'x_is_category=%(x_is_category)s '
                'labels=%(labels)s vertical_grid_line=%(vertical_grid_line)s '
                'horizontal_grid_line=%(horizontal_grid_line)s '
                'show_legend=%(show_legend)s zoom=%(zoom)s '
                'group_tooltip=%(group_tooltip)s '
                'height=%(height)s width=%(width)s '
                'column_width=%(column_width)s %%}'
                )

    def test_bind_element(self):
        self.template_to_render = Template(self.template % self.tag_arguments)
        rendered_template = self.template_to_render.render(self.context)
        bind_to_rgx = r'bindto:\s+"%s"' % self.tag_arguments['bind_element']
        self.assertRegex(rendered_template, bind_to_rgx)

    def test_chart_title(self):
        self.tag_arguments['title'] = 'mytitle'
        self.template_to_render = Template(self.template % self.tag_arguments)
        rendered_template = self.template_to_render.render(self.context)
        rgx = r'title: { text: "%s"}' % 'mytitle'
        self.assertRegex(rendered_template, rgx)

    def test_chart_labels_true(self):
        self.tag_arguments['labels'] = True
        self.template_to_render = Template(self.template % self.tag_arguments)
        rendered_template = self.template_to_render.render(self.context)
        rgx = r'labels : true'
        self.assertRegex(rendered_template, rgx)

    def test_chart_labels_false(self):
        self.tag_arguments['labels'] = False
        self.template_to_render = Template(self.template % self.tag_arguments)
        rendered_template = self.template_to_render.render(self.context)
        rgx = r'labels : false'
        self.assertRegex(rendered_template, rgx)

    def test_chart_legend_true(self):
        self.tag_arguments['show_legend'] = True
        self.template_to_render = Template(self.template % self.tag_arguments)
        rendered_template = self.template_to_render.render(self.context)
        rgx = r'legend: { show: true }'
        self.assertRegex(rendered_template, rgx)

    def test_chart_legend_false(self):
        self.tag_arguments['show_legend'] = False
        self.template_to_render = Template(self.template % self.tag_arguments)
        rendered_template = self.template_to_render.render(self.context)
        rgx = r'legend: { show: false }'
        self.assertRegex(rendered_template, rgx)

    def test_chart_vertical_grid_line_true(self):
        self.tag_arguments['vertical_grid_line'] = True
        self.template_to_render = Template(self.template % self.tag_arguments)
        rendered_template = self.template_to_render.render(self.context)
        rgx = r'x: { show: true ,lines'
        self.assertRegex(rendered_template, rgx)

    def test_chart_vertical_grid_line_false(self):
        self.tag_arguments['vertical_grid_line'] = False
        self.template_to_render = Template(self.template % self.tag_arguments)
        rendered_template = self.template_to_render.render(self.context)
        rgx = r'x: { show: false ,lines'
        self.assertRegex(rendered_template, rgx)

    def test_chart_horizontal_grid_line_true(self):
        self.tag_arguments['horizontal_grid_line'] = True
        self.template_to_render = Template(self.template % self.tag_arguments)
        rendered_template = self.template_to_render.render(self.context)
        rgx = r'y: { show: true ,lines'
        self.assertRegex(rendered_template, rgx)

    def test_chart_horizontal_grid_line_false(self):
        self.tag_arguments['horizontal_grid_line'] = False
        self.template_to_render = Template(self.template % self.tag_arguments)
        rendered_template = self.template_to_render.render(self.context)
        rgx = r'zoom: { enabled: false },'
        self.assertRegex(rendered_template, rgx)

    def test_chart_zoom_true(self):
        self.tag_arguments['zoom'] = True
        self.template_to_render = Template(self.template % self.tag_arguments)
        rendered_template = self.template_to_render.render(self.context)
        rgx = r'zoom: { enabled: true },'
        self.assertRegex(rendered_template, rgx)

    def test_chart_zoom_false(self):
        self.tag_arguments['zoom'] = False
        self.template_to_render = Template(self.template % self.tag_arguments)
        rendered_template = self.template_to_render.render(self.context)
        rgx = r'y: { show: false ,lines'
        self.assertRegex(rendered_template, rgx)

    def test_chart_group_tooltip_true(self):
        self.tag_arguments['group_tooltip'] = True
        self.template_to_render = Template(self.template % self.tag_arguments)
        rendered_template = self.template_to_render.render(self.context)
        rgx = r'tooltip: { grouped: true },'
        self.assertRegex(rendered_template, rgx)

    def test_chart_group_tooltip_false(self):
        self.tag_arguments['group_tooltip'] = False
        self.template_to_render = Template(self.template % self.tag_arguments)
        rendered_template = self.template_to_render.render(self.context)
        rgx = r'tooltip: { grouped: false },'
        self.assertRegex(rendered_template, rgx)

    def test_chart_height(self):
        self.tag_arguments['height'] = 500
        self.template_to_render = Template(self.template % self.tag_arguments)
        rendered_template = self.template_to_render.render(self.context)
        rgx = r'size: { height: %s' % self.tag_arguments['height']
        self.assertRegex(rendered_template, rgx)

    def test_chart_width(self):
        self.tag_arguments['width'] = 402
        self.template_to_render = Template(self.template % self.tag_arguments)
        rendered_template = self.template_to_render.render(self.context)
        rgx = r'size: { height: 130, width: %s }' % self.tag_arguments['width']
        self.assertRegex(rendered_template, rgx)

    def test_chart_column_width(self):
        self.tag_arguments['column_width'] = 35
        self.template_to_render = Template(self.template % self.tag_arguments)
        rendered_template = self.template_to_render.render(self.context)
        rgx = r'bar: { width: %s },' % self.tag_arguments['column_width']
        self.assertRegex(rendered_template, rgx)

    def test_colors(self):
        self.template_to_render = Template(self.template % self.tag_arguments)
        rendered_template = self.template_to_render.render(self.context)
        rgx = r'colors: {  "B": "red",  }'
        self.assertRegex(rendered_template, rgx)

    def test_x_is_category(self):
        self.tag_arguments['x_is_category'] = False
        self.template_to_render = Template(self.template % self.tag_arguments)
        self.assertRaises(
            ValueError, self.template_to_render.render, self.context)

    def test_data(self):
        self.template_to_render = Template(self.template % self.tag_arguments)
        rendered_template = self.template_to_render.render(self.context)
        self.assertTrue('["A", 26,5,52,74]' in rendered_template)
        self.assertTrue('["B", 54,21,40,26]' in rendered_template)
        self.assertTrue('["C", 63,14,25,11]' in rendered_template)
        self.assertRegex(
            rendered_template, r'x: "2d2014226823e74c2accfcce8e0ca141",')

        columns = (
                    '["2d2014226823e74c2accfcce8e0ca141", '
                    '\'2017-5-19\',\'2017-5-20\',\'2017-5-21\',\'2017-5-22\']'
                    )
        self.assertTrue(columns in rendered_template)


###############################################################################


class LineChartTest(SimpleTestCase):

    def setUp(self):
        self.line_chart_data = {
            'x': ['2017-5-19', '2017-5-20', '2017-5-21', '2017-5-22'],
            'horizontal_lines': [40],
            'data': [
                {'title': 'A', 'values': [26, 35, 52, 34, 45, 74]},
                {'title': 'B', 'values': [54, 25, 52, 26, 20, 89],
                    'color': 'red'},
            ],
            # 'groups': [('A', 'B')]
        }

        self.context = Context({'line_chart': self.line_chart_data})
        self.tag_arguments = {
            'bind_element': '#chart',
            'title': 'step-chart',
            'x_is_category': True,
            'area': False,
            'labels': False,
            'vertical_grid_line': False,
            'horizontal_grid_line': False,
            'zoom': False,
            'show_legend': False,
            'group_tooltip': True,
            'height': 130,
            'width': 120,
            'show_points': True,
            'angle': True,
        }

        self.template = (
                '{%% load c3 %%}'
                '{%% line "%(bind_element)s" '
                'line_chart title="%(title)s" '
                'area=%(area)s x_is_category=%(x_is_category)s '
                'labels=%(labels)s vertical_grid_line=%(vertical_grid_line)s '
                'horizontal_grid_line=%(horizontal_grid_line)s '
                'show_legend=%(show_legend)s zoom=%(zoom)s '
                'group_tooltip=%(group_tooltip)s '
                'height=%(height)s width=%(width)s '
                'show_points=%(show_points)s angle=%(angle)s %%}'
                )

    def test_bind_element(self):
        self.template_to_render = Template(self.template % self.tag_arguments)
        rendered_template = self.template_to_render.render(self.context)
        bind_to_rgx = r'bindto:\s+"%s"' % self.tag_arguments['bind_element']
        self.assertRegex(rendered_template, bind_to_rgx)

    def test_chart_title(self):
        self.tag_arguments['title'] = 'mytitle'
        self.template_to_render = Template(self.template % self.tag_arguments)
        rendered_template = self.template_to_render.render(self.context)
        rgx = r'title: { text: "%s"}' % 'mytitle'
        self.assertRegex(rendered_template, rgx)

    def test_chart_area_true(self):
        self.tag_arguments['area'] = True
        self.template_to_render = Template(self.template % self.tag_arguments)
        rendered_template = self.template_to_render.render(self.context)
        rgx = r'type : "area"'
        self.assertRegex(rendered_template, rgx)

    def test_chart_area_false(self):
        self.tag_arguments['area'] = False
        self.template_to_render = Template(self.template % self.tag_arguments)
        rendered_template = self.template_to_render.render(self.context)
        rgx = r'type : "line"'
        self.assertRegex(rendered_template, rgx)

    def test_chart_labels_true(self):
        self.tag_arguments['labels'] = True
        self.template_to_render = Template(self.template % self.tag_arguments)
        rendered_template = self.template_to_render.render(self.context)
        rgx = r'labels : true'
        self.assertRegex(rendered_template, rgx)

    def test_chart_labels_false(self):
        self.tag_arguments['labels'] = False
        self.template_to_render = Template(self.template % self.tag_arguments)
        rendered_template = self.template_to_render.render(self.context)
        rgx = r'labels : false'
        self.assertRegex(rendered_template, rgx)

    def test_chart_legend_true(self):
        self.tag_arguments['show_legend'] = True
        self.template_to_render = Template(self.template % self.tag_arguments)
        rendered_template = self.template_to_render.render(self.context)
        rgx = r'legend: { show: true }'
        self.assertRegex(rendered_template, rgx)

    def test_chart_legend_false(self):
        self.tag_arguments['show_legend'] = False
        self.template_to_render = Template(self.template % self.tag_arguments)
        rendered_template = self.template_to_render.render(self.context)
        rgx = r'legend: { show: false }'
        self.assertRegex(rendered_template, rgx)

    def test_chart_vertical_grid_line_true(self):
        self.tag_arguments['vertical_grid_line'] = True
        self.template_to_render = Template(self.template % self.tag_arguments)
        rendered_template = self.template_to_render.render(self.context)
        rgx = r'x: { show: true ,lines'
        self.assertRegex(rendered_template, rgx)

    def test_chart_vertical_grid_line_false(self):
        self.tag_arguments['vertical_grid_line'] = False
        self.template_to_render = Template(self.template % self.tag_arguments)
        rendered_template = self.template_to_render.render(self.context)
        rgx = r'x: { show: false ,lines'
        self.assertRegex(rendered_template, rgx)

    def test_chart_horizontal_grid_line_true(self):
        self.tag_arguments['horizontal_grid_line'] = True
        self.template_to_render = Template(self.template % self.tag_arguments)
        rendered_template = self.template_to_render.render(self.context)
        rgx = r'y: { show: true ,lines'
        self.assertRegex(rendered_template, rgx)

    def test_chart_horizontal_grid_line_false(self):
        self.tag_arguments['horizontal_grid_line'] = False
        self.template_to_render = Template(self.template % self.tag_arguments)
        rendered_template = self.template_to_render.render(self.context)
        rgx = r'zoom: { enabled: false },'
        self.assertRegex(rendered_template, rgx)

    def test_chart_zoom_true(self):
        self.tag_arguments['zoom'] = True
        self.template_to_render = Template(self.template % self.tag_arguments)
        rendered_template = self.template_to_render.render(self.context)
        rgx = r'zoom: { enabled: true },'
        self.assertRegex(rendered_template, rgx)

    def test_chart_zoom_false(self):
        self.tag_arguments['zoom'] = False
        self.template_to_render = Template(self.template % self.tag_arguments)
        rendered_template = self.template_to_render.render(self.context)
        rgx = r'y: { show: false ,lines'
        self.assertRegex(rendered_template, rgx)

    def test_chart_group_tooltip_true(self):
        self.tag_arguments['group_tooltip'] = True
        self.template_to_render = Template(self.template % self.tag_arguments)
        rendered_template = self.template_to_render.render(self.context)
        rgx = r'tooltip: { grouped: true },'
        self.assertRegex(rendered_template, rgx)

    def test_chart_group_tooltip_false(self):
        self.tag_arguments['group_tooltip'] = False
        self.template_to_render = Template(self.template % self.tag_arguments)
        rendered_template = self.template_to_render.render(self.context)
        rgx = r'tooltip: { grouped: false },'
        self.assertRegex(rendered_template, rgx)

    def test_chart_show_points_true(self):
        self.tag_arguments['show_points'] = True
        self.template_to_render = Template(self.template % self.tag_arguments)
        rendered_template = self.template_to_render.render(self.context)
        rgx = r'point: { show: true },'
        self.assertRegex(rendered_template, rgx)

    def test_chart_show_points_false(self):
        self.tag_arguments['show_points'] = False
        self.template_to_render = Template(self.template % self.tag_arguments)
        rendered_template = self.template_to_render.render(self.context)
        rgx = r'point: { show: false },'
        self.assertRegex(rendered_template, rgx)

    def test_chart_show_angle_true(self):
        self.tag_arguments['angle'] = True
        self.template_to_render = Template(self.template % self.tag_arguments)
        rendered_template = self.template_to_render.render(self.context)
        rgx = r'type : "line"'
        self.assertRegex(rendered_template, rgx)

    def test_chart_angle_false(self):
        self.tag_arguments['angle'] = False
        self.template_to_render = Template(self.template % self.tag_arguments)
        rendered_template = self.template_to_render.render(self.context)
        rgx = r'type : "spline"'
        self.assertRegex(rendered_template, rgx)

    def test_chart_height(self):
        self.tag_arguments['height'] = 500
        self.template_to_render = Template(self.template % self.tag_arguments)
        rendered_template = self.template_to_render.render(self.context)
        rgx = r'size: { height: %s' % self.tag_arguments['height']
        self.assertRegex(rendered_template, rgx)

    def test_chart_width(self):
        self.tag_arguments['width'] = 402
        self.template_to_render = Template(self.template % self.tag_arguments)
        rendered_template = self.template_to_render.render(self.context)
        rgx = r'size: { height: 130, width: %s }' % self.tag_arguments['width']
        self.assertRegex(rendered_template, rgx)

    def test_colors(self):
        self.template_to_render = Template(self.template % self.tag_arguments)
        rendered_template = self.template_to_render.render(self.context)
        rgx = r'colors: {  "B": "red",  }'
        self.assertRegex(rendered_template, rgx)

    def test_data(self):
        self.template_to_render = Template(self.template % self.tag_arguments)
        rendered_template = self.template_to_render.render(self.context)
        self.assertTrue('["A", 26,35,52,34,45,74]' in rendered_template)
        self.assertTrue('["B", 54,25,52,26,20,89]' in rendered_template)
        self.assertTrue(
            ('["2d2014226823e74c2accfcce8e0ca141",'
            '\'2017-5-19\',\'2017-5-20\',\'2017-5-21\',\'2017-5-22\']') in
            rendered_template)

###############################################################################


class GaugeSingleColumnChartTest(SimpleTestCase):
    """ Tests single column, half circle with color pattern """

    def setUp(self):
        self.gauge_chart_data = {
            'data': [
                {'title': 'A', 'value': 91.4,
                 },
            ],
            'color':
                {'pattern': ['#FF0000', '#F97600', '#F6C600', '#60B044'],
                 'threshold': [30, 60, 90, 100]
                 }
        }

        self.context = Context({'gauge_chart': self.gauge_chart_data})

        self.tag_arguments = {
            'bind_element': '#chart',
            'title': 'gauge-chart',
            'labels': True,
            'show_legend': True,
            'min': 0,
            'max': 100,
            'thickness': 50,
            'height': None,
            'full_circle': False,
            'starting_angle': None,
            'interaction': None
        }

        self.template = (
            '{%% load c3 %%}'
            '{%% gauge "%(bind_element)s" '
            'gauge_chart title="%(title)s" '
            'labels=%(labels)s '
            'show_legend=%(show_legend)s '
            'min=%(min)s max=%(max)s thickness=%(thickness)s '
            'height=%(height)s '
            'full_circle=%(full_circle)s starting_angle=%(starting_angle)s '
            'interaction=%(interaction)s %%}'
        )

    def test_bind_element(self):
        self.template_to_render = Template(self.template % self.tag_arguments)
        rendered_template = self.template_to_render.render(self.context)
        bind_to_rgx = r'bindto:\s+"%s"' % self.tag_arguments['bind_element']
        self.assertRegex(rendered_template, bind_to_rgx)

    def test_data(self):
        self.template_to_render = Template(self.template % self.tag_arguments)
        rendered_template = self.template_to_render.render(self.context)
        self.assertRegex(rendered_template, r'columns:\s\[\s+\[\"A\",\s91.4\],\s+\]')

    def test_pattern_colors(self):
        self.template_to_render = Template(self.template % self.tag_arguments)
        rendered_template = self.template_to_render.render(self.context)
        self.assertRegex(rendered_template, r"pattern:\s\['#FF0000',\s'#F97600',\s'#F6C600',\s'#60B044'\]")

    def test_pattern_threshold(self):
        self.template_to_render = Template(self.template % self.tag_arguments)
        rendered_template = self.template_to_render.render(self.context)
        self.assertRegex(rendered_template, r'values:\s\[30,\s60,\s90,\s100\]')

    def test_chart_title(self):
        self.template_to_render = Template(self.template % self.tag_arguments)
        rendered_template = self.template_to_render.render(self.context)
        rgx = r'title: {text: "%s"}' % 'gauge-chart'
        self.assertRegex(rendered_template, rgx)

    def test_labels_true(self):
        self.tag_arguments['labels'] = True
        self.template_to_render = Template(self.template % self.tag_arguments)
        rendered_template = self.template_to_render.render(self.context)
        rgx = r'show:\strue\s//\sto turn off the min/max labels.'
        self.assertRegex(rendered_template, rgx)

    def test_labels_false(self):
        self.tag_arguments['labels'] = False
        self.template_to_render = Template(self.template % self.tag_arguments)
        rendered_template = self.template_to_render.render(self.context)
        rgx = r'show:\sfalse\s//\sto turn off the min/max labels.'
        self.assertRegex(rendered_template, rgx)

    def test_legend_true(self):
        self.tag_arguments['show_legend'] = True
        self.template_to_render = Template(self.template % self.tag_arguments)
        rendered_template = self.template_to_render.render(self.context)
        rgx = r'legend: {show: true}'
        self.assertRegex(rendered_template, rgx)

    def test_legend_false(self):
        self.tag_arguments['show_legend'] = False
        self.template_to_render = Template(self.template % self.tag_arguments)
        rendered_template = self.template_to_render.render(self.context)
        rgx = r'legend: {show: false}'
        self.assertRegex(rendered_template, rgx)

    def test_min(self):
        self.tag_arguments['min'] = 0
        self.template_to_render = Template(self.template % self.tag_arguments)
        rendered_template = self.template_to_render.render(self.context)
        rgx = r'min: 0'
        self.assertRegex(rendered_template, rgx)

    def test_max(self):
        self.tag_arguments['max'] = 100
        self.template_to_render = Template(self.template % self.tag_arguments)
        rendered_template = self.template_to_render.render(self.context)
        rgx = r'max: 100'
        self.assertRegex(rendered_template, rgx)

    def test_thickness(self):
        self.tag_arguments['width'] = 50
        self.template_to_render = Template(self.template % self.tag_arguments)
        rendered_template = self.template_to_render.render(self.context)
        rgx = r'width: 50'
        self.assertRegex(rendered_template, rgx)

    def test_height(self):
        self.tag_arguments['height'] = 250
        self.template_to_render = Template(self.template % self.tag_arguments)
        rendered_template = self.template_to_render.render(self.context)
        rgx = r'size:\s{\n\s+height:\s250,\n\s+}'
        self.assertRegex(rendered_template, rgx)

    def test_full_circle_false(self):
        self.tag_arguments['full_circle'] = False
        self.template_to_render = Template(self.template % self.tag_arguments)
        rendered_template = self.template_to_render.render(self.context)
        rgx = r'gauge:\s{\n\s+fullCircle:\sfalse'
        self.assertRegex(rendered_template, rgx)

    def test_starting_angle(self):
        self.tag_arguments['full_circle'] = None
        self.template_to_render = Template(self.template % self.tag_arguments)
        rendered_template = self.template_to_render.render(self.context)
        rgx = r'startingAngle:\sundefined'
        self.assertRegex(rendered_template, rgx)

    def test_interactions_true(self):
        self.tag_arguments['interaction'] = True
        self.template_to_render = Template(self.template % self.tag_arguments)
        rendered_template = self.template_to_render.render(self.context)
        rgx = r'interaction:\s{\senabled:\strue}'
        self.assertRegex(rendered_template, rgx)

    def test_interactions_false(self):
        self.tag_arguments['interaction'] = False
        self.template_to_render = Template(self.template % self.tag_arguments)
        rendered_template = self.template_to_render.render(self.context)
        rgx = r'interaction:\s{\senabled:\sfalse}'
        self.assertRegex(rendered_template, rgx)

###############################################################################


class GaugeMultiColumnChartTest(SimpleTestCase):
    """ Tests multi-column, half circle with column specific colors """

    def setUp(self):
        self.gauge_chart_data = {
            'data': [
                {'title': 'A', 'value': 65.7,
                 'color': '#FF8C00'
                 },
                {'title': 'B', 'value': 42.3,
                 'color': '#F6C600'
                 },
            ],
        }

        self.context = Context({'gauge_chart': self.gauge_chart_data})

        self.tag_arguments = {
            'bind_element': '#chart',
            'title': 'gauge-chart',
            'labels': True,
            'show_legend': True,
            'min': 0,
            'max': 100,
            'thickness': 50,
            'height': None,
            'full_circle': False,
            'starting_angle': None,
            'interaction': None
        }

        self.template = (
            '{%% load c3 %%}'
            '{%% gauge "%(bind_element)s" '
            'gauge_chart title="%(title)s" '
            'labels=%(labels)s '
            'show_legend=%(show_legend)s '
            'min=%(min)s max=%(max)s thickness=%(thickness)s '
            'height=%(height)s '
            'full_circle=%(full_circle)s starting_angle=%(starting_angle)s '
            'interaction=%(interaction)s %%}'
        )

    def test_data(self):
        self.template_to_render = Template(self.template % self.tag_arguments)
        rendered_template = self.template_to_render.render(self.context)
        self.assertRegex(rendered_template, r'columns:\s\[\s+\[\"A\",\s65.7\],\s+\[\"B\",\s42.3\],\s+\]')

    def test_colors(self):
        self.template_to_render = Template(self.template % self.tag_arguments)
        rendered_template = self.template_to_render.render(self.context)
        self.assertRegex(rendered_template, r'colors:\s{\s+\"A\":\s\"#FF8C00\",\s+\"B\":\s\"#F6C600\",\s+\}')

    def test_full_circle_false(self):
        self.tag_arguments['full_circle'] = False
        self.template_to_render = Template(self.template % self.tag_arguments)
        rendered_template = self.template_to_render.render(self.context)
        rgx = r'gauge:\s{\n\s+fullCircle:\sfalse'
        self.assertRegex(rendered_template, rgx)

    def test_starting_angle(self):
        self.tag_arguments['full_circle'] = None
        self.template_to_render = Template(self.template % self.tag_arguments)
        rendered_template = self.template_to_render.render(self.context)
        rgx = r'startingAngle:\sundefined'
        self.assertRegex(rendered_template, rgx)

###############################################################################


class GaugeFullCircleChartTest(SimpleTestCase):
    """ Tests full circle gauge chart """

    def setUp(self):
        self.gauge_chart_data = {
            'data': [
                {'title': 'A', 'value': 91.4,
                 },
            ],
            'color':
                {'pattern': ['#FF0000', '#F97600', '#F6C600', '#60B044'],
                 'threshold': [30, 60, 90, 100]
                 }
        }

        self.context = Context({'gauge_chart': self.gauge_chart_data})

        self.tag_arguments = {
            'bind_element': '#chart',
            'title': 'gauge-chart',
            'labels': True,
            'show_legend': True,
            'min': 0,
            'max': 100,
            'thickness': 50,
            'height': None,
            'full_circle': True,
            'starting_angle': '6.28',
            'interaction': None
        }

        self.template = (
            '{%% load c3 %%}'
            '{%% gauge "%(bind_element)s" '
            'gauge_chart title="%(title)s" '
            'labels=%(labels)s '
            'show_legend=%(show_legend)s '
            'min=%(min)s max=%(max)s thickness=%(thickness)s '
            'height=%(height)s '
            'full_circle=%(full_circle)s starting_angle=%(starting_angle)s '
            'interaction=%(interaction)s %%}'
        )

    def test_full_circle_false(self):
        self.tag_arguments['full_circle'] = True
        self.template_to_render = Template(self.template % self.tag_arguments)
        rendered_template = self.template_to_render.render(self.context)
        rgx = r'gauge:\s{\n\s+fullCircle:\strue'
        self.assertRegex(rendered_template, rgx)

    def test_starting_angle(self):
        self.tag_arguments['full_circle'] = None
        self.template_to_render = Template(self.template % self.tag_arguments)
        rendered_template = self.template_to_render.render(self.context)
        rgx = r'startingAngle:\s6.28'
        self.assertRegex(rendered_template, rgx)
