from django.test import TestCase


class StudentsApiTests(TestCase):
    def test_list_returns_json(self):
        response = self.client.get("/api/students/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"items": [
            {"id": 1, "name": "Ana Popescu", "year": 3},
            {"id": 2, "name": "Radu Ionescu", "year": 3},
        ]})

    def test_detail_returns_student(self):
        response = self.client.get("/api/students/2/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "id": 2, "name": "Radu Ionescu", "year": 3,
        })

    def test_missing_student_returns_404(self):
        response = self.client.get("/api/students/999/")
        self.assertEqual(response.status_code, 404)

    def test_health_returns_ok(self):
        response = self.client.get("/api/health/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok"})

    def test_list_rejects_post(self):
        response = self.client.post("/api/students/")
        self.assertEqual(response.status_code, 405)
