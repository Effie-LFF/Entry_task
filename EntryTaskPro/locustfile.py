from locust import HttpUser, task, between


class QuickstartUser(HttpUser):
    wait_time = between(5, 9)

    @task
    def on_start(self):
        param = {"name_id": "user001", "price": 123.3, "discount": 0.9}
        self.client.post("/query", json=param)
