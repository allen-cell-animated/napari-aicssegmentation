import pytest

from PyQt5.QtWidgets import QFrame
from napari_aicssegmentation.core.view import View, ViewTemplate

class FakeTemplate(ViewTemplate):
    def setup_ui(self):
        pass

    def get_container(self) -> QFrame:
        return QFrame()

class FakeView(View):
    def setup_ui(self):
        pass

class TestView:
    def test_init_throws_with_bad_template(self):
        with pytest.raises(TypeError):
            FakeView(template_class=object)

    def test_template(self):
        view = FakeView(template_class=FakeTemplate)
        assert view.template is not None
        assert view.has_template()
        assert isinstance(view.template, FakeTemplate)

    def test_no_template(self):
        view = FakeView()
        assert view.template is None
        assert not view.has_template()
