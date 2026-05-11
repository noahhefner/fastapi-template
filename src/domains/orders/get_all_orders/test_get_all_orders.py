def test_get_all_orders(client):
    response = client.get("/orders/")

    assert response.status_code == 200
    assert len(response.json()) == 3
