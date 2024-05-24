# Social Network Analysis Project

This case study involves the discussion of a custom unit-tested algorithm to calculate the influence and the engagement rate of each member of a simplified social network using two formulas.
Engagement Rate Formula:

The social networks calculate engagement rate using this formula:
Engagement Rate=(Total Likes+Total CommentsFollowers)×100Engagement Rate=(FollowersTotal Likes+Total Comments​)×100
Influence Formula:

The influence of a member A on a member B is calculated by:
Influence=Likes from A to B+Comments from A to BTotal Engagement of A×100Influence=Total Engagement of ALikes from A to B+Comments from A to B​×100

In this network, members can follow other members without the requirement of following back. The primary objective is to represent a social network with suitable data structures. Finally, it must identify the shortest and the highest engagement path between any given pair of members, noting that there is not always a path from a member A to a member B.

## Description

This project analyzes social network interactions using various algorithms to calculate engagement rates, influence, and paths within the network. In main.py, you can adjust the number of users by modifying the sizes list. Study and analyze the results in network_analysis_output.txt.

## Installation

### IDE

- Visual Studio Code

### Prerequisites

- Python 3.x

## Setup

1. Clone the repository:

    ```sh
    git clone https://github.com/liakopal/social-network-influence.git
    

2. Navigate to the project directory:

    ```sh
    cd social_network
    

3. Create a virtual environment:

    ```sh
    python -m venv venv


4. Activate the virtual environment:

    - **Windows:**
      ```sh
      .\venv\Scripts\activate
      ```

    - **macOS/Linux:**
      ```sh
      source venv/bin/activate
    

5. Install the required dependencies:

    ```sh
   pip install -r requirements.txt


## Usage

1. Run the main script:

    ```sh
   python src/main.py

2. Run an individual test file:
    ```sh
   python -m unittest discover -s ./src/test/

### Related Project

You can find a similar version of this project in another GitHub account here: https://github.com/alexliak/social-media-influence.git

## Algorithms Used

BFS (Breadth-First Search): Used to find the shortest path between members.
DFS (Depth-First Search): Used to find the path with the highest engagement between members.
Dijkstra's Algorithm: Another approach to find the shortest path between members.

### Adjusting the Number of Users
To adjust the number of users in the network, modify the sizes list in the main function in src/main.py. For example, to create networks of sizes 10, 20, and 30, update the sizes list as follows:
def main():
    sizes = [10, 20, 30]  # Network sizes for testing
    networks = generate_progressive_networks(sizes)