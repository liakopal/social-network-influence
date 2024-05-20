# Social Network Analysis Project

This case study involves the discussion of a custom unit-tested algorithm to calculate the influence and the engagement rate of each member of a simplified social network using two formulas.

The social networks calculate engagement rate using this formula: 

The influence of a member A on a member B is calculated by:


In this network, members can follow other members without the requirement of following back. The primary objective is to represent a social network with suitable data structures. Finally, it must identify the shortest and the highest engagement path between any given pair of members, noting that there is not always a path from a member A to a member B.

## Description

This project analyzes social network interactions using various algorithms to calculate engagement rates, influence, and paths within the network. In line 267 in `main.py`, you can adjust the numbers of users by modifying the range when adding members. Study and analyze the results in `network_summary.csv`.

## Installation

### IDE

- Visual Studio Code

### Prerequisites

- Python 3.x

## Setup

1. Clone the repository:

    ```sh
    git clone https://github.com/liakopal/social-network-influence.git
    ```

2. Navigate to the project directory:

    ```sh
    cd social-network
    ```

3. Create a virtual environment:

    ```sh
    python -m venv venv
    ```

4. Activate the virtual environment:

    - **Windows:**
      ```sh
      .\venv\Scripts\activate
      ```

    - **macOS/Linux:**
      ```sh
      source venv/bin/activate
      ```

5. Install the required dependencies:

    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. Run the main script:

    ```sh
    python src/main.py

2. Run the test script:
    ```sh
    pytest -s .\src\test\

3. Run an individual test file:
    ```sh
    pytest src/tests/test_specific_file.py

### Related Project

You can find a similar version of this project in another GitHub account here: https://github.com/liakopal/social-network-influence.git

### Adjusting the Number of Users

To change the number of users for testing, you can modify the range in line 267 of main.py. This allows you to customize the size of the social network for different test scenarios.