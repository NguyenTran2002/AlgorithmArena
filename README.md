
# Algorithm Arena

**Welcome to Algorithm Arena**, a gamified algorithm testbed designed to challenge your coding skills. Users can solve coding problems similar to LeetCode or Codeforces, and soon, we will introduce functionality for users to upload their own challenges and compete with others in real-time competitions.

---

## Table of Contents
1. [Overview](#overview)  
2. [Getting Started](#getting-started)  
   - [Prerequisites](#prerequisites)  
   - [Quick Start](#quick-start)  
   - [Docker Setup](#docker-setup)  
3. [Functionalities](#functionalities)  
   - [Algorithm Testbed](#algorithm-testbed)  
   - [User Authentication & Progress Tracking](#user-authentication--progress-tracking)  
   - [Leaderboard](#leaderboard)  
4. [Project Structure](#project-structure)  
   - [React Main App](#react-main-app)  
   - [Database Container](#database-container)  
   - [Evaluation Container](#evaluation-container)  
5. [Correct Code Access](#correct-code-access)  
6. [Acknowledgments](#acknowledgments)

---

## Overview
Algorithm Arena provides a testbed for algorithm enthusiasts to practice and improve their problem-solving skills. Users can select from a variety of challenges, attempt solutions in an IDE-like interface, and track their progress over time. We plan to extend this platform to allow custom problem uploads and multiplayer competitions.

---

## Getting Started

### Prerequisites
This is a server-based application, and some features require authentication keys. Please contact any of the following team members to request these keys:
- **Albert Jing**  
- **Geoffrey Jing**  
- **Christo Polydorou**  
- **Nguyen Tran**

Additionally, ensure Docker is installed on your system. Follow the [Docker installation guide](https://docs.docker.com/get-docker/) for platform-specific instructions.

---

### Quick Start  
**For Mac and Linux:**
1. Install Docker if not already installed.  
2. Clone this repository and navigate to the project directory in the terminal.  
3. Run the following command once to make the script executable:
   ```bash
   chmod +x run.sh
   ```
4. Start the application:
   ```bash
   ./run.sh
   ```
   > The browser will open automatically. The first launch may take 40-50 seconds, while subsequent runs will take less than 5 seconds.

5. On subsequent runs, you can skip steps 1-3 and directly execute:
   ```bash
   ./run.sh
   ```

**For Windows:**  
Follow the [Docker Setup](#docker-setup) instructions below.

---

### Docker Setup
**For All Systems:**
1. Ensure Docker is installed and running.  
2. In the terminal, navigate to the directory where you cloned the repository.  
3. Build and start the application with:
   ```bash
   docker compose up --build
   ```
4. Open your browser and visit: `http://localhost:8080/`

---

## Functionalities

### Algorithm Testbed
- Select from **10 curated coding problems** spanning **easy, medium, and hard** levels.  
- Write and submit solutions directly in the integrated IDE.  
- Get instant feedback on your submission:
  - **Success:** View the runtime per test case.  
  - **Failure:** See which test cases failed and compare expected vs. actual outputs.  
  - **Timeout:** Detect and manage inefficient code or infinite loops.  

### User Authentication & Progress Tracking
- **Log in or Sign up** to save your progress.  
- Your progress is stored in an **AWS-hosted MySQL** database and remembered using cookies.

### Leaderboard
- Compete to reach the **top 5 leaderboard** and showcase your problem-solving achievements.

---

## Project Structure

### React Main App  
Handles the **frontend interface** and communication between containers. Key functions include:
- Fetching and displaying problems and starter code from the database.  
- Sending user solutions to the evaluation container for testing.  
- Managing user logins and leaderboard displays through API calls to the database container.

### Database Container  
Facilitates interactions with the AWS MySQL and MongoDB servers. Responsibilities include:
- Retrieving problem descriptions, arguments, and test cases.  
- Handling user authentication and leaderboard updates.  

### Evaluation Container  
The core of the application, responsible for:
- Testing user code against predefined test cases.  
- Ensuring solutions are efficient and free of infinite loops.  
- Returning success/failure results along with average runtimes.

---

## Correct Code Access
You can find the correct solutions for all available problems under the `./Q&A/solutions` directory. Use these for reference while exploring the platform.

---

## Acknowledgments
We extend our gratitude to **Team Scramble** (John, Sunny, Artem, and Roo) for their invaluable help in building the React-based leaderboard page.

---

This README provides a comprehensive overview and usage instructions for Algorithm Arena. We look forward to your contributions and feedback as we continue to improve the platform.
