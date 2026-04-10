import pytest

def test_index_page(client):
    """Test the main index page loads correctly."""
    response = client.get('/')
    assert response.status_code == 200
    assert b'index.html' in response.data or 'Dashboard' in response.data.decode('utf-8')

def test_computers_page(client):
    """Test the computers management page."""
    response = client.get('/computers')
    assert response.status_code == 200
    assert b'Equipos Registrados' in response.data or 'Computadoras' in response.data.decode('utf-8')

def test_campers_page(client):
    """Test the campers management page."""
    response = client.get('/campers')
    assert response.status_code == 200
    assert b'campers.html' in response.data or 'Campers' in response.data.decode('utf-8')

def test_history_page(client):
    """Test the history page."""
    response = client.get('/history')
    assert response.status_code == 200
    assert b'history.html' in response.data or 'Historial' in response.data.decode('utf-8')

def test_404_page(client):
    """Test 404 error page."""
    response = client.get('/nonexistent')
    assert response.status_code == 404
    assert b'404.html' in response.data or '404' in response.data.decode('utf-8')