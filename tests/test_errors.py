import pytest
import json
import os

def test_assign_unavailable_computer(client, clean_data):
    """Test assigning an already assigned computer."""
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    
    # Setup
    client.post('/computers', data={'serial': 'ERR-001', 'brand': 'Err', 'model': 'Model'}, follow_redirects=True)
    client.post('/campers', data={'id_camper': 'ERR1', 'name': 'Err Camper1', 'email': 'err1@example.com'}, follow_redirects=True)
    client.post('/campers', data={'id_camper': 'ERR2', 'name': 'Err Camper2', 'email': 'err2@example.com'}, follow_redirects=True)
    
    with open(os.path.join(data_dir, 'computers.json'), 'r') as f:
        computers = json.load(f)
        computer_id = computers[0]['id']
    
    # First assignment
    client.post('/assign', data={'camper_id': 'ERR1', 'computer_id': computer_id}, follow_redirects=True)
    
    # Second assignment (should fail)
    response = client.post('/assign', data={'camper_id': 'ERR2', 'computer_id': computer_id}, follow_redirects=True)
    assert response.status_code == 200  # Redirects to index
    
    # Check only one assignment
    with open(os.path.join(data_dir, 'assignments.json'), 'r') as f:
        assignments = json.load(f)
        assert len(assignments) == 1

def test_assign_nonexistent_computer(client, clean_data):
    """Test assigning a non-existent computer."""
    client.post('/campers', data={'id_camper': 'ERR1', 'name': 'Err Camper', 'email': 'err@example.com'}, follow_redirects=True)
    
    response = client.post('/assign', data={'camper_id': 'ERR1', 'computer_id': 'nonexistent'}, follow_redirects=True)
    assert response.status_code == 200
    
    # Check no assignment created
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    with open(os.path.join(data_dir, 'assignments.json'), 'r') as f:
        assignments = json.load(f)
        assert len(assignments) == 0

def test_corrupt_json_handling(client, clean_data):
    """Test handling of corrupt JSON files."""
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    
    # Corrupt computers.json
    with open(os.path.join(data_dir, 'computers.json'), 'w') as f:
        f.write('invalid json')
    
    # Try to access pages that read JSON
    response = client.get('/')
    assert response.status_code == 200  # Should handle gracefully
    
    response = client.get('/computers')
    assert response.status_code == 200

def test_empty_form_submission(client, clean_data):
    """Test submitting empty forms."""
    # Empty computer form
    response = client.post('/computers', data={}, follow_redirects=True)
    assert response.status_code == 200
    
    # Empty camper form
    response = client.post('/campers', data={}, follow_redirects=True)
    assert response.status_code == 200
    
    # Check no data added
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    with open(os.path.join(data_dir, 'computers.json'), 'r') as f:
        computers = json.load(f)
        assert len(computers) == 0
    
    with open(os.path.join(data_dir, 'campers.json'), 'r') as f:
        campers = json.load(f)
        assert len(campers) == 0