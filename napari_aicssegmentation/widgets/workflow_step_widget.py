from typing import List

from aicssegmentation.workflow import WorkflowStep
from aicssegmentation.workflow.segmenter_function import FunctionParameter, WidgetType
from magicgui.widgets import FloatSlider, Slider
from qtpy.QtWidgets import QLabel, QVBoxLayout, QWidget

from napari_aicssegmentation.widgets.collapsible_box import CollapsibleBox
from napari_aicssegmentation.widgets.form import Form, FormRow
from napari_aicssegmentation.util.ui_utils import UiUtils


class WorkflowStepWidget(QWidget):
    """
    A widget wrapping a CollapsibleBox that contains all the parameter controls and other
    necessary child widgets for a given WorkflowStep

    Params:
        step (WorkflowStep): WorkflowStep object for this widget
    """

    def __init__(self, step: WorkflowStep):
        super().__init__()
        self.form_rows = []

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        if step.function.parameters is None:
            self.form_rows.append(FormRow("", QLabel("No parameters needed")))
        else:
            # Get all the separate parameters to put into this layout
            for param_label, param_data in step.function.parameters.items():
                default_values = step.parameter_defaults[param_label]
                self.add_param_widgets(param_label, param_data, default_values)

        step_name = f"<span>{step.step_number}.&nbsp;{step.name}</span>"
        layout.addWidget(CollapsibleBox(step_name, Form(self.form_rows, (11, 5, 5, 5))))

    def add_param_widgets(self, param_label: str, param_data: List[FunctionParameter], default_values: List):
        # Prepare to append a number to the label if multiple parameter widgets
        # share the same label
        param_label_numbered = param_label
        is_label_numbered = False
        if len(param_data) > 1:
            is_label_numbered = True

        for i, param in enumerate(param_data):
            if is_label_numbered:
                param_label_numbered = f"{param_label} {i + 1}"

            if param.widget_type == WidgetType.SLIDER:
                self.add_slider(param_label_numbered, param, default_values[i])
            elif param.widget_type == WidgetType.DROPDOWN:
                self.add_dropdown(param_label_numbered, param, default_values[i])

    def add_slider(self, param_label, param, default_value):
        # NOTE: This is on Jianxu's radar to fix
        # Sometimes default values are less than min or greater than max
        if default_value < param.min_value:
            default_value = param.min_value
        elif default_value > param.max_value:
            default_value = param.max_value

        # Build dictionary of keyword args for slider widgets
        kwargs = dict()
        kwargs["step"] = param.increment
        kwargs["max"] = param.max_value
        kwargs["min"] = param.min_value
        kwargs["value"] = default_value

        # Determine which type of slider to use based on data type
        # and unpack dictionary with slider info and feed when initializing
        widget = None
        if param.data_type == "float":
            widget = FloatSlider(**kwargs).native
        if param.data_type == "int":
            widget = Slider(**kwargs).native
        widget.setObjectName("slider")

        self.form_rows.append(FormRow(param_label, widget))

    def add_dropdown(self, param_label, param, default_value):
        dropdown_row = UiUtils.dropdown_row(
            param_label, default=default_value, options=param.options, enabled=True
        )
        self.form_rows.append(dropdown_row)
