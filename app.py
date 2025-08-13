from flask import Flask, render_template, request

app = Flask(__name__)

# Dummy credentials
VALID_USERNAME = "admin"
VALID_PASSWORD = "password"

# Dummy data for AWS instances
instances = [
    {
        "id": f"i-{str(i).zfill(3)}",
        "name": f"Instance-{i}",
        "type": "t2.micro" if i % 2 == 0 else "t3.medium",
        "region": "us-east-1" if i % 3 == 0 else "us-west-1" if i % 3 == 1 else "eu-central-1",
        "status": "running" if i % 2 == 0 else "stopped",
        "launch_date": f"2025-{str((i % 12) + 1).zfill(2)}-{str((i % 28) + 1).zfill(2)}",
        "cpu": i % 100,
        "memory": i % 16
    }
    for i in range(1, 101)  # Generate 100 instances
]

@app.route("/")
def login():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def handle_login():
    username = request.form.get("username")
    password = request.form.get("password")

    if username == VALID_USERNAME and password == VALID_PASSWORD:
        return render_template("AWSInventory.html", instances=instances)
    else:
        return render_template("login.html", error="Invalid username or password")

@app.route("/instance-metrics")
def instance_metrics():
    # Get query parameters
    instance_id = request.args.get("id", "Unknown")
    cpu_usage = request.args.get("cpu", 15)
    memory_usage = request.args.get("memory", 55)

    # Render the InstanceMetrics.html template and pass the parameters
    return render_template("InstanceMetrics.html", instance_id=instance_id, cpu_usage=cpu_usage, memory_usage=memory_usage)

if __name__ == "__main__":
    app.run(debug=True)