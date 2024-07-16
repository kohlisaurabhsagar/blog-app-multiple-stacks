from locust import HttpUser, task, SequentialTaskSet, constant

class UserBehavior(SequentialTaskSet):
    def __init__(self, parent):
        super().__init__(parent)
        self.token = ""
        self.temp = ""
        self.rtoken = ""

    @task
    def login(self):
        with self.client.post("/users/login/", json={"username": "hari@iic", "password": "Qwerty@123"}, catch_response=True) as response:
            if response.status_code == 200:
                self.token = response.json()['access']
                self.rtoken = response.json()['refresh']
                print("Login successful.")
            else:
                print("Login Failed: ", response.text)
                response.failure("Failed to log in")

    @task
    def dashboard(self):
        headers = {
            "Authorization": f"Bearer {self.token}"
        }
        with self.client.get("/", headers=headers, catch_response=True) as response:
            if response.status_code == 200:
                print("Accessed protected route successfully.")
            else:
                print("Failed to access protected route.")
                response.failure("Failed to access protected route")

    @task
    def create_post(self):
        headers = {
            "Authorization": f"Bearer {self.token}"
        }
        with self.client.post("/", json={"title": "sample title", "content": "sample content"}, headers=headers, catch_response=True) as response:
            if response.status_code == 201:
                self.temp = response.json()['id']
                print("Post created successfully, ID:", self.temp)
            else:
                print("Failed to create post.")
                response.failure("Failed to create post")

    @task
    def fetch_comment(self):
        headers = {
            "Authorization": f"Bearer {self.token}"
        }
        with self.client.get(f"/posts/{self.temp}/comments", headers=headers, catch_response=True) as response:
            if response.status_code == 200:
                print("Comments fetched successfully.")
            else:
                print("Failed to fetch comments.")
                response.failure("Failed to fetch comments")

    @task
    def add_comment(self):
        headers = {
            "Authorization": f"Bearer {self.token}"
        }
        with self.client.post(f"/posts/{self.temp}/comments", json={"content": "sample comment"}, headers=headers, catch_response=True) as response:
            if response.status_code == 201:
                print("Comment added successfully.")
            else:
                print("Failed to add comment.")
                response.failure("Failed to add comment")

    @task
    def edit_post(self):
        headers = {
            "Authorization": f"Bearer {self.token}"
        }
        with self.client.put(f"/posts/{self.temp}", json={"title": "updated title", "content": "updated content"}, headers=headers, catch_response=True) as response:
            if response.status_code == 200:
                print("Post edited successfully.")
            else:
                print("Failed to edit post.")
                response.failure("Failed to edit post")

    @task
    def delete_post(self):
        headers = {
            "Authorization": f"Bearer {self.token}"
        }
        with self.client.delete(f"/posts/{self.temp}", headers=headers, catch_response=True) as response:
            if response.status_code == 204:
                print("Post deleted successfully.")
            else:
                print("Failed to delete post.")
                response.failure("Failed to delete post")

    @task
    def logout(self):
        headers = {
            "Authorization": f"Bearer {self.token}"
        }
        with self.client.post(f"/users/logout/", json={"refresh": self.rtoken}, headers=headers, catch_response=True) as response:
            if response.status_code == 205:
                print("Logged out successfully.")
            else:
                print("Failed to delete post.")
                response.failure("Failed to log out.")



class WebsiteUser(HttpUser):
    host = "http://localhost:9000"
    tasks = [UserBehavior]
    wait_time = constant(5)






