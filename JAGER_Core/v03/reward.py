def calculate_reward(
    status: str,
    discovery: bool,
    reproduced: bool,
) -> float:

    reward = 0.0

    if status == "FAILED":
        reward += 5.0

    elif status == "DEGRADED":
        reward += 1.0

    if discovery:
        reward += 3.0

    if reproduced:
        reward += 2.0

    return reward
