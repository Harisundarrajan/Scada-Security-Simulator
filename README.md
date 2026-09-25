# SCADA Security Simulator

This project is a simple simulation of a **SCADA/Industrial Control System environment** created to understand basic cybersecurity concepts in industrial systems.

The project simulates communication between a **PLC/RTU and a client** and demonstrates how an authentication weakness can allow unauthorized commands. It then shows how adding authentication can help prevent unauthorized access.

## What this project does

* Simulates a basic PLC/RTU device.
* Uses socket communication between the client and the simulated device.
* Demonstrates an authentication weakness.
* Shows how unauthorized commands can be accepted when proper authentication is not implemented.
* Adds token-based authentication as a security improvement.
* Tests the system before and after applying the security improvement.
* Provides a simple Flask-based dashboard to view the system.
* Records basic activity through logs.

## Technologies Used

* **Python**
* **Flask**
* **Socket Programming**
* **HTML/CSS**
* **Token-based Authentication**

## How It Works

The project has two main stages.

### Before Security Improvement

The simulated device accepts commands without properly verifying the user.

```text
Client → PLC/RTU → Command Accepted
```

This represents a basic authentication weakness.

### After Security Improvement

Token-based authentication is added to verify the request before accepting protected commands.

```text
Client → Authentication → PLC/RTU → Command Accepted
```

If authentication fails, the command is rejected.

## Testing

The project includes testing to compare the system before and after the security improvement.

The tests check whether:

* An unauthorized request can access the device.
* An authenticated request is accepted.
* Invalid authentication is rejected.
* The security improvement prevents unauthorized commands.

## Project Structure

```text
SCADA-Security-Simulator/
│
├── app.py
├── plc.py
├── client.py
├── requirements.txt
├── README.md
└── templates/
```

The exact files may vary as the project is developed further.

## Running the Project

### 1. Clone the repository

```bash
git clone https://github.com/Harisundarrajan/Scada-Security-Simulator.git
cd Scada-Security-Simulator
```

### 2. Install the required packages

```bash
pip install -r requirements.txt
```

### 3. Run the application

```bash
python app.py
```

Follow the instructions provided by the application to start the simulated SCADA environment.

## What I Learned

Through this project, I learned the basics of:

* SCADA and industrial control systems
* PLC/RTU communication
* Socket programming
* Authentication
* Basic network security concepts
* Identifying security weaknesses
* Applying a security improvement
* Testing security controls
* Using Flask to create a simple monitoring interface

## Future Improvements

Some improvements I would like to add in the future are:

* More realistic PLC/RTU communication
* Better authentication and authorization
* Network traffic monitoring
* More security test cases
* Improved logging
* Detection of suspicious commands
* Additional SCADA security scenarios

## Done By:

**Hari S**

GitHub: https://github.com/Harisundarrajan
