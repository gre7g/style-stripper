import builtins
from six import text_type as unicode
from typing import Callable, Mapping, Sequence, Optional, Tuple, Union
import wx
from wx.lib.masked.maskededit import Field, MaskedEditMixin

Text = Union[unicode, str]

if not hasattr(builtins, "long"):
    long = int

class BaseMaskedTextCtrl(wx.TextCtrl, MaskedEditMixin):
    pass
    # ChangeValue	Provided to accomodate similar functionality added to base
    # Clear	Blanks the current control value by replacing it with the default value.
    # Cut	This function redefines the externally accessible TextCtrl.Cut
    # IsEmpty
    # IsModified	This function overrides the raw TextCtrl.IsModified method,
    # ModifyValue	This factored function of common code does the bulk of the work for
    # Paste	This function redefines the externally accessible TextCtrl.Paste
    # Refresh	This function redefines the externally accessible TextCtrl.Refresh
    # SetFont	Set the font, then recalculate control size, if appropriate.
    # SetValue	This function redefines the externally accessible TextCtrl.SetValue
    # Undo	This function defines the undo operation for the control.

class MaskedEditAccessorsMixin(object):
    pass

class TextCtrl(BaseMaskedTextCtrl, MaskedEditAccessorsMixin):
    def __init__(
        self,
        parent: wx.Window,
        id: int = ...,
        value: Text = ...,
        pos: wx.Point = ...,
        size: wx.Size = ...,
        style: long = ...,
        validator: wx.Validator = ...,
        name: Text = ...,
        setupEventHandling: bool = ...,
        *,  # everything below this point is a named arg
        # MaskedEditMixin params:
        # mask : Text = ..., # duplicated in FIeld params below
        autoformat: Text = ...,
        fields: Union[Sequence[Field], Mapping[int, Field]] = ...,
        datestyle: Text = ...,
        autoCompleteKeycodes: Sequence[wx.KeyCode] = ...,
        useFixedWidthFont: bool = ...,
        defaultEncoding: Text = ...,
        retainFieldValidation: bool = ...,
        emptyBackgroundColor: Text = ...,
        validBackgroundColor: Text = ...,
        invalidBackgroundColor: Text = ...,
        foregroundColour: Text = ...,
        signedForegroundColour: Text = ...,
        demo: bool = ...,
        # Field params:
        mask: Text = ...,
        formatcodes: Text = ...,
        fillChar: Text = ...,
        groupChar: Text = ...,
        decimalChar: Text = ...,
        shiftDecimalChar: Text = ...,
        useParensForNegatives: bool = ...,
        defaultValue: Text = ...,
        excludeChars: Text = ...,
        includeChars: Text = ...,
        validRegex: Text = ...,
        validRange: Optional[Tuple[int, int]] = ...,
        choices: Sequence[Text] = ...,
        choiceRequired: bool = ...,
        compareNoCase: bool = ...,
        autoSelect: bool = ...,
        validFunc: Optional[Callable[[Text], bool]] = ...,
        validRequired: bool = ...,
        emptyInvalid: bool = ...,
        description: Text = ...,
        raiseOnInvalidPaste: bool = ...,
        stopFieldChangeIfInvalid: bool = ...,
    ) -> None: ...
