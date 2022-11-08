from six import text_type as unicode
from typing import Callable, Sequence, Optional, Tuple, Union
import wx

Text = Union[unicode, str]

class Field(object):
    def __init__(
        self,
        *,
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

class MaskedEditMixin(object):
    pass
    # ClearValue	Blanks the current control value by replacing it with the default value.
    # ClearValueAlt	Blanks the current control value by replacing it with the default value.
    # GetCtrlParameter	Routine for retrieving the value of any given parameter
    # GetFieldParameter	Routine provided for getting a parameter of an individual field.
    # GetMaskParameter	old name for the GetCtrlParameters function (DEPRECATED)
    # GetPlainValue	Returns control's value stripped of the template text.
    # IsDefault	Returns True if the value specified (or the value of the control if not specified)
    # IsEmpty	Returns True if control is equal to an empty value.
    # IsValid	Indicates whether the value specified (or the current value of the control
    # SetBackgroundColour
    # SetCtrlParameters	This public function can be used to set individual or multiple masked edit
    # SetFieldParameters	Routine provided to modify the parameters of a given field.
    # SetForegroundColour
    # SetMaskParameters	old name for the SetCtrlParameters function (DEPRECATED)
