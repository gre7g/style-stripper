import logging
import wx

from style_stripper.model.content_pane import ContentPanel
from style_stripper.model.utility import add_stretcher

# Constants:
LOG = logging.getLogger(__name__)
_ = wx.GetTranslation


class DonePanel(ContentPanel):
    def __init__(self, *args, **kwargs):
        super(DonePanel, self).__init__(*args, **kwargs)

        sizer1 = wx.BoxSizer(wx.VERTICAL)
        text = wx.StaticText(
            self,
            label=_(
                'Processing complete! Click the "Export..." button below to save the .docx'
            ),
        )
        sizer1.Add(text, 0, 0, 0)
        button = wx.Button(self, label=_("Export..."))
        button.Bind(wx.EVT_BUTTON, self.app.frame_controls.on_export)
        sizer1.Add(button, 0, wx.TOP, 10)

        add_stretcher(sizer1)
        button = wx.Button(self, label=_("Previous"))
        button.Bind(wx.EVT_BUTTON, self.app.frame_controls.on_reload)
        sizer1.Add(button, 0, 0, 0)

        self.SetSizer(sizer1)

    def apply(self):
        # Questionable cases are cases where we cannot blindly guess how the quotes should look. We have to present
        # options to the user and apply them as instructed.
        for question in self.app.frame.review_panel.questionable:
            question.apply()
