import pytest
from pathlib import Path
import tempfile
from math_explorations.export import (
    extract_metadata,
    _infer_tags,
    NotebookMetadata
)

def test_infer_tags():
    content = "This notebook discusses derivatives and integrals."
    tags = _infer_tags(content, "001_test")
    assert "Derivatives" in tags
    assert "Integration" in tags
    
    content = "Just some text."
    tags = _infer_tags(content, "001_test")
    assert tags == ["Mathematics"]

def test_extract_metadata():
    content = '''"""
Title: Test Notebook
Description: This is a test description.
"""
import marimo as mo
mo.md(r"""# My Real Title""")
'''
    with tempfile.NamedTemporaryFile(suffix=".py", mode="w", delete=False) as tmp:
        tmp.write(content)
        tmp_path = Path(tmp.name)
    
    try:
        # Mocking the filename as 001_test.py for extraction
        test_path = tmp_path.parent / "001_test.py"
        tmp_path.rename(test_path)
        
        meta = extract_metadata(test_path)
        assert meta.number == "001"
        assert meta.title == "My Real Title"
        assert "This is a test description" in meta.description
        assert "Mathematics" in meta.tags
    finally:
        if test_path.exists():
            test_path.unlink()

def test_extract_metadata_fallback():
    content = 'import marimo as mo'
    with tempfile.NamedTemporaryFile(suffix=".py", mode="w", delete=False) as tmp:
        tmp.write(content)
        tmp_path = Path(tmp.name)
    
    try:
        test_path = tmp_path.parent / "999_fallback_test.py"
        tmp_path.rename(test_path)
        
        meta = extract_metadata(test_path)
        assert meta.number == "999"
        assert meta.title == "Fallback Test"
        assert "interactive exploration of fallback test" in meta.description.lower()
    finally:
        if test_path.exists():
            test_path.unlink()
