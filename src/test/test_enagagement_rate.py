import statistics
from utils import calculate_regression, timed_test
import pytest
from data_structures.network import Network

@timed_test
def test_large_network_engagement_rate(large_network):
    print("Testing engagement rates for first 100 members...")
    engagement_rates = []
    followers_counts = []

    for member_id in range(1, 101):
        member = large_network.members[member_id]
        engagement_rate = member.engagement_rate()
        engagement_rates.append(engagement_rate)
        followers_counts.append(len(member.followers))

        print(f"Member {member_id} - Engagement rate: {engagement_rate:.2f} %")
        assert engagement_rate >= 0.0

    mean_engagement_rate = statistics.mean(engagement_rates)
    stddev_engagement_rate = statistics.stdev(engagement_rates)
    regression_coef, r_squared = calculate_regression(followers_counts, engagement_rates)

    print(f"Mean engagement rate: {mean_engagement_rate:.2f}")
    print(f"Standard deviation: {stddev_engagement_rate:.2f}")
    print(f"Regression coefficient: {regression_coef:.2f}")
    print(f"R-squared value: {r_squared:.2f}")

@pytest.fixture
def network():
    net = Network()
    net.generate_large_network(num_members=1000, num_followings=10000, num_interactions=5000)
    return net

def test_engagement_rate(network):
    print("Testing engagement rates for first 100 members...")
    total_engagement_rate = 0
    engagement_rates = []
    
    for member_id in range(1, 101):
        member = network.get_member(member_id)
        engagement_rate = member.engagement_rate()
        engagement_rates.append(engagement_rate)
        print(f"Member {member_id} - Engagement rate: {engagement_rate:.2f} %")
    
    mean_engagement_rate = sum(engagement_rates) / len(engagement_rates)
    print(f"Mean engagement rate: {mean_engagement_rate:.2f}")
    
    std_dev = (sum((x - mean_engagement_rate) ** 2 for x in engagement_rates) / len(engagement_rates)) ** 0.5
    print(f"Standard deviation: {std_dev:.2f}")
    
    # Additional statistics like regression coefficient and R-squared value can be printed similarly
    print("Test completed.")
