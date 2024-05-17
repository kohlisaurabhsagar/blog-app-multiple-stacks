from locust import HttpUser, task, SequentialTaskSet, constant
from urllib.parse import urlparse, parse_qs
from bs4 import BeautifulSoup

class UserBehavior(SequentialTaskSet):
    def __init__(self, parent):
        super().__init__(parent)
        self.temp = ""

    def get_csrf_token(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        token_input = soup.find('input', {'name': 'csrf_token'})
        if token_input:
            return token_input.get('value')
        else:
            print("CSRF token not found in the response.")
            return None

    @task
    def login(self):
        response = self.client.get("/")
        token = self.get_csrf_token(response)
        form_data = {"username": "saurabh@iic", "password": "qwerty@123", "csrf_token": token}
        with self.client.post("/", data=form_data, catch_response=True, allow_redirects=False) as response:
            if response.status_code == 200:
                redirect_url = response.headers['Location']
                if redirect_url.endswith("/dashboard"):
                    print("Login successful, redirecting to dashboard.")
                    self.client.get(redirect_url)  
                else:
                    print("Unexpected redirect URL:", redirect_url)
                    response.failure("Unexpected redirect URL")
            else:
                print("Login Failed: ", response.text)
                response.failure("Login failed.")


    @task
    def create_post(self):
    
        response = self.client.get("/dashboard")
        token = self.get_csrf_token(response)
        
        form_data = {
            "title": (None, "sample title"),
            "content": (None, "sample content"),
            "csrf_token": (None, token),
            "image": ('', ''),  
        }

        
        with self.client.post("/dashboard", files=form_data, catch_response=True, allow_redirects=False) as response:
            print("Response status code:", response.status_code)
            if response.status_code == 302:
                redirect_url = response.headers['Location']
                print("Post created successfully, redirected to:", redirect_url)

                url_parts = urlparse(redirect_url)
                query_params = parse_qs(url_parts.query)
                post_id = query_params.get('post_id', [None])[0]

                if post_id:
                    self.temp = post_id
                    print("Captured post ID:", post_id)
                else:
                    print("Post ID not found in redirect URL.")
                    response.failure("Post ID not found")
            else:
                print("Failed to create post. Status code:", response.status_code)
                print("Response body:", response.text)
                response.failure("Failed to create post")
    
    @task
    def fetch_comment(self):
        with self.client.get(f"/post/{self.temp}", catch_response=True) as response:
            print(self.temp)
            print(response.status_code)
            if response.status_code == 200:
                print("Comments fetched successfully.")
            else:
                print("Failed to fetch comments.")
                response.failure("Failed to fetch comments")
    @task
    def add_comment(self):
        response = self.client.get(f"/post/{self.temp}")
        token = self.get_csrf_token(response)

        form_data = {
            "content": (None, "sample comment"),
            "csrf_token": (None, token),
        }
        with self.client.post(f"/post/{self.temp}", data=form_data, catch_response=True) as response:
            if response.status_code == 200:
                print("Comment added successfully.")
            else:
                print("Failed to add comment.")
                response.failure("Failed to add comment")
    
    @task
    def edit_post(self):
        response = self.client.get(f"/post/{self.temp}")
        token = self.get_csrf_token(response)
        data = {
            "title": "updated title",
            "content": "updated content",
            "_method": "PUT",
            "csrf_token":  token,
        }
        with self.client.put(f"/post/{self.temp}", data=data, catch_response=True) as response:
            if response.status_code == 200:
                print("Post edited successfully.")
            else:
                print("Failed to edit post.")
                response.failure("Failed to edit post")

    @task
    def delete_post(self):
        response = self.client.get(f"/post/{self.temp}")
        token = self.get_csrf_token(response)
        data = {
        "csrf_token": token,
        }
        with self.client.post(f"/post/{self.temp}/delete",data=data, catch_response=True) as response:
            print(response.status_code)
            if response.status_code == 200:
                print("Post deleted successfully.")
            else:
                print("Failed to delete post.")
                response.failure("Failed to delete post")

    @task
    def logout(self):
        with self.client.get("/logout", catch_response=True) as response:
            print("Logout status:", response.status_code)
            if response.status_code == 200:
                self.interrupt(reschedule=False)  

class WebsiteUser(HttpUser):
    host = "http://localhost:5000"
    tasks = [UserBehavior]
    wait_time = constant(1)
