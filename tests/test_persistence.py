import pytest
import json
import os

def test_data_persistence_across_requests(client, clean_data):
    """Test that data persists across multiple requests."""
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    
    # Add data
    client.post('/computers', data={'serial': 'PERSIST-001', 'brand': 'Persist', 'model': 'Model'}, follow_redirects=True)
    client.post('/campers', data={'id_camper': 'PERSIST1', 'name': 'Persist Camper', 'email': 'persist@example.com'}, follow_redirects=True)
    
    # Check data is there
    with open(os.path.join(data_dir, 'computers.json'), 'r') as f:
        computers = json.load(f)
        assert len(computers) == 1
    
    with open(os.path.join(data_dir, 'campers.json'), 'r') as f:
        campers = json.load(f)
        assert len(campers) == 1
    
    # Simulate app restart by creating new client (in real test, restart server)
    # For now, just check data is still there after more requests
    client.get('/')  # Another request
    
    with open(os.path.join(data_dir, 'computers.json'), 'r') as f:
        computers = json.load(f)
        assert len(computers) == 1

def test_json_format_validity(client, clean_data):
    """Test that JSON files remain valid after operations."""
    import json
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    
    # Perform operations
    client.post('/computers', data={'serial': 'FORMAT-001', 'brand': 'Format', 'model': 'Model'}, follow_redirects=True)
    client.post('/campers', data={'id_camper': 'FORMAT1', 'name': 'Format Camper', 'email': 'format@example.com'}, follow_redirects=True)
    
    with open(os.path.join(data_dir, 'computers.json'), 'r') as f:
        computers = json.load(f)
        assert len(computers) == 1
        # Check it's properly formatted
        assert isinstance(computers, list)
        assert 'id' in computers[0]
        assert 'status' in computers[0]

def test_no_duplicate_data(client, clean_data):
    """Test that operations don't create duplicate entries."""
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    
    # Add same computer multiple times (should create different IDs)
    for i in range(3):
        client.post('/computers', data={'serial': f'DUP-{i}', 'brand': 'Dup', 'model': 'Model'}, follow_redirects=True)
    
    with open(os.path.join(data_dir, 'computers.json'), 'r') as f:
        computers = json.load(f)
        assert len(computers) == 3
        ids = [c['id'] for c in computers]
        assert len(set(ids)) == 3  # All IDs unique

def test_data_integrity_after_operations(client, clean_data):
    """Test data integrity after complex operations."""
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    
    # Add computer and camper
    client.post('/computers', data={'serial': 'INTEGRITY-001', 'brand': 'Integrity', 'model': 'Model'}, follow_redirects=True)
    client.post('/campers', data={'id_camper': 'INT1', 'name': 'Integrity Camper', 'email': 'integrity@example.com'}, follow_redirects=True)
    
    with open(os.path.join(data_dir, 'computers.json'), 'r') as f:
        computers = json.load(f)
        computer_id = computers[0]['id']
    
    # Assign
    client.post('/assign', data={'camper_id': 'INT1', 'computer_id': computer_id}, follow_redirects=True)
    
    # Return
    client.get(f'/return/{computer_id}', follow_redirects=True)
    
    # Check all files are valid
    files = ['computers.json', 'campers.json', 'assignments.json']
    for file in files:
        with open(os.path.join(data_dir, file), 'r') as f:
            data = json.load(f)
            assert isinstance(data, list)