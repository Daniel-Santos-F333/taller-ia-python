import pytest
import json
import os

def test_complete_flow(client, clean_data):
    """Test complete flow: add computer, add camper, assign, return."""
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    
    # Add computer
    client.post('/computers', data={'serial': 'FLOW-001', 'brand': 'FlowBrand', 'model': 'FlowModel'}, follow_redirects=True)
    
    # Add camper
    client.post('/campers', data={'id_camper': '67890', 'name': 'Flow Camper', 'email': 'flow@example.com'}, follow_redirects=True)
    
    # Get IDs
    with open(os.path.join(data_dir, 'computers.json'), 'r') as f:
        computers = json.load(f)
        computer_id = computers[0]['id']
    
    # Assign
    client.post('/assign', data={'camper_id': '67890', 'computer_id': computer_id}, follow_redirects=True)
    
    # Check assignment
    with open(os.path.join(data_dir, 'computers.json'), 'r') as f:
        computers = json.load(f)
        assert computers[0]['status'] == 'asignado'
    
    # Return
    client.get(f'/return/{computer_id}', follow_redirects=True)
    
    # Check return
    with open(os.path.join(data_dir, 'computers.json'), 'r') as f:
        computers = json.load(f)
        assert computers[0]['status'] == 'disponible'
    
    with open(os.path.join(data_dir, 'assignments.json'), 'r') as f:
        assignments = json.load(f)
        assert assignments[0]['return_date'] is not None

def test_multiple_assignments(client, clean_data):
    """Test multiple computers and assignments."""
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    
    # Add multiple computers
    for i in range(3):
        client.post('/computers', data={'serial': f'MULTI-{i}', 'brand': 'Multi', 'model': f'Model{i}'}, follow_redirects=True)
    
    # Add multiple campers
    for i in range(2):
        client.post('/campers', data={'id_camper': f'ID{i}', 'name': f'Camper{i}', 'email': f'camper{i}@example.com'}, follow_redirects=True)
    
    # Get computer IDs
    with open(os.path.join(data_dir, 'computers.json'), 'r') as f:
        computers = json.load(f)
        computer_ids = [c['id'] for c in computers]
    
    # Assign first two
    client.post('/assign', data={'camper_id': 'ID0', 'computer_id': computer_ids[0]}, follow_redirects=True)
    client.post('/assign', data={'camper_id': 'ID1', 'computer_id': computer_ids[1]}, follow_redirects=True)
    
    # Try to assign already assigned (should fail)
    response = client.post('/assign', data={'camper_id': 'ID0', 'computer_id': computer_ids[0]}, follow_redirects=True)
    assert response.status_code == 200  # But check flash message in real app
    
    # Check assignments
    with open(os.path.join(data_dir, 'assignments.json'), 'r') as f:
        assignments = json.load(f)
        assert len(assignments) == 2