import pytest
import json
import os

def test_add_computer(client, clean_data):
    """Test adding a new computer."""
    data = {
        'serial': 'TEST-001',
        'brand': 'TestBrand',
        'model': 'TestModel'
    }
    response = client.post('/computers', data=data, follow_redirects=True)
    assert response.status_code == 200
    
    # Check if computer was added to JSON
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    with open(os.path.join(data_dir, 'computers.json'), 'r') as f:
        computers = json.load(f)
        assert len(computers) == 1
        assert computers[0]['serial'] == 'TEST-001'
        assert computers[0]['status'] == 'disponible'

def test_add_camper(client, clean_data):
    """Test adding a new camper."""
    data = {
        'id_camper': '12345',
        'name': 'Test Camper',
        'email': 'test@example.com'
    }
    response = client.post('/campers', data=data, follow_redirects=True)
    assert response.status_code == 200
    
    # Check if camper was added to JSON
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    with open(os.path.join(data_dir, 'campers.json'), 'r') as f:
        campers = json.load(f)
        assert len(campers) == 1
        assert campers[0]['id'] == '12345'
        assert campers[0]['name'] == 'Test Camper'

def test_assign_computer(client, clean_data):
    """Test assigning a computer to a camper."""
    # First add computer and camper
    client.post('/computers', data={'serial': 'TEST-001', 'brand': 'Test', 'model': 'Model'}, follow_redirects=True)
    client.post('/campers', data={'id_camper': '12345', 'name': 'Test', 'email': 'test@example.com'}, follow_redirects=True)
    
    # Get computer ID
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    with open(os.path.join(data_dir, 'computers.json'), 'r') as f:
        computers = json.load(f)
        computer_id = computers[0]['id']
    
    # Assign
    data = {
        'camper_id': '12345',
        'computer_id': computer_id
    }
    response = client.post('/assign', data=data, follow_redirects=True)
    assert response.status_code == 200
    
    # Check assignment
    with open(os.path.join(data_dir, 'assignments.json'), 'r') as f:
        assignments = json.load(f)
        assert len(assignments) == 1
        assert assignments[0]['camper_id'] == '12345'
        assert assignments[0]['computer_id'] == computer_id

def test_return_computer(client, clean_data):
    """Test returning a computer."""
    # Setup: add and assign
    client.post('/computers', data={'serial': 'TEST-001', 'brand': 'Test', 'model': 'Model'}, follow_redirects=True)
    client.post('/campers', data={'id_camper': '12345', 'name': 'Test', 'email': 'test@example.com'}, follow_redirects=True)
    
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    with open(os.path.join(data_dir, 'computers.json'), 'r') as f:
        computers = json.load(f)
        computer_id = computers[0]['id']
    
    client.post('/assign', data={'camper_id': '12345', 'computer_id': computer_id}, follow_redirects=True)
    
    # Return
    response = client.get(f'/return/{computer_id}', follow_redirects=True)
    assert response.status_code == 200
    
    # Check status
    with open(os.path.join(data_dir, 'computers.json'), 'r') as f:
        computers = json.load(f)
        assert computers[0]['status'] == 'disponible'