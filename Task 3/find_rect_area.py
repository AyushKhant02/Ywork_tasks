class Solution:
    def maximalRectangle(self, matrix):
        if not matrix:
            return 0, 0  # area, count
        
        n = len(matrix[0])
        heights = [0] * (n + 1)  # extra 0 for stack processing
        max_area = 0
        count = 0

        for row in matrix:
            # update histogram heights
            for i in range(n):
                heights[i] = heights[i] + 1 if row[i] == "1" else 0

            stack = [-1]
            for i in range(n + 1):
                while heights[i] < heights[stack[-1]]:
                    h = heights[stack.pop()]
                    w = i - stack[-1] - 1
                    area = h * w

                    if area > max_area:
                        max_area = area
                        count = 1
                    elif area == max_area:
                        count += 1

                stack.append(i)
        
        return max_area, count


# Example usage
matrix = [
  ["1","1","1","1","1"],
  ["1","1","1","1","1"],
  ["1","1","0","1","1"],
  ["1","1","1","1","1"],
  ["1","1","1","1","1"]
]
area, cnt = Solution().maximalRectangle(matrix)
print(f"Maximum Area: {area}, Count: {cnt}")
