from django.http.response import HttpResponse, JsonResponse
from django.test import TestCase
from django.utils.encoding import force_str


class TaskViewTests(TestCase):
    def post_task(self, data, expected_status=200):
        url = "/tasks/"
        content_type = "application/json"
        response = self.client.post(url, data, content_type)
        self.assertIsInstance(response, HttpResponse)
        self.assertEqual(response.status_code, expected_status)
        return response

    def test_post_200(self):
        """
        POST 200
        """
        data = '{"task": "foo", "completed": false}'
        response = self.post_task(data)
        self.assertIsInstance(response, JsonResponse)
        expected = {"data": {"task": "foo", "completed": False, "id": 1}}
        self.assertJSONEqual(force_str(response.content), expected)

    def test_post_422(self):
        """
        POST 422
        """
        data = '{"bad": "foo", "completed": "wrong"}'
        self.post_task(data, expected_status=422)

    def test_get_200(self):
        """
        GET 200
        """
        data = '{"task": "foo", "completed": false}'
        response = self.post_task(data)
        data = '{"task": "bar", "completed": false}'
        response = self.post_task(data)
        url = "/tasks/"
        response = self.client.get(url)
        self.assertIsInstance(response, JsonResponse)
        expected = {
            "data": [
                {"task": "foo", "completed": False, "id": 1},
                {"task": "bar", "completed": False, "id": 2},
            ]
        }
        self.assertJSONEqual(force_str(response.content), expected)


class TaskDetailViewTests(TestCase):
    def post_task(self, data, expected_status=200):
        url = "/tasks/"
        content_type = "application/json"
        response = self.client.post(url, data, content_type)
        self.assertEqual(response.status_code, expected_status)
        self.assertIsInstance(response, JsonResponse)
        body = response.json()
        self.assertTrue("data" in body)
        self.assertTrue("id" in body["data"])
        return body["data"]["id"]

    def test_get_200(self):
        """
        GET 200
        """
        data = '{"task": "foo", "completed": false}'
        pid = self.post_task(data)
        url = f"/tasks/{pid}/"
        response = self.client.get(url)
        print("---------response",response)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response, JsonResponse)
        expected = {"data": {"task": "foo", "completed": False, "id": 1}}
        self.assertJSONEqual(force_str(response.content), expected)

    def test_get_404(self):
        """
        GET 404
        """
        url = "/tasks/42/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_delete_200(self):
        """
        DELETE 200
        """
        data = '{"task": "foo", "completed": false}'
        pid = self.post_task(data)
        url = f"/tasks/{pid}/"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 200)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_delete_404(self):
        """
        DELETE 404
        """
        url = "/tasks/42/"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 404)

    def test_put_200(self):
        """
        PUT 200
        """
        data = '{"task": "foo", "completed": false}'
        pid = self.post_task(data)
        url = f"/tasks/{pid}/"
        data = '{"task": "bar", "completed": true}'
        response = self.client.put(url, data)
        print("============++++++++++++response",response)
        self.assertEqual(response.status_code, 200)
        response = self.client.get(url)
        self.assertIsInstance(response, JsonResponse)
        expected = {"data": {"task": "bar", "completed": True, "id": 1}}
        self.assertJSONEqual(force_str(response.content), expected)

    def test_put_404(self):
        """
        PUT 404
        """
        url = "/tasks/42/"
        response = self.client.put(url)
        self.assertEqual(response.status_code, 404)
