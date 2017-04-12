from locust import HttpLocust, TaskSet, task

class AmbryTasks(TaskSet):
    def on_start(self):
        print "On start..."
        #self.client.post("/login", {
        #    "username": "test_user",
        #    "password": ""
        #})
    
    @task
    def health(self):
        self.client.get("/healthCheck")
        
class AmbryUser(HttpLocust):
    task_set = AmbryTasks
    # Each user would wait between 1 and 5 seconds between tasks
    min_wait = 1000     # in ms
    max_wait = 5000     # in ms
