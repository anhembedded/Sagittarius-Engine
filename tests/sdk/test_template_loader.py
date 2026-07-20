import pytest
from sagittarius_engine.sdk.template_loader import TemplateLoader
from sagittarius_engine.exceptions import PathTraversalError

def test_template_loader__get_template_path__path_traversal_raises_error():
    loader = TemplateLoader()
    with pytest.raises(PathTraversalError):
        loader.get_template_path("../../../../etc")

def test_template_loader__get_template_path__valid_path_raises_not_found_if_does_not_exist():
    loader = TemplateLoader()
    with pytest.raises(ValueError, match="Template 'some_template' not found."):
        loader.get_template_path("some_template")
