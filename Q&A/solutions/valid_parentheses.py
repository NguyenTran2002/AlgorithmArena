class Solution:
    def valid_parentheses(self, s: str) -> bool:
        
        stack = []

        for p in s:

            if p == '(' or p =='[' or p == '{':
                stack.append(p)

            else:

                if len(stack) == 0:
                    return False

                if p == ')' and stack[-1] != '(':
                    return False

                elif p == ']' and stack[-1] != '[':
                    return False

                elif p == '}' and stack[-1] != '{':
                    return False

                else:
                    stack.pop()

        if len(stack) == 0:
            return True

        return False