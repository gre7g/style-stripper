from mock_wx.event_binder import EventBinder

EVT_SIZE = EventBinder(2000000)
EVT_SIZING = EventBinder(2000001)
EVT_MOVE = EventBinder(2000002)
EVT_MOVING = EventBinder(2000003)
EVT_MOVE_START = EventBinder(2000004)
EVT_MOVE_END = EventBinder(2000005)
EVT_CLOSE = EventBinder(2000006)
EVT_END_SESSION = EventBinder(2000007)
EVT_QUERY_END_SESSION = EventBinder(2000008)
EVT_PAINT = EventBinder(2000009)
EVT_NC_PAINT = EventBinder(2000010)
EVT_ERASE_BACKGROUND = EventBinder(2000011)
EVT_CHAR = EventBinder(2000012)
EVT_KEY_DOWN = EventBinder(2000013)
EVT_KEY_UP = EventBinder(2000014)
EVT_HOTKEY = EventBinder(2000015)
EVT_CHAR_HOOK = EventBinder(2000016)
EVT_MENU_OPEN = EventBinder(2000017)
EVT_MENU_CLOSE = EventBinder(2000018)
EVT_MENU_HIGHLIGHT = EventBinder(2000019)
EVT_MENU_HIGHLIGHT_ALL = EventBinder(2000020)
EVT_SET_FOCUS = EventBinder(2000021)
EVT_KILL_FOCUS = EventBinder(2000022)
EVT_CHILD_FOCUS = EventBinder(2000023)
EVT_ACTIVATE = EventBinder(2000024)
EVT_ACTIVATE_APP = EventBinder(2000025)
EVT_HIBERNATE = EventBinder(2000026)
EVT_DROP_FILES = EventBinder(2000027)
EVT_INIT_DIALOG = EventBinder(2000028)
EVT_SYS_COLOUR_CHANGED = EventBinder(2000029)
EVT_DISPLAY_CHANGED = EventBinder(2000030)
EVT_SHOW = EventBinder(2000031)
EVT_MAXIMIZE = EventBinder(2000032)
EVT_ICONIZE = EventBinder(2000033)
EVT_NAVIGATION_KEY = EventBinder(2000034)
EVT_PALETTE_CHANGED = EventBinder(2000035)
EVT_QUERY_NEW_PALETTE = EventBinder(2000036)
EVT_WINDOW_CREATE = EventBinder(2000037)
EVT_WINDOW_DESTROY = EventBinder(2000038)
EVT_SET_CURSOR = EventBinder(2000039)
EVT_MOUSE_CAPTURE_CHANGED = EventBinder(2000040)
EVT_MOUSE_CAPTURE_LOST = EventBinder(2000041)

EVT_LEFT_DOWN = EventBinder(2000042)
EVT_LEFT_UP = EventBinder(2000043)
EVT_MIDDLE_DOWN = EventBinder(2000044)
EVT_MIDDLE_UP = EventBinder(2000045)
EVT_RIGHT_DOWN = EventBinder(2000046)
EVT_RIGHT_UP = EventBinder(2000047)
EVT_MOTION = EventBinder(2000048)
EVT_LEFT_DCLICK = EventBinder(2000049)
EVT_MIDDLE_DCLICK = EventBinder(2000050)
EVT_RIGHT_DCLICK = EventBinder(2000051)
EVT_LEAVE_WINDOW = EventBinder(2000052)
EVT_ENTER_WINDOW = EventBinder(2000053)
EVT_MOUSEWHEEL = EventBinder(2000054)
EVT_MOUSE_AUX1_DOWN = EventBinder(2000055)
EVT_MOUSE_AUX1_UP = EventBinder(2000056)
EVT_MOUSE_AUX1_DCLICK = EventBinder(2000057)
EVT_MOUSE_AUX2_DOWN = EventBinder(2000058)
EVT_MOUSE_AUX2_UP = EventBinder(2000059)
EVT_MOUSE_AUX2_DCLICK = EventBinder(2000060)

EVT_MOUSE_EVENTS = EventBinder(2000061)


# Scrolling from wxWindow (sent to wxScrolledWindow)
EVT_SCROLLWIN = EventBinder(2000062)

EVT_SCROLLWIN_TOP = EventBinder(2000063)
EVT_SCROLLWIN_BOTTOM = EventBinder(2000064)
EVT_SCROLLWIN_LINEUP = EventBinder(2000065)
EVT_SCROLLWIN_LINEDOWN = EventBinder(2000066)
EVT_SCROLLWIN_PAGEUP = EventBinder(2000067)
EVT_SCROLLWIN_PAGEDOWN = EventBinder(2000068)
EVT_SCROLLWIN_THUMBTRACK = EventBinder(2000069)
EVT_SCROLLWIN_THUMBRELEASE = EventBinder(2000070)

# Scrolling from wx.Slider and wx.ScrollBar
EVT_SCROLL = EventBinder(2000071)

EVT_SCROLL_TOP = EventBinder(2000072)
EVT_SCROLL_BOTTOM = EventBinder(2000073)
EVT_SCROLL_LINEUP = EventBinder(2000074)
EVT_SCROLL_LINEDOWN = EventBinder(2000075)
EVT_SCROLL_PAGEUP = EventBinder(2000076)
EVT_SCROLL_PAGEDOWN = EventBinder(2000077)
EVT_SCROLL_THUMBTRACK = EventBinder(2000078)
EVT_SCROLL_THUMBRELEASE = EventBinder(2000079)
EVT_SCROLL_CHANGED = EventBinder(2000080)
EVT_SCROLL_ENDSCROLL = EVT_SCROLL_CHANGED

# Scrolling from wx.Slider and wx.ScrollBar, with an id
EVT_COMMAND_SCROLL = EventBinder(2000081)

EVT_COMMAND_SCROLL_TOP = EventBinder(2000082)
EVT_COMMAND_SCROLL_BOTTOM = EventBinder(2000083)
EVT_COMMAND_SCROLL_LINEUP = EventBinder(2000084)
EVT_COMMAND_SCROLL_LINEDOWN = EventBinder(2000085)
EVT_COMMAND_SCROLL_PAGEUP = EventBinder(2000086)
EVT_COMMAND_SCROLL_PAGEDOWN = EventBinder(2000087)
EVT_COMMAND_SCROLL_THUMBTRACK = EventBinder(2000088)
EVT_COMMAND_SCROLL_THUMBRELEASE = EventBinder(2000089)
EVT_COMMAND_SCROLL_CHANGED = EventBinder(2000090)
EVT_COMMAND_SCROLL_ENDSCROLL = EVT_COMMAND_SCROLL_CHANGED

EVT_BUTTON = EventBinder(2000091)
EVT_CHECKBOX = EventBinder(2000092)
EVT_CHOICE = EventBinder(2000093)
EVT_LISTBOX = EventBinder(2000094)
EVT_LISTBOX_DCLICK = EventBinder(2000095)
EVT_MENU = EventBinder(2000096)
EVT_MENU_RANGE = EventBinder(2000097)
EVT_SLIDER = EventBinder(2000098)
EVT_RADIOBOX = EventBinder(2000099)
EVT_RADIOBUTTON = EventBinder(2000100)

EVT_SCROLLBAR = EventBinder(2000101)
EVT_VLBOX = EventBinder(2000102)
EVT_COMBOBOX = EventBinder(2000103)
EVT_TOOL = EventBinder(2000104)
EVT_TOOL_RANGE = EventBinder(2000105)
EVT_TOOL_RCLICKED = EventBinder(2000106)
EVT_TOOL_RCLICKED_RANGE = EventBinder(2000107)
EVT_TOOL_ENTER = EventBinder(2000108)
EVT_TOOL_DROPDOWN = EventBinder(2000109)
EVT_CHECKLISTBOX = EventBinder(2000110)
EVT_COMBOBOX_DROPDOWN = EventBinder(2000111)
EVT_COMBOBOX_CLOSEUP = EventBinder(2000112)

EVT_COMMAND_LEFT_CLICK = EventBinder(2000113)
EVT_COMMAND_LEFT_DCLICK = EventBinder(2000114)
EVT_COMMAND_RIGHT_CLICK = EventBinder(2000115)
EVT_COMMAND_RIGHT_DCLICK = EventBinder(2000116)
EVT_COMMAND_SET_FOCUS = EventBinder(2000117)
EVT_COMMAND_KILL_FOCUS = EventBinder(2000118)
EVT_COMMAND_ENTER = EventBinder(2000119)

EVT_HELP = EventBinder(2000120)
EVT_HELP_RANGE = EventBinder(2000121)
EVT_DETAILED_HELP = EventBinder(2000122)
EVT_DETAILED_HELP_RANGE = EventBinder(2000123)

EVT_IDLE = EventBinder(2000124)

EVT_UPDATE_UI = EventBinder(2000125)
EVT_UPDATE_UI_RANGE = EventBinder(2000126)

EVT_CONTEXT_MENU = EventBinder(2000127)

EVT_THREAD = EventBinder(2000128)

EVT_WINDOW_MODAL_DIALOG_CLOSED = EventBinder(2000130)

EVT_JOY_BUTTON_DOWN = EventBinder(2000131)
EVT_JOY_BUTTON_UP = EventBinder(2000132)
EVT_JOY_MOVE = EventBinder(2000133)
EVT_JOY_ZMOVE = EventBinder(2000134)
EVT_JOYSTICK_EVENTS = EventBinder(2000135)

EVT_TIMER = EventBinder(2000136)
EVT_NOTEBOOK_PAGE_CHANGED = EventBinder(2000137)
EVT_NOTEBOOK_PAGE_CHANGING = EventBinder(2000138)

EVT_BOOKCTRL_PAGE_CHANGED = EVT_NOTEBOOK_PAGE_CHANGED
EVT_BOOKCTRL_PAGE_CHANGING = EVT_NOTEBOOK_PAGE_CHANGING

EVT_SPLITTER_SASH_POS_CHANGED = EventBinder(2000139)
EVT_SPLITTER_SASH_POS_CHANGING = EventBinder(2000140)
EVT_SPLITTER_DOUBLECLICKED = EventBinder(2000141)
EVT_SPLITTER_UNSPLIT = EventBinder(2000142)
EVT_SPLITTER_DCLICK = EVT_SPLITTER_DOUBLECLICKED

EVT_COLLAPSIBLEPANE_CHANGED = EventBinder(2000143)

EVT_TEXT = EventBinder(2000144)
EVT_TEXT_ENTER = EventBinder(2000145)
EVT_TEXT_URL = EventBinder(2000146)
EVT_TEXT_MAXLEN = EventBinder(2000147)
EVT_TEXT_CUT = EventBinder(2000148)
EVT_TEXT_COPY = EventBinder(2000149)
EVT_TEXT_PASTE = EventBinder(2000150)

EVT_HEADER_CLICK = EventBinder(2000151)
EVT_HEADER_RIGHT_CLICK = EventBinder(2000152)
EVT_HEADER_MIDDLE_CLICK = EventBinder(2000153)
EVT_HEADER_DCLICK = EventBinder(2000154)
EVT_HEADER_RIGHT_DCLICK = EventBinder(2000155)
EVT_HEADER_MIDDLE_DCLICK = EventBinder(2000156)
EVT_HEADER_SEPARATOR_DCLICK = EventBinder(2000157)
EVT_HEADER_BEGIN_RESIZE = EventBinder(2000158)
EVT_HEADER_RESIZING = EventBinder(2000159)
EVT_HEADER_END_RESIZE = EventBinder(2000160)
EVT_HEADER_BEGIN_REORDER = EventBinder(2000161)
EVT_HEADER_END_REORDER = EventBinder(2000162)
EVT_HEADER_DRAGGING_CANCELLED = EventBinder(2000163)

EVT_SEARCHCTRL_CANCEL_BTN = EventBinder(2000164)
EVT_SEARCHCTRL_SEARCH_BTN = EventBinder(2000165)

EVT_SPIN_UP = EventBinder(2000166)
EVT_SPIN_DOWN = EventBinder(2000167)
EVT_SPIN = EventBinder(2000168)
EVT_SPINCTRL = EventBinder(2000169)
EVT_SPINCTRLDOUBLE = EventBinder(2000170)

EVT_TOGGLEBUTTON = EventBinder(2000171)

EVT_LIST_BEGIN_DRAG = EventBinder(2000172)
EVT_LIST_BEGIN_RDRAG = EventBinder(2000173)
EVT_LIST_BEGIN_LABEL_EDIT = EventBinder(2000174)
EVT_LIST_END_LABEL_EDIT = EventBinder(2000175)
EVT_LIST_DELETE_ITEM = EventBinder(2000176)
EVT_LIST_DELETE_ALL_ITEMS = EventBinder(2000177)
EVT_LIST_ITEM_SELECTED = EventBinder(2000178)
EVT_LIST_ITEM_DESELECTED = EventBinder(2000179)
EVT_LIST_KEY_DOWN = EventBinder(2000180)
EVT_LIST_INSERT_ITEM = EventBinder(2000181)
EVT_LIST_COL_CLICK = EventBinder(2000182)
EVT_LIST_ITEM_RIGHT_CLICK = EventBinder(2000183)
EVT_LIST_ITEM_MIDDLE_CLICK = EventBinder(2000184)
EVT_LIST_ITEM_ACTIVATED = EventBinder(2000185)
EVT_LIST_CACHE_HINT = EventBinder(2000186)
EVT_LIST_COL_RIGHT_CLICK = EventBinder(2000187)
EVT_LIST_COL_BEGIN_DRAG = EventBinder(2000188)
EVT_LIST_COL_DRAGGING = EventBinder(2000189)
EVT_LIST_COL_END_DRAG = EventBinder(2000190)
EVT_LIST_ITEM_FOCUSED = EventBinder(2000191)

EVT_TREE_BEGIN_DRAG = EventBinder(2000192)
EVT_TREE_BEGIN_RDRAG = EventBinder(2000193)
EVT_TREE_BEGIN_LABEL_EDIT = EventBinder(2000194)
EVT_TREE_END_LABEL_EDIT = EventBinder(2000195)
EVT_TREE_DELETE_ITEM = EventBinder(2000196)
EVT_TREE_GET_INFO = EventBinder(2000197)
EVT_TREE_SET_INFO = EventBinder(2000198)
EVT_TREE_ITEM_EXPANDED = EventBinder(2000199)
EVT_TREE_ITEM_EXPANDING = EventBinder(2000200)
EVT_TREE_ITEM_COLLAPSED = EventBinder(2000201)
EVT_TREE_ITEM_COLLAPSING = EventBinder(2000202)
EVT_TREE_SEL_CHANGED = EventBinder(2000203)
EVT_TREE_SEL_CHANGING = EventBinder(2000204)
EVT_TREE_KEY_DOWN = EventBinder(2000205)
EVT_TREE_ITEM_ACTIVATED = EventBinder(2000206)
EVT_TREE_ITEM_RIGHT_CLICK = EventBinder(2000207)
EVT_TREE_ITEM_MIDDLE_CLICK = EventBinder(2000208)
EVT_TREE_END_DRAG = EventBinder(2000209)
EVT_TREE_STATE_IMAGE_CLICK = EventBinder(2000210)
EVT_TREE_ITEM_GETTOOLTIP = EventBinder(2000211)
EVT_TREE_ITEM_MENU = EventBinder(2000212)

EVT_COLOURPICKER_CHANGED = EventBinder(2000213)

EVT_FILEPICKER_CHANGED = EventBinder(2000214)
EVT_DIRPICKER_CHANGED = EventBinder(2000215)

EVT_FONTPICKER_CHANGED = EventBinder(2000216)

EVT_FILECTRL_SELECTIONCHANGED = EventBinder(2000217)
EVT_FILECTRL_FILEACTIVATED = EventBinder(2000218)
EVT_FILECTRL_FOLDERCHANGED = EventBinder(2000219)
EVT_FILECTRL_FILTERCHANGED = EventBinder(2000220)

EVT_CHOICEBOOK_PAGE_CHANGED = EventBinder(2000221)
EVT_CHOICEBOOK_PAGE_CHANGING = EventBinder(2000222)

EVT_LISTBOOK_PAGE_CHANGED = EventBinder(2000223)
EVT_LISTBOOK_PAGE_CHANGING = EventBinder(2000224)

EVT_TOOLBOOK_PAGE_CHANGED = EventBinder(2000225)
EVT_TOOLBOOK_PAGE_CHANGING = EventBinder(2000226)

EVT_TREEBOOK_PAGE_CHANGED = EventBinder(2000227)
EVT_TREEBOOK_PAGE_CHANGING = EventBinder(2000228)
EVT_TREEBOOK_NODE_COLLAPSED = EventBinder(2000229)
EVT_TREEBOOK_NODE_EXPANDED = EventBinder(2000230)

EVT_DIRCTRL_SELECTIONCHANGED = EventBinder(2000231)
EVT_DIRCTRL_FILEACTIVATED = EventBinder(2000232)

EVT_FIND = EventBinder(2000233)
EVT_FIND_NEXT = EventBinder(2000234)
EVT_FIND_REPLACE = EventBinder(2000235)
EVT_FIND_REPLACE_ALL = EventBinder(2000236)
EVT_FIND_CLOSE = EventBinder(2000237)

EVT_POWER_SUSPENDING = EventBinder(2000238)
EVT_POWER_SUSPENDED = EventBinder(2000239)
EVT_POWER_SUSPEND_CANCEL = EventBinder(2000240)
EVT_POWER_RESUME = EventBinder(2000241)
EVT_END_PROCESS = EventBinder(2000242)
EVT_FSWATCHER = EventBinder(2000243)

EVT_CATEGORY_ALL = EventBinder(2000244)
EVT_CATEGORY_SOCKET = EventBinder(2000245)
EVT_CATEGORY_THREAD = EventBinder(2000246)
EVT_CATEGORY_TIMER = EventBinder(2000247)
EVT_CATEGORY_UI = EventBinder(2000248)
EVT_CATEGORY_USER_INPUT = EventBinder(2000249)
