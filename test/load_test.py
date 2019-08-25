import json

from locust import HttpLocust, TaskSet, task


class SchemaOperations(TaskSet):
    def on_start(self):
        # assume all users arrive at the index page
        self.get()

    @task(10)
    def get(self):
        r = self.client.get("/schemas", verify=False)
        print(r)


def get_url():
    with open('api_conf.json') as json_file:
        data = json.load(json_file)
        return data['gwApiUrl']


class SchemaLoadApp(HttpLocust):
    task_set = SchemaOperations
    host = get_url()

    # Fire test with some random times
    min_wait = 20 * 1000
    max_wait = 600 * 1000
