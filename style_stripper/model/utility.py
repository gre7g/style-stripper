import wx


def add_stretcher(sizer: wx.Sizer):
    temp_sizer = wx.BoxSizer(wx.VERTICAL)
    temp_sizer.AddSpacer(10)
    sizer.Add(temp_sizer, 1, wx.TOP | wx.LEFT, 10)
