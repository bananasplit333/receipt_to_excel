import pytest
import requests
from ..app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_shorten_url(client):
    # Test shortening a URL
    url = 'https://www.example.com'
    response = client.post('/shorten_link', data={'url': url})
    assert response.status_code == 200
    short_url = response.data.decode('utf-8')
    assert short_url.startswith(request.host_url)

def test_redirect_url(client):
    # Test redirecting a short URL
    url = 'https://www.example.com'
    response = client.post('/shorten_link', data={'url': url})
    short_url = response.data.decode('utf-8')
    short_code = short_url.replace(request.host_url, '')

    response = client.get(f'/{short_code}')
    assert response.status_code == 302
    assert response.headers['Location'] == url

def test_url_expiration(client):
    # Test URL expiration after maximum clicks
    url = 'https://www.example.com'
    response = client.post('/shorten_link', data={'url': url})
    short_url = response.data.decode('utf-8')
    short_code = short_url.replace(request.host_url, '')

    for _ in range(MAX_CLICKS):
        client.get(f'/{short_code}')

    response = client.get(f'/{short_code}')
    assert response.status_code == 404
    assert b'URL has expired' in response.data

def test_invalid_url(client):
    # Test accessing an invalid short URL
    response = client.get('/invalid')
    assert response.status_code == 404
    assert b'URL not found' in response.data