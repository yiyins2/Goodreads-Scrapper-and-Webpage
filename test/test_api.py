import pytest
import requests

url = 'http://localhost:5000/'


class TestAPI():
    def test_get_book_id_negative(self):
        r = requests.get(url + '/book?id=-1')
        assert r.status_code == 400

    def test_get_book_id_nonint(self):
        r = requests.get(url + '/book?id=xx')
        assert r.status_code == 400

    def test_get_book_id(self):
        r = requests.get(url + '/book?id=1')
        data = r.json()
        assert data['book_id'] == 1

    def test_search(self):
        r = requests.get(url + '/search?q=book.book_id:1')
        data = r.json()[0]
        assert data['book_id'] == 1

    def test_search_invalid_query(self):
        r = requests.get(url + '/search?q=x.xxx:1')
        assert r.status_code == 400

    def test_put_book_id(self):
        rp = requests.put(url + '/book?id=1', json={"ISBN": 10})
        assert rp.text == "Successfully updated document with book id: 1"

    def test_delete(self):
        rp = requests.delete(url + '/book?id=8')
        assert rp.status_code == 400
