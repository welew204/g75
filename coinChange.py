def calcCoins(denoms, amt):
    dp = [amt + 1] * (amt + 1)
    dp[0] = 0
    for a in range(1, amt+1):
        for d in denoms:
            if a - d >= 0:
                dp[a] = min(dp[a], 1 + dp[a - d])
    return dp[amt] if dp[amt] != amt+1 else -1
