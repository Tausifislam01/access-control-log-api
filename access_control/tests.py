from django.test import TestCase
from rest_framework.test import APIClient



class AccessLogApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    
    def test_create_access_log(self):
        response = self.client.post(
            "/api/logs/",
            {"card_id": "C1001", "door_name": "Main Entrance", "access_granted": True},
            format="json",
        )
        self.assertEqual(response.status_code, 201)
        self.assertIn("id", response.data)
        self.assertEqual(response.data["card_id"], "C1001")
        self.assertIn("timestamp", response.data)

    
    def test_list_access_logs_includes_created_log(self):
        create_access_log_response = self.client.post(
            "/api/logs/",
             {"card_id": "C2001", "door_name": "Side Entrance", "access_granted": False},
            format="json",
            )
        
        created_log_id = create_access_log_response.data["id"]
        list_access_logs_response = self.client.get("/api/logs/")

        self.assertEqual(list_access_logs_response.status_code, 200)
        self.assertTrue(
            any(item["id"] == created_log_id for item in list_access_logs_response.data)
        )



    def test_retrieve_access_log_returns_correct_data(self):
        create_access_log_response = self.client.post(
            "/api/logs/",
            {"card_id": "C3001", "door_name": "Server Room", "access_granted": True},
            format="json",
        )

        created_log_id = create_access_log_response.data["id"]
        retrieve_access_log_response = self.client.get(
            f"/api/logs/{created_log_id}/"
        )

        self.assertEqual(retrieve_access_log_response.status_code, 200)
        self.assertEqual(
            retrieve_access_log_response.data["card_id"], "C3001"
        )
        self.assertEqual(
            retrieve_access_log_response.data["door_name"], "Server Room"
        )
        self.assertEqual(
            retrieve_access_log_response.data["access_granted"], True
        )


    def test_update_access_log_does_not_change_timestamp(self):
        create_access_log_response = self.client.post(
            "/api/logs/",
            {"card_id": "C4001", "door_name": "Main Entrance", "access_granted": True},
            format="json",
        )

        created_log_id = create_access_log_response.data["id"]
        original_timestamp = create_access_log_response.data["timestamp"]
        update_access_log_response = self.client.put(
            f"/api/logs/{created_log_id}/",
            {
                "card_id": "C4001",
                "door_name": "Side Entrance",
                "access_granted": False,
                "timestamp": "2000-01-01T00:00:00Z",
            },
            format="json",
        )

        self.assertEqual(update_access_log_response.status_code, 200)
        self.assertEqual(update_access_log_response.data["door_name"], "Side Entrance")
        self.assertEqual(update_access_log_response.data["access_granted"], False)
        self.assertEqual(update_access_log_response.data["timestamp"], original_timestamp)


    def test_delete_access_log_removes_record(self):
        create_access_log_response = self.client.post(
            "/api/logs/",
            {"card_id": "C5001", "door_name": "Main Entrance", "access_granted": True},
            format="json",
        )

        created_log_id = create_access_log_response.data["id"]
        delete_access_log_response = self.client.delete(
            f"/api/logs/{created_log_id}/"
        )
        self.assertEqual(delete_access_log_response.status_code, 204)

        retrieve_after_delete_response = self.client.get(
            f"/api/logs/{created_log_id}/"
        )
        self.assertEqual(retrieve_after_delete_response.status_code, 404)


    def test_filter_access_logs_by_card_id(self):
        self.client.post(
            "/api/logs/",
            {"card_id": "C6001", "door_name": "Door A", "access_granted": True},
            format="json",
        )
        self.client.post(
            "/api/logs/",
            {"card_id": "C6002", "door_name": "Door B", "access_granted": False},
            format="json",
        )
        self.client.post(
            "/api/logs/",
            {"card_id": "C6001", "door_name": "Door C", "access_granted": True},
            format="json",
        )

        filtered_response = self.client.get("/api/logs/?card_id=C6001")

        self.assertEqual(filtered_response.status_code, 200)
        self.assertEqual(len(filtered_response.data), 2)
        self.assertTrue(
            all(item["card_id"] == "C6001" for item in filtered_response.data)
        )


