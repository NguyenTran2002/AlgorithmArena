class Solution:
    
    def search(self, nums: list[int], target: int) -> int:
        
        start = 0
        end = len(nums) - 1

        while start <= end:

            mid = start + (end - start) // 2

            if nums[mid] == target:
                return mid

            elif target > nums[mid]:
                start = mid + 1

            else: # target < nums[mid]
                end = mid - 1

        return -1