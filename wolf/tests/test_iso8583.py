
def test_iso8583_server(run_iso8583_server):
    url = run_iso8583_server()
    response = requests.get(url)
    assert response.status_code == 200

