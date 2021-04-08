from magicgui.widgets import FloatSlider
from qtpy.QtWidgets import (
    QHBoxLayout,
    QLabel, 
    QLayout, 
    QProgressBar,
    QPushButton, 
    QVBoxLayout, 
    QWidget
)

from napari_aicssegmentation.model.segmenter_model import SegmenterModel
from napari_aicssegmentation.util.debug_utils import debug_class
from napari_aicssegmentation.controller._interfaces import IWorkflowStepsController
from napari_aicssegmentation.core.view import View
from napari_aicssegmentation.widgets.collapsible_box import CollapsibleBox
from napari_aicssegmentation.widgets.form import Form, FormRow
from napari_aicssegmentation.view._main_template import MainTemplate
from napari_aicssegmentation._style import PAGE_CONTENT_WIDTH


@debug_class
class WorkflowStepsView(View):  # pragma: no-cover
    # _lbl_selected_workflow: QLabel

    def __init__(self, controller: IWorkflowStepsController):
        super().__init__(template_class=MainTemplate)

        if controller is None:
            raise ValueError("controller")
        self._controller = controller

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.setLayout(layout)

        # self._lbl_selected_workflow = QLabel()

        btn_run_all = QPushButton("Run all")
        btn_run_all.clicked.connect(self._btn_back_clicked)

        # Add all widgets
        self._add_workflow_title(layout)
        self._add_progress_bar(layout)
        self._add_workflow_steps(layout, "preprocessing")
        self._add_workflow_steps(layout, "core")
        self._add_workflow_steps(layout, "postprocessing")
        layout.addStretch()
        layout.addWidget(btn_run_all)

    def load_model(self, model: SegmenterModel):
        pass
        # self._lbl_selected_workflow.setText(f"Selected workflow: {model.active_workflow}")
        # self._lbl_selected_workflow.repaint()

    def _btn_back_clicked(self, checked: bool):
        self._controller.navigate_back()

    def _add_workflow_title(self, layout: QLayout):
        widget = QWidget()
        title_layout = QHBoxLayout()
        widget.setLayout(title_layout)

        # To be replaced by data
        config_workflow_name = "sec61b"
        workflow_name = QLabel(f"Workflow: {config_workflow_name}")
        info = QLabel("ⓘ")

        title_layout.addStretch()
        title_layout.addWidget(workflow_name)
        title_layout.addWidget(info)
        title_layout.addStretch()
        title_layout.setSpacing(5)

        widget.setObjectName("workflowTitle")
        layout.addWidget(widget)
    
    def _add_progress_bar(self, layout: QLayout):
        # To be replaced by data
        num_steps = 4

        # Progress bar
        progress_bar = QProgressBar()
        progress_bar.setRange(0, num_steps)
        progress_bar.setValue(3) # TODO: Change arg to 0
        progress_bar.setTextVisible(False)
        layout.addWidget(progress_bar)

        # Tick marks
        progress_labels = QLabel()
        progress_labels.setFixedWidth(PAGE_CONTENT_WIDTH)
        progress_labels.setObjectName("progressLabels")

        labels_layout = QHBoxLayout()
        labels_layout.setContentsMargins(5, 0, 5, 11)
        progress_labels.setLayout(labels_layout)

        for step in range(0, num_steps + 1):
            tick = QLabel("|")
            labels_layout.addWidget(tick)
            if step < num_steps:
                labels_layout.addStretch()
        layout.addWidget(progress_labels)

    def _add_workflow_steps(self, layout: QLayout, category: str):
        # To be replaced by data
        steps = [
            {   
                "number": 1,
                "name": "Intensity Normalization",
            },
            {
                "number": 2,
                "name": "Edge Preserving Smoothing",
            },
        ]
        
        category_label = QLabel(category.upper())
        category_label.setObjectName("categoryLabel")
        layout.addWidget(category_label)

        for i, step in enumerate(steps):
            row_1 = FormRow("Param 1", FloatSlider(value=2.5, min=0.5, max=30, step=0.5).native)
            row_2 = FormRow("Param 2", FloatSlider(value=7.5, min=0.5, max=200, step=0.5).native)
            content = Form([row_1, row_2])

            layout.addWidget(CollapsibleBox(f"<span>{i + 1}.&nbsp;{step['name']}", content))
        
        layout.addSpacing(10)
