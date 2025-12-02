import random


def coin_flip():
    """Simulates a single coin flip and returns 'Heads' or 'Tails'."""
    # random.choice selects a random element from a non-empty sequence
    return random.choice(["Heads", "Tails"])


# Example usage:
result = coin_flip()
print(f"The coin landed on: {result}")

# To simulate multiple flips:
num_flips = 10
print(f"\nSimulating {num_flips} coin flips:")
for _ in range(num_flips):
    print(coin_flip())

