def test_get_item_by_id(client):
    response = client.get("/items/11111111-1111-1111-1111-111111111111")

    assert response.status_code == 200
    assert response.json()["name"] == "Apples"
