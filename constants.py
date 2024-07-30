import pandas as pd

IMG_FILES = [# list of image files in same directory
    '0.jpg',
    '1.jpg',
    '2.jpg',
    '4.jpg',
]
FLOOR_DICT = {}
i = 0
for name in IMG_FILES:
    FLOOR_DICT[i] = name[:name.find('.')]
    i += 1
MARKERS = pd.read_csv('markerSequence.csv').iloc[:, 0].astype(
    str).values.tolist()
BUTTONS = pd.read_csv('buttons.csv').iloc[:, 1].astype(
    str).values.tolist()
SURVEY = pd.read_csv('survey.csv')
for i, marker in enumerate(MARKERS):
    MARKERS[i] = marker.title().replace('_', ' ')
TASK_LIST_LENGTH = 20
SIGN_LIST_LENGTH = 20
LANDMARK = pd.read_csv('landmarks.csv')
LANDMARK_RADIUS = 40
X, Y = (1050, 816)  # canvas size 7:5
CURSOR_TYPE = "circle"  # defines cursor appearance when hovering over canvas
CURSOR_OFFSET = 1  # adjust position of circle cursor for dot to be in center
PLOT_SIZE = 3  # size of circle radius (in px)
PLOT_COUNT_MAX = 8  # trailing plot count max
ADJ_SIZE = 2  # plotAdjust size (in px)
S_AUTOSAVE = 5  # autosave checkpoint time (seconds)
MS_AUTOSAVE = S_AUTOSAVE*1000  # autosave checkpoint time (milliseconds)
MSG_TIME = 900  # time for on screen messages (milliseconds)
RED = '#FF0000'
CYAN = '#00eaff'
ORANGE = '#e59400'
GREEN = '#00FF00'
YELLOW = '#FFFF00'
BROWN = '#332100'
BTN_HEIGHT = 2
BTN_WIDTH = 10
BTN_SPACING = 22
URL = 'https://www.google.com/'
