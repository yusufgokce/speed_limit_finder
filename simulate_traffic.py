# Import required libraries
import numpy as np
import matplotlib.pyplot as plt

# GLOBAL CONSTANTS
EU_STANDARD_PERCENTILE = 85  # Percentile for determining speed limits in the EU
US_STANDARD_PERCENTILE = 90  # Example of another standard
DEFAULT_NUM_VEHICLES = 1000
DEFAULT_MEAN_SPEED = 70  # mph
DEFAULT_STD_DEV_SPEED = 10  # mph


# FUNCTIONS

def import_data():
    """
    Allows the user to input custom speed data or use simulated data.

    Precondition: User provides a valid option (1 or 2) and optionally supplies custom speed data.
    Postcondition: Returns an array of vehicle speeds.
    """
    print("\nChoose an option to provide speed data:")
    print("1. Simulate vehicle speeds (default random data).")
    print("2. Enter a list of speeds manually.")
    option = input("Enter 1 or 2: ").strip()

    if option == "1":
        print(
            f"\nSimulating {DEFAULT_NUM_VEHICLES} vehicle speeds with mean = {DEFAULT_MEAN_SPEED} mph and std deviation = {DEFAULT_STD_DEV_SPEED} mph.")
        return generate_speed_data(DEFAULT_NUM_VEHICLES, DEFAULT_MEAN_SPEED, DEFAULT_STD_DEV_SPEED)
    elif option == "2":
        print("\nEnter a list of speeds, separated by commas (ex: 60, 70, 80, ... ):")
        try:
            speeds = list(map(float, input().split(",")))
            if len(speeds) == 0:
                raise ValueError("No speeds were provided.")
            return np.array(speeds)
        except ValueError as e:
            print(f"Error: {e}")
            return import_data()  # Retry in case of error
    else:
        print("Invalid option. Please enter 1 or 2.")
        return import_data()


def generate_speed_data(num_vehicles, mean_speed, std_dev_speed, seed=None):
    """
    Simulates vehicle speed data using a normal distribution.

    Precondition: `num_vehicles` > 0, `std_dev_speed` > 0.
    Postcondition: Returns an array of simulated vehicle speeds.
    """
    np.random.seed(seed)
    return np.random.normal(mean_speed, std_dev_speed, num_vehicles)


def calculate_percentile(speeds, nth_percentile):
    """
    Calculates the nth percentile of the given speed data.

    Precondition: 0 <= nth_percentile <= 100.
    Postcondition: Returns the speed corresponding to the nth percentile.
    """
    return np.percentile(speeds, nth_percentile)


def remove_outliers(speeds, z_threshold=3):
    """
    Removes outliers from the dataset using the Z-score method.

    Precondition: `z_threshold` > 0.
    Postcondition: Returns a tuple: the speeds without outliers and the list of removed outliers.
    """
    mean = np.mean(speeds)
    std_dev = np.std(speeds)
    z_scores = (speeds - mean) / std_dev
    outliers = speeds[np.abs(z_scores) >= z_threshold]
    cleaned_speeds = speeds[np.abs(z_scores) < z_threshold]
    return cleaned_speeds, outliers


def find_vehicles_above_threshold(speeds, threshold):
    """
    Finds speeds above a specified threshold.

    Precondition: `threshold` is a valid number.
    Postcondition: Returns a list of speeds above the threshold.
    """
    return speeds[speeds > threshold]


def visualize_data(speeds, percentile_threshold, highlighted_speeds, nth_percentile):
    """
    Visualizes the speed distribution and highlights vehicles exceeding the threshold.

    Precondition: `speeds` and `highlighted_speeds` are non-empty arrays.
    Postcondition: Displays a histogram with the threshold and highlighted excessive speeds.
    """
    plt.figure(figsize=(12, 6))

    # Overall speed histogram
    bins = np.linspace(min(speeds), max(speeds), 30)
    plt.hist(speeds, bins=bins, alpha=0.7, label="Vehicle Speeds", color='blue', edgecolor='black')

    # Highlight speeds exceeding the threshold
    plt.hist(highlighted_speeds, bins=bins, alpha=0.7, label=f"Speeds > {nth_percentile}th Percentile", color='red',
             edgecolor='black')

    # Add a vertical line for the percentile threshold
    plt.axvline(percentile_threshold, color='red', linestyle='dashed', linewidth=2,
                label=f"{nth_percentile}th Percentile = {percentile_threshold:.2f} mph")

    plt.title("Vehicle Speed Distribution and Excessive Speeders")
    plt.xlabel("Speed (mph)")
    plt.ylabel("Frequency")
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.6)

    # Display the plot
    plt.show()


def main():
    """
    Main function to drive the application.

    Precondition: User interacts via command line.
    Postcondition: Performs statistical analysis and visualization based on input data.
    """
    print("\nWelcome to the Vehicle Speed Analysis Tool!")
    speeds = import_data()

    # Option to remove outliers
    print("\nWould you like to remove outliers?")
    remove_outliers_option = input("Enter 'yes' or 'no': ").strip().lower()
    if remove_outliers_option == "yes":
        speeds_without_outliers, removed_outliers = remove_outliers(speeds)
        print(f"Outliers removed: {', '.join(map(lambda x: f'{x:.2f}', removed_outliers))}")
        print(f"Dataset size after outlier removal: {len(speeds_without_outliers)} speeds remaining.")
        print(f"List of removed outliers: {list(removed_outliers)}")
    else:
        speeds_without_outliers = speeds
        print("Proceeding with the original data.")

    # Choose a preset percentile or manual input
    print("\nChoose the percentile threshold:")
    print(f"1. EU Standard ({EU_STANDARD_PERCENTILE}%)")
    print(f"2. US Standard ({US_STANDARD_PERCENTILE}%)")
    print("3. Enter a custom percentile.")
    try:
        option = input("Enter 1, 2, or 3: ").strip()
        if option == "1":
            nth_percentile = EU_STANDARD_PERCENTILE
        elif option == "2":
            nth_percentile = US_STANDARD_PERCENTILE
        elif option == "3":
            nth_percentile = int(input("Enter your custom percentile (0-100): "))
            if nth_percentile < 0 or nth_percentile > 100:
                raise ValueError("Percentile must be between 0 and 100.")
        else:
            raise ValueError("Invalid option.")
    except ValueError as e:
        print(f"Error: {e}")
        return main()

    # Perform calculations
    percentile_threshold = calculate_percentile(speeds, nth_percentile)
    recommended_limit = percentile_threshold

    percentile_threshold_no_outliers = calculate_percentile(speeds_without_outliers, nth_percentile)
    recommended_limit_no_outliers = percentile_threshold_no_outliers

    excessive_speeds = find_vehicles_above_threshold(speeds, percentile_threshold)

    # Print results
    print(f"\nAnalysis Results:")
    print(f"- Average Vehicle Speed: {sum(speeds) / len(speeds)} mph")
    print(f"- {nth_percentile}th Percentile Speed: {percentile_threshold:.2f} mph (with outliers)")
    print(f"- {nth_percentile}th Percentile Speed: {percentile_threshold_no_outliers:.2f} mph (without outliers)")
    print(f"- Recommended Speed Limit: {recommended_limit:.2f} mph (with outliers)")
    print(f"- Recommended Speed Limit: {recommended_limit_no_outliers:.2f} mph (without outliers)")
    print(f"- Number of Vehicles Above Threshold: {len(excessive_speeds)}")
    print(f"- Total Vehicles: {len(speeds)}")
    # Visualize the data
    visualize_data(speeds, percentile_threshold, excessive_speeds, nth_percentile)


# Run the program
if __name__ == "__main__":
    main()
