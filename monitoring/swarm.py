import subprocess

from locust import between, HttpUser, task, TaskSet


class MyAPITasks(TaskSet):
    @task
    def register_user(self):
        self.client.post("/auth/register", json={"email": "test@example.com", "password": "password123"})

    @task
    def login_user(self):
        self.client.post("/auth/login", json={"email": "test@example.com", "password": "password123"})

    @task
    def logout_user(self):
        self.client.post("/auth/logout")

    @task
    def delete_user(self):
        self.client.post("/auth/delete")

    @task
    def get_profile(self):
        self.client.get("/auth/profile")


class MyAPIUser(HttpUser):
    tasks = [MyAPITasks]
    wait_time = between(1, 5)
    host = "http://localhost:8000"

    def on_start(self):
        self.client.post("/auth/login", json={"email": "test@example.com", "password": "password123"})


if __name__ == "__main__":
    subprocess.run([
        "locust",
        "-f",
        "swarm.py"
    ])
