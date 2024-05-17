from locust import HttpUser, task, SequentialTaskSet, constant

class UserBehavior(SequentialTaskSet):
    def __init__(self, parent):
        super().__init__(parent)
        self.token = ""
        self.temp = ""

    @task
    def login(self):
        with self.client.post("/api/login/", json={"username": "saurabh@iic", "password": "qwerty@123"}, catch_response=True) as response:
            if response.status_code == 200:
                print("Login Success: ", response.json())
                self.token = response.json()['token']
                print("Token stored for future requests:", self.token)
            else:
                print("Login Failed: ", response.text)
                response.failure("Failed to log in")

    @task
    def dashboard(self):
        headers = {
            "Authorization": f"Bearer {self.token}"
        }
        with self.client.get("/api/dashboard/", headers=headers, catch_response=True) as response:
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
        with self.client.post("/api/dashboard/", json={"title": "sample title", "content": "sample content"}, headers=headers, catch_response=True) as response:
            if response.status_code == 200:
                self.temp = response.json()['post']['_id']
                print("Post created successfully, ID:", self.temp)
            else:
                print("Failed to create post.")
                response.failure("Failed to create post")

    @task
    def fetch_comment(self):
        headers = {
            "Authorization": f"Bearer {self.token}"
        }
        with self.client.get(f"/api/post/{self.temp}/comment", headers=headers, catch_response=True) as response:
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
        with self.client.post(f"/api/post/{self.temp}/comment", json={"content": "sample comment"}, headers=headers, catch_response=True) as response:
            if response.status_code == 201:
                print("Comment added successfully.")
            else:
                print("Failed to add comment.")
                # print(response.status_code) sometimes backend may send 201 so it's good to check the response code
                response.failure("Failed to add comment")

    @task
    def edit_post(self):
        headers = {
            "Authorization": f"Bearer {self.token}"
        }
        with self.client.put(f"/api/post/{self.temp}", json={"title": "new title", "content": "new content"}, headers=headers, catch_response=True) as response:
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
        with self.client.delete(f"/api/post/{self.temp}", headers=headers, catch_response=True) as response:
            if response.status_code == 200:
                print("Post deleted successfully.")
            else:
                print("Failed to delete post.")
                response.failure("Failed to delete post")

    @task
    def logout(self):
        response = self.client.post("/api/logout")
        print("Logout status:", response.status_code)

class WebsiteUser(HttpUser):
    host = "http://localhost:9000"
    tasks = [UserBehavior]
    wait_time = constant(0.1)






