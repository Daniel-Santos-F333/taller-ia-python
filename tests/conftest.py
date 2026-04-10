import pytest
import os
import json
from run import create_app

@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    return app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def clean_data():
    """Fixture to clean JSON files before and after tests."""
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    files = ['computers.json', 'campers.json', 'assignments.json']
    backups = {}
    
    # Backup original data
    for file in files:
        path = os.path.join(data_dir, file)
        if os.path.exists(path):
            with open(path, 'r') as f:
                backups[file] = f.read()
        else:
            backups[file] = '[]'
    
    # Clean files
    for file in files:
        path = os.path.join(data_dir, file)
        with open(path, 'w') as f:
            f.write('[]')
    
    yield
    
    # Restore original data
    for file, content in backups.items():
        path = os.path.join(data_dir, file)
        with open(path, 'w') as f:
            f.write(content)