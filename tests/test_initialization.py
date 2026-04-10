import pytest
import os

def test_app_creation(app):
    """Test that the Flask app is created successfully."""
    assert app is not None
    assert app.config['TESTING'] is True

def test_data_files_exist():
    """Test that data JSON files exist."""
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    files = ['computers.json', 'campers.json', 'assignments.json']
    for file in files:
        path = os.path.join(data_dir, file)
        assert os.path.exists(path), f"{file} does not exist"

def test_data_files_are_valid_json(clean_data):
    """Test that data files contain valid JSON."""
    import json
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    files = ['computers.json', 'campers.json', 'assignments.json']
    for file in files:
        path = os.path.join(data_dir, file)
        with open(path, 'r') as f:
            content = f.read()
            try:
                json.loads(content)
            except json.JSONDecodeError:
                pytest.fail(f"{file} contains invalid JSON")