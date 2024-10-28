
# Algorithm Arena: Compete, Learn, and Win

![Flask](https://img.shields.io/badge/Backend-Flask-green)
![React](https://img.shields.io/badge/Frontend-React-blue)
![Docker](https://img.shields.io/badge/Deployment-Docker-yellow)
[![AWS](https://img.shields.io/badge/AWS-%23FF9900.svg?logo=amazon-web-services&logoColor=white)](#)

Welcome to **Algorithm Arena**, an algorithm testbed where users can solve coding problems with a gamified perspective. Our platform allows users to submit solutions to various algorithmic challenges, and it evaluates their performance. Built with a multi-container architecture, Algorithm Arena is designed for scalability and engaging competition.

---

## 🌟 Features

- **Algorithm Battles:** Choose from a curated list of problems with varying difficulty (easy, medium, hard), and test your algorithms in real-time.
- **Leaderboard:** Track your progress and compete with the top five users displayed on the leaderboard.
- **Log-in System:** Sign up or log in to track your progress. Your achievements are stored in our AWS-hosted database, and log-ins are remembered using cookies.

---

## 🚀 Quick Start

### Prerequisites

- Docker (for running the containers)
- Authentication keys (obtain from one of the project owners)

### Installation & Setup

#### Clone the Repository

```bash
git clone https://github.com/your_repo/algorithm-arena.git
cd algorithm-arena
```

#### Docker Setup

##### On Mac/Linux
1. Install Docker.
2. Run the following command to make the setup script executable:
```bash
chmod +x run.sh
```
3. Start the application with:
```bash
./run.sh
```

##### On Windows

1. Install Docker.
2. Open a terminal and run the following command to build and run the containers:
```bash
docker-compose up --build
```

3. Access the app by navigating to `http://localhost:8080/`.

---

## 🔑 Environment Variables

You will need to set up the following environment variables in a `.env` file for the application to run smoothly.
Please contact one of the authors for this.

---

## 💡 Future Enhancements

- **User-uploaded Problems:** Users will be able to upload their own problems for others to solve.
- **Competition Mode:** Start a competition session between multiple participants.
- **OAuth Integration:** Allow users to sign in using third-party services like Google or GitHub.
- **CI/CD Pipelines:** Automated deployment with GitHub Actions or AWS pipelines.

---

## 📧 Contact

For inquiries, please contact one of the project authors:  
📧 Albert Jing, Geoffrey Jing, Christo Polydorou, Nguyen Tran

---

## 🎉 Acknowledgments

Special thanks to team Scramble (John, Sunny, Artem, Roo) for helping implement the leaderboard feature.