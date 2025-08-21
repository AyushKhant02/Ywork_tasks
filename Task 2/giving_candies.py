class Solution(object):
    def candy(self, ratings):
        n = len(ratings)
        candies = [1] * n  # everyone gets at least 1 candy

        # Keep updating until stable (because both neighbors matter)
        changed = True
        while changed:
            changed = False
            for i in range(n):
                # Check left neighbor
                if i > 0 and ratings[i] > ratings[i - 1] and candies[i] <= candies[i - 1]:
                    candies[i] = candies[i - 1] + 1
                    changed = True

                # Check right neighbor
                if i < n - 1 and ratings[i] > ratings[i + 1] and candies[i] <= candies[i + 1]:
                    candies[i] = candies[i + 1] + 1
                    changed = True

        print("Ratings:      ", ratings)
        print("Distribution: ", candies)
        print("Total Candies:", sum(candies))
        return sum(candies)


ratings = [3, 2, 1]
Solution().candy(ratings)
