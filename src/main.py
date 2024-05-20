from utils import generate_progressive_networks, create_engagement_matrix, create_shortest_path_matrix, create_binary_matrix
import statistics

def main():
    sizes = [10, 50, 100, 500, 1000]  # progressively larger network sizes
    networks = generate_progressive_networks(sizes)

    for idx, network in enumerate(networks):
        size = sizes[idx]
        print(f"Testing network of size {size}...")
        
        # Calculate Engagement Matrix
        engagement_matrix = create_engagement_matrix(network)
        
        # Calculate Shortest Path Matrix
        shortest_path_matrix = create_shortest_path_matrix(network)
        
        # Calculate Binary Matrix from Shortest Path Matrix
        binary_matrix = create_binary_matrix(shortest_path_matrix)

        # Metrics and Output
        mean_engagement_rate = statistics.mean(
            [engagement for row in engagement_matrix for engagement in row if engagement != 0]
        )
        max_engagement_rate = max(
            [engagement for row in engagement_matrix for engagement in row if engagement != 0]
        )
        mean_shortest_path_length = statistics.mean(
            [path for row in shortest_path_matrix for path in row if path != float('inf')]
        )
        max_shortest_path_length = max(
            [path for row in shortest_path_matrix for path in row if path != float('inf')]
        )

        print(f"Network of size {size} tested.")
        print(f"Mean engagement rate: {mean_engagement_rate:.2f}")
        print(f"Max engagement rate: {max_engagement_rate:.2f}")
        print(f"Mean shortest path length: {mean_shortest_path_length:.2f}")
        print(f"Max shortest path length: {max_shortest_path_length:.2f}")

        # Display some samples for verification
        print(f"Engagement matrix sample: {engagement_matrix[:3][:3]}")
        print(f"Shortest path matrix sample: {shortest_path_matrix[:3][:3]}")
        print(f"Binary matrix sample: {binary_matrix[:3][:3]}")
        print()

if __name__ == "__main__":
    main()
