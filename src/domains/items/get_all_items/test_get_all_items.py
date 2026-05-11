def test_get_all_items(client):

    response = client.get("/items/")

    assert response.status_code == 200
    assert len(response.json()) == 3
