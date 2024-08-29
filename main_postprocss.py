import json
import matplotlib.pyplot as plt


with open('/Users/xiayi/Desktop/Current_projects/Integrated optimization design of modular building/python scripts for ICES2024/git_0824/modular-structural-team/Layout_Results/layout1_GA.json', 'r') as file:
    data = json.load(file)


def plot1():
    # Step 2: Extract the x-axis (numbers) and y-axis (fitness values)
    numbers = list(map(int, data.keys()))
    fitness_values = [item['fitness'] for item in data.values()]

    # Step 3: Create the line plot
    plt.figure(figsize=(9, 6))
    plt.plot(numbers, fitness_values, marker='o', color='black')

    # Step 4: Customize the plot
    # plt.title('Fitness Values Over Iterations', fontsize=16)
    plt.xlabel('Iteration Number', fontsize=18)
    plt.ylabel('Fitness Value', fontsize=18)
    # plt.grid(False, linestyle='--', alpha=0.7)

    # Step 5: Improve readability
    plt.xticks(range(0, max(numbers)+1, 5), fontsize=14)  # Show x-axis labels every 5 steps
    plt.yticks(fontsize=14)  # Show x-axis labels every 5 steps
    plt.xlim(0, max(numbers))

    # # Step 6: Add some styling
    # plt.style.use('seaborn')

    # Step 7: Show the plot
    plt.tight_layout()
    plt.show()

plot1()