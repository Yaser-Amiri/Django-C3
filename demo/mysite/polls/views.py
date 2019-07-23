from django.shortcuts import render
# Create your views here.


def main(request):
    line = {
        'x': ['2017-5-19', '2017-5-20', '2017-5-21', '2017-5-22'],
        'horizontal_lines': [40],
        'data': [
            {'title': 'A', 'values': [26, 35, 52, 34, 45, 74]},
            {'title': 'B', 'values': [54, 25, 52, 26, 20, 89]},
        ],
        # 'groups': [('A', 'B')]
    }

    step = {
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

    bar = {
        'x': ['2017-5-19', '2017-5-20', '2017-5-21', '2017-5-22'],
        'horizontal_lines': [40],
        'data': [
            {'title': 'A', 'values': [26, 5, 52, 74]},
            {'title': 'B', 'values': [54, 21, 40, 26]},
            {'title': 'C', 'values': [63, 14, 25, 11]},
        ],
        # 'groups': [('B', 'C')]
    }

    pie = [
            {'title': 'A', 'value': 6},
            {'title': 'B', 'value': 10},
            {'title': 'C', 'value': 84},
        ]

    donut = [
            {'title': 'A', 'value': 6},
            {'title': 'B', 'value': 10},
            {'title': 'C', 'value': 84},
        ]
    xy = {
        'horizontal_lines': [40],
        'data': [
            {'title': 'A', 'values': [(i, i*2) for i in range(25)]},

        ],
        # 'groups': [('A', 'B')]
    }

    gauge0 = {
        'data': [
            {'title': 'A', 'value': 91.4,
             'color': '#FF8C00'
             },
        ],
    }

    gauge1 = {
        'data': [
            {'title': 'A', 'value': 65.7,
             'color': '#FF8C00'
             },
            {'title': 'B', 'value': 42.3,
             'color': '#F6C600'
             },
        ],
    }

    gauge2 = {
        'data': [
            {'title': 'A', 'value': 91.4,
             },
        ],
        'color':
            {'pattern': ['#FF0000', '#F97600', '#F6C600', '#60B044'],
             'threshold': [30, 60, 90, 100]
             }
    }

    return render(
        request, 'polls/index.html', {
            'bar0': bar, 'pie0': pie, 'step0': step,
            'donut0': donut, 'line0': line, 'xy': xy,
            'gauge0': gauge0, 'gauge1': gauge1, 'gauge2': gauge2}
    )
