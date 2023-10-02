class Solution:

    def minEatingSpeed(self, piles: List[int], h: int) -> int:
        
        left = 1
        right = max(piles)

        while left < right:

            mid = left + (right - left) // 2

            if self.can_eat_all(piles, h, mid):
                right = mid

            else:
                left = mid + 1

        return left

    def can_eat_all(self, piles, h, k):

        hours = 0
        
        for pile in piles:

            if pile % k == 0:
                hours += pile // k

            else:
                hours += pile // k + 1

        if hours <= h:
            return True

        return False