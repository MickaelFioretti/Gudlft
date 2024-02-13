from locust import HttpUser, task, between


class WebsiteUser(HttpUser):
    wait_time = between(1, 5)

    @task
    def load_homepage(self):
        self.client.get("/")

    @task(3)  # Exécute cette tâche 3 fois plus souvent que les autres
    def perform_task(self):
        self.client.post("/showSummary", {"email": "john@simplylift.co"})
