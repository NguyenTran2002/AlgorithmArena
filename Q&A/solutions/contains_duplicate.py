class Solution:
    
    def contains_duplicate(self, nums: list[int]) -> bool:
        
        nums_set = set()

        for item in nums:

            if item in nums_set:
                return True

            else:
                nums_set.add(item)

        return False