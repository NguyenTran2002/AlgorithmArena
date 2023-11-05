class Solution:
    def valid_palindrome_2(self, s: str) -> bool:
        
        i = 0
        j = len(s) - 1

        while i < j:

            if s[i] != s[j]:
                return self.isSimplePalindrome(s, i, j - 1) or\
                self.isSimplePalindrome(s, i + 1, j)

            i += 1
            j -= 1

        return True
        
    def isSimplePalindrome(self, s, i, j):

        while i < j:

            if s[i] != s[j]:
                return False

            i += 1
            j -= 1

        return True