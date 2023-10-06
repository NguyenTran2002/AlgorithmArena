# Addition Web Application

This is a multi-container docker applications as a proof of concepts.

This application demonstrate the communication ability between the following component:
    - Add Numbers API (add_numbers folder)
    - Random A Number API (num_randomizer folder)
    - Front-end that takes user input as two numbers

Each of the components above is a separate and independent Docker container.

To run this application, at the root directory, use the command
```docker compose up -d```