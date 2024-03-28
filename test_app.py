import os
import pytest
from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_index(client):
    response = client.get('/')
    assert response.status_code == 200

# def test_upload(client):
#     with open('test_image.png', 'rb') as f:
#         data = {'image': (f, 'test_image.png')}
#         response = client.post('/upload', data=data, content_type='multipart/form-data')
#         assert response.status_code == 200

# def test_display_responses(client):
#     # Test displaying responses for an uploaded image
#     response = client.get('/display-responses/test_image.png')
#     assert response.status_code == 200
#     assert b'Metadata for Uploaded Image' in response.data
#     assert b'Filename:' in response.data
