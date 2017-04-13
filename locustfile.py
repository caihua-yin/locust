from locust import HttpLocust, TaskSet, task
from faker import Faker
import random
import md5

class AmbryTasks(TaskSet):
    def on_start(self):
        print "On start..."

        # Initialize fake factory, to generate blob data for POST
        self.fake = Faker()

        # Initialize blobs dict, which stores blob id and corresponding checksum
        self.blobs = {}

    @task(1)
    def health(self):
        self.client.get("/healthCheck")

    @task(5)
    def post(self):
        blob_content = self.fake.text()
        self.client.headers['x-ambry-blob-size'] = str(len(blob_content))
        self.client.headers['x-ambry-service-id'] = 'locust'
        self.client.headers['x-ambry-content-type'] = 'text/plain'
        with self.client.post("/", data=blob_content, catch_response=True) as response:
            # Verify response status
            if response.status_code != 201:
                response.failure("POST blob response status is %d, expect 201, response body: %s" \
                        % (response.status_code, response.content))
            else:
                # The returned location string has a '/' before blob id,
                # like '/AAEAAQAAAAAAAAABAAAAJGVlZjc3MmNiLWJmNGItNGNmNi05NDNmLTZhNWIzZmMzM2M1Zg'
                # Extract the blob id from location string
                blob_id = response.headers['Location'][1:]
                print "POST %s" % blob_id

                # Store blob id and content checksum for GET/HEAD/DELETE operation
                self.blobs[blob_id] = md5.new(blob_content).hexdigest()

    @task(1)
    def get(self):
        # Remove extra headers set by post
        self._remove_header()

        # Skip GET blob if there is no blob created
        if len(self.blobs) == 0:
            return

        blob_id = random.choice(self.blobs.keys())
        print "GET %s" % blob_id

        # Catch the response and define success/failure criteria
        # (By default locust will consider all 2xx response status as success)
        with self.client.get("/%s" % blob_id, name="/[blob id]", catch_response=True) as response:
            # Verify response status
            if response.status_code != 200:
                response.failure("GET blob response status is %d, expect 200, response body: %s, blob: %s" \
                        % (response.status_code, response.content, blob_id))
            else:
                # Verify MD5 checksum of blob content
                got_chesum = md5.new(response.content).hexdigest()
                if got_chesum != self.blobs[blob_id]:
                    # Write blob content to /tmp/<blob id> for later trouble shooting if checksum not matches
                    blob_content_file = "/tmp/%s" % blob_id
                    with open(blob_content_file, 'w') as f:
                        f.write(response.content)
                    # Report failure
                    response.failure("Blob content checksum not match on GET, blob: %s, expected checksum: %s, got: %s, blob content dumped at %s" \
                            % (blob_id, self.blobs[blob_id], got_chesum, blob_content_file))

    @task(2)
    def head(self):
        # Remove extra headers set by post
        self._remove_header()

        # Skip GET blob if there is no blob created
        if len(self.blobs) == 0:
            return

        blob_id = random.choice(self.blobs.keys())
        print "HEAD %s" % blob_id
        self.client.head("/%s" % blob_id, name="/[blob id]")

    @task(1)
    def delete(self):
        # Remove extra headers set by post
        self._remove_header()

        # Skip GET blob if there is no blob created
        if len(self.blobs) == 0:
            return
        
        blob_id = random.choice(self.blobs.keys())
        self.blobs.pop(blob_id)
        print "DELETE %s" % blob_id

        self.client.delete("/%s" % blob_id, name="/[blob id]")

    def _remove_header(self):
        self.client.headers.pop('x-ambry-blob-size', None)
        self.client.headers.pop('x-ambry-service-id', None)
        self.client.headers.pop('x-ambry-content-type', None)

class AmbryUser(HttpLocust):
    task_set = AmbryTasks
    # Each user would wait between 1 and 5 seconds between tasks
    min_wait = 100     # in ms
    max_wait = 500     # in ms

    # Specify host here so it need not be specified by '--host' when running locust command
    # host = "http://192.168.33.22:1174"
