import matplotlib.pyplot as plt

def fcfs(requests, head):
    order = [head] + requests
    movement = sum(
        abs(order[i] - order[i - 1])
        for i in range(1, len(order))
    )
    return requests[:], movement


def sstf(requests, head):
    pending = requests.copy()
    order = []
    current = head
    movement = 0

    while pending:
        nearest = min(pending, key=lambda x: abs(x - current))
        movement += abs(nearest - current)
        order.append(nearest)
        pending.remove(nearest)
        current = nearest

    return order, movement


def scan(requests, head, disk_size, direction="right"):
    pending = sorted(requests)
    left = [r for r in pending if r < head]
    right = [r for r in pending if r >= head]

    order = []
    current = head
    movement = 0

    if direction == "right":
        order = right + [disk_size - 1] + left[::-1]
    else:
        order = left[::-1] + [0] + right

    for position in order:
        movement += abs(position - current)
        current = position

    return order, movement


def plot_movement(head, order, algorithm_name):
    full_order = [head] + order
    plt.figure()
    plt.plot(full_order, range(len(full_order)), marker='o', linestyle='-')
    plt.title(f"Disk Scheduling - {algorithm_name}")
    plt.xlabel("Cylinder Number")
    plt.ylabel("Step")
    plt.gca().invert_yaxis()
    plt.grid(True)
    plt.show()


def main():
    requests = list(map(
        int, input("Enter disk requests separated by spaces: ").split()
    ))
    head = int(input("Enter initial head position: "))
    disk_size = int(input("Enter total number of disk cylinders: "))

    if disk_size <= 0 or not 0 <= head < disk_size:
        print("Invalid disk size or head position.")
        return

    if any(r < 0 or r >= disk_size for r in requests):
        print("All requests must be valid cylinder numbers.")
        return

    if not requests:
        print("No disk requests were entered.")
        return

    algorithms = {
        "FCFS": fcfs(requests, head),
        "SSTF": sstf(requests, head),
        "SCAN": scan(requests, head, disk_size)
    }

    print("\n--- Disk Scheduling Results ---")
    
    # Properly indented inside main() so it can see 'algorithms'
    for name, (order, movement) in algorithms.items():
        print(f"\n{name}")
        print("Service order:", order)
        print("Total head movement:", movement, "cylinders")

        plot_movement(head, order, name)


if __name__ == "__main__":
    main()