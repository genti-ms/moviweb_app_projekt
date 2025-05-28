import pytest
from app import app  # Deine Flask-App importieren

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"Welcome to MovieWeb App" in response.data

def test_list_users(client):
    response = client.get('/users')
    assert response.status_code == 200
    assert b"Users" in response.data or b"Username" in response.data  # Je nachdem wie dein users.html aussieht

def test_user_movies_page(client):
    # Beispiel: Prüfe, ob Seite für User mit ID 1 erreichbar ist
    response = client.get('/users/1')
    # 200 oder 404 ist möglich, falls User 1 nicht existiert. Teste nur Statuscode.
    assert response.status_code in [200, 404]

def test_add_movie_get(client):
    # Test GET-Methode zum Add Movie Formular für User 1
    response = client.get('/users/1/add_movie')
    assert response.status_code in [200, 404]

def test_add_movie_post(client):
    # Test POST-Methode: Filmeintrag hinzufügen für User 1 (ggf. User 1 existieren)
    response = client.post('/users/1/add_movie', data={
        'title': 'Inception',
        'director': 'Christopher Nolan',
        'year': '2010',
        'rating': '9'
    }, follow_redirects=True)
    # Prüfe, ob Weiterleitung funktioniert (200) oder User 1 nicht gefunden (404)
    assert response.status_code in [200, 404]
    if response.status_code == 200:
        assert b"Inception" in response.data

def test_update_movie_get(client):
    # Test GET-Formular zum Update eines Films (z.B. Movie 1 bei User 1)
    response = client.get('/users/1/update_movie/1')
    assert response.status_code in [200, 404]

def test_delete_movie(client):
    # Test Löschen eines Films (Movie 1 bei User 1)
    response = client.post('/users/1/delete_movie/1', follow_redirects=True)
    assert response.status_code in [200, 404]

def test_404_page(client):
    response = client.get('/users/99999999')  # nicht existierender User
    assert response.status_code == 404
    assert b"not found" in response.data.lower() or b"not found" in response.data
