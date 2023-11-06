class Solution:
    def two_sum(self, nums: list[int], target: int) -> list[int]:
        
        nums_dict = {}

        for i in range(len(nums)):

            complement = target - nums[i]

            if complement in nums_dict:
                return [i, nums_dict[complement]]

            nums_dict[nums[i]] = i