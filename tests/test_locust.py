from locust import HttpUser, task, between

class FoodAppUser(HttpUser):
    wait_time = between(1, 5)
    csrf_token = None

    def on_start(self):
        # Bersihkan cookies dan ambil halaman /user/ untuk dapatkan CSRF token dari cookie
        self.client.cookies.clear()
        response = self.client.get("/user/")
        if response.status_code == 200:
            # Ambil csrf token dari cookie 'csrftoken'
            self.csrf_token = self.client.cookies.get("csrftoken")

    @task(3)
    def access_user_page(self):
        with self.client.get("/user/", catch_response=True) as response:
            if response.status_code != 200:
                response.failure(f"Failed to load /user/ page: {response.status_code}")

    @task(5)
    def submit_user_data(self):
        if not self.csrf_token:
            # Kalau belum ada token, coba reload dulu
            response = self.client.get("/user/")
            self.csrf_token = self.client.cookies.get("csrftoken")
            if not self.csrf_token:
                return  # skip jika token masih gak ada

        data = {
            "age": "22",
            "weight": "60",
            "height": "170",
            "gender": "male",         
            "activity": "1.55",
            "csrfmiddlewaretoken": self.csrf_token
        }
        headers = {
            "Referer": self.client.base_url + "/user/",
        }

        with self.client.post("/user/", data=data, headers=headers, catch_response=True) as response:
            if response.status_code != 200:
                response.failure(f"Submit form failed: {response.status_code}")
            elif "Hasil BMI" not in response.text:
                response.failure("Response missing expected 'Hasil BMI' text")
