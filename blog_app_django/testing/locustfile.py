from locust import HttpUser, task, SequentialTaskSet, constant
from urllib.parse import urlparse, parse_qs
from bs4 import BeautifulSoup

class UserBehavior(SequentialTaskSet):
    def __init__(self, parent):
        super().__init__(parent)
        self.temp = ""

    def get_csrf_token(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        token_input = soup.find('input', {'name': 'csrfmiddlewaretoken'})

        if token_input:
            return token_input.get('value')
        else:
            print("CSRF token not found in the response.")
            return None

    @task
    def login(self):
        response = self.client.get("/users/login/")
        print(response)
        token = self.get_csrf_token(response)
        print(token)
        form_data = {"username": "saurabh@iic", "password": "qwerty@123", "csrfmiddlewaretoken": token}
        with self.client.post("/users/login/", data=form_data, catch_response=True, allow_redirects=False) as response:
            print(response.status_code)
            if response.status_code == 302:
                    print("Login successful")
            else:
                print("Login Failed: ", response.text)
                response.failure("Login failed.")


    @task
    def create_post(self):
        response = self.client.get("/")
        token = self.get_csrf_token(response)
        print(token)
        form_data = {
            "title": (None, "sample title"),
            "content": (None, "sample content"),
            "csrfmiddlewaretoken": (None, token),
            "image": ('', ''),  
        }
        
        with self.client.post("/", files=form_data, catch_response=True, allow_redirects=False) as response:
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
        with self.client.get(f"/post_details/{self.temp}", catch_response=True) as response:
            print(response.status_code)
            if response.status_code == 200:
                print("Comments fetched successfully.")
            else:
                print("Failed to fetch comments.")
                response.failure("Failed to fetch comments")
    @task
    def add_comment(self):
        response = self.client.get(f"/post_details/{self.temp}")
        token = self.get_csrf_token(response)

        form_data = {
            "content": (None, "sample comment"),
            "csrfmiddlewaretoken": (None, token),
        }
        with self.client.post(f"/post_details/{self.temp}", data=form_data, catch_response=True) as response:
            if response.status_code == 200:
                print("Comment added successfully.")
            else:
                print("Failed to add comment.")
                response.failure("Failed to add comment")
    
    @task
    def edit_post(self):
        response = self.client.get(f"/post_edit/{self.temp}")
        token = self.get_csrf_token(response)
        print(token)
        data = {
            "title": "updated title",
            "content": "updated content",
            "csrfmiddlewaretoken": token,
        }
        with self.client.post(f"/post_edit/{self.temp}", data=data, catch_response=True) as response:
            print(f"Response status code: {response.status_code}")
            if response.status_code == 200:
                print("Post edited successfully.")
            else:
                print("Failed to edit post.")
                response.failure("Failed to edit post")

    @task
    def delete_post(self):
        print(f"Attempting to delete post with ID: {self.temp}")
        response = self.client.get(f"/post_delete/{self.temp}")
        print(f"Response status code: {response.status_code}")
        if response.status_code == 200:
            print("Post deleted successfully.")
        else:
            print("Failed to delete post.")
            response.failure("Failed to delete post")

    @task
    def logout(self):
        with self.client.get("/users/logout", catch_response=True) as response:
            print("Logout status:", response.status_code)
            if response.status_code == 200:
                self.interrupt(reschedule=False)  

class WebsiteUser(HttpUser):
    host = "http://localhost:8000"
    tasks = [UserBehavior]
    wait_time = constant(5)






