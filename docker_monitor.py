import time # Import the time module.
import docker # Import the Docker module.
from prometheus_client import Gauge, start_http_server # Import the Prometheus library.

# Initialize the Docker client
client = docker.from_env() # Connect to the Docker daemon using the environment variables

# Define a gauge to store Docker container metrics
# This line of code is defining a metric named 'docker_container_state_created' using the Prometheus client library in Python. This metric will track the state of Docker containers created. The metric has two labels: 'id' and 'name'. The labels will help you distinguish between different containers. The metric will be of type Gauge, which means it can go both up and down.
# Here's a brief explanation of the metric:
# 'docker_container_state_created': The name of the metric.
# 'State of Docker containers created': A description of what the metric represents.
# ['id', 'name']: The labels for this metric. These labels will help you identify specific containers in your monitoring data.
container_state_created = Gauge('docker_container_state_created', 'State of Docker containers created', ['id', 'name']) 
container_state_restarting = Gauge('docker_container_state_restarting', 'State of Docker containers Restarting', ['id', 'name'])
container_state_running = Gauge('docker_container_state_running', 'State of Docker containers Running', ['id', 'name'])
container_state_removing = Gauge('docker_container_state_removing', 'State of Docker containers removing', ['id', 'name'])
container_state_paused = Gauge('docker_container_state_paused', 'State of Docker containers paused', ['id', 'name'])
container_state_exited = Gauge('docker_container_state_exited', 'State of Docker containers exited', ['id', 'name'])
container_state_dead = Gauge('docker_container_state_dead', 'State of Docker containers dead', ['id', 'name'])
container_cpu_percent = Gauge('docker_container_cpu_percent', 'CPU usage percentage of Docker containers', ['id', 'name'])
container_memory_usage = Gauge('docker_container_memory_usage', 'Memory usage of Docker containers (MB)', ['id', 'name'])

# Define a function to get container metrics
def get_container_metrics(container): # Function to get container metrics
    info = container.stats(stream=False) # Get container stats
    cpu_percent = info['cpu_stats']['cpu_usage']['total_usage'] / info['cpu_stats']['system_cpu_usage'] * 100 # Calculate CPU usage
    memory_usage = info['memory_stats']['usage'] / (1024 * 1024) # Calculate memory usage in MB
    return cpu_percent, memory_usage # Return CPU usage and memory usage

# Define a function to update metrics
# This line of code is using Python and the Prometheus client library to create a metric called 'container_state_created' with labels 'id' and 'name'. It then sets the value of this metric to 1 if the condition inside the set() function is true, or 0 if it is false.
# Here's a breakdown of what each part does:
# container_state_created: This is the name of the metric.
# labels(id=container.id, name=container.name): This creates labels for the metric with the given values. The labels allow you to group and filter metrics based on specific attributes.
# .set(container.status == 'created'): This sets the value of the metric. In this case, it checks if the container.status attribute equals the string 'created'. If it does, it sets the metric value to 1; otherwise, it sets it to 0.

def update_metrics(): # Function to update metrics
    for container in client.containers.list(): # Loop through all containers
        cpu_percent, memory_usage = get_container_metrics(container) # Get container metrics
        container_state_created.labels(id=container.id, name=container.name).set(container.status == 'created')
        container_state_restarting.labels(id=container.id, name=container.name).set(container.status == 'restarting')
        container_state_running.labels(id=container.id, name=container.name).set(container.status == 'running')
        container_state_removing.labels(id=container.id, name=container.name).set(container.status == 'removing')
        container_state_paused.labels(id=container.id, name=container.name).set(container.status == 'paused')
        container_state_exited.labels(id=container.id, name=container.name).set(container.status == 'exited')
        container_state_dead.labels(id=container.id, name=container.name).set(container.status == 'dead')
        container_cpu_percent.labels(id=container.id, name=container.name).set(cpu_percent)
        container_memory_usage.labels(id=container.id, name=container.name).set(memory_usage)


# Start the Docker Information HTTP server
start_http_server(8000)

# Update metrics every 5 seconds
while True: # Loop forever
    update_metrics() # Update metrics
    time.sleep(5)  # Adjust the interval as needed
