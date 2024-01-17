def exist(board, word):
    """
    Check if the word exists in the 2D board. The word can be constructed from letters of 
    sequentially adjacent cell, where “adjacent” cells are those horizontally or vertically neighbouring.
    The same letter cell may not be used more than once.
    """
    if not board:
        return False
    for i in range(len(board)):
        for j in range(len(board[0])):
            if search(board, i, j, word):
                return True,word
    return False

def search(board, i, j, word):
    """
    Depth-first search to find the word starting at position (i,j) in the board.
    """
    if len(word) == 0: # all the characters are checked
        return True
    
    if i<0 or i>=len(board) or j<0 or j>=len(board[0]) or word[0]!=board[i][j]:
        return False
    
    tmp = board[i][j]  # first character is found, check the remaining part
    board[i][j] = -1  # avoid visiting the same cell again

    # check whether can find "word" along one direction
    res = search(board, i+1, j, word[1:]) or search(board, i-1, j, word[1:]) \
    or search(board, i, j+1, word[1:]) or search(board, i, j-1, word[1:])
    
    board[i][j] = tmp  # restore the cell after DFS search
    return res


board = [
    ['A','B','C','E'],
    ['S','F','C','S'],
    ['A','D','E','E']
]

print(exist(board, "ABCCED"))  
print(exist(board, "SEE"))  
print(exist(board, "ABCB"))  
