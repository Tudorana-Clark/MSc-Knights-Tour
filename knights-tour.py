"""
Task 1: Knight's Tour Problem
Author: Daniel Tudorana-Clark
Subject: MSc Computer Science - Data Structure and Algorithms 2
Date: November 2025

This program implements the Knight's Tour problem in its closed version,
where the knight must return to the starting square after visiting all squares.
Two approaches are implemented: Las Vegas and Backtracking.
"""

import random
from typing import Tuple, List

# Global constants for the board
BOARD_SIZE = 8

# Knight's possible moves (8 directions)
KNIGHT_MOVES = [
    (2, 1), (2, -1), (-2, 1), (-2, -1),
    (1, 2), (1, -2), (-1, 2), (-1, -2)
]

def display_board(board: List[List[int]], title: str = "Chessboard") -> None:
    """
    Display the chess board with knight's path
    
    Numbers represent the order of movements (1st move, 2nd move, etc.)
    Unvisited cells are marked with 0
    """
    print(f"\n{title}:")
    print("      ", end="")
    # Print column headers
    for i in range(BOARD_SIZE):
        print(f"{i:3}", end="")
    print()
    print("    " + "---" * (BOARD_SIZE + 1))
    
    for i in range(BOARD_SIZE):
        # Print row header
        print(f"{i} |", end="")
        for j in range(BOARD_SIZE):
            if board[i][j] == 0:
                print(f"  0", end="")  # Unvisited squares marked with 01
            else:
                print(f"{board[i][j]:3}", end="")  # Movement order
        print()
    print()
    
    # Count visited squares
    visited_count = sum(1 for i in range(BOARD_SIZE) 
                        for j in range(BOARD_SIZE) if board[i][j] > 0)
    print(f"Visited squares: {visited_count}/{BOARD_SIZE * BOARD_SIZE}")

# Check if the move is valid (within bounds and unvisited)
def is_valid_move(x: int, y: int, board: List[List[int]]) -> bool:
    return (0 <= x < BOARD_SIZE and 
            0 <= y < BOARD_SIZE and 
            board[x][y] == 0)

# Get all valid moves from current position
def get_valid_moves(x: int, y: int, board: List[List[int]]) -> List[Tuple[int, int]]:
    valid_moves = []
    for dx, dy in KNIGHT_MOVES:
        new_x, new_y = x + dx, y + dy
        if is_valid_move(new_x, new_y, board):
            valid_moves.append((new_x, new_y))
    return valid_moves

# Count number of valid moves from a given position (for Warnsdorff's rule)
def count_onward_moves(x: int, y: int, board: List[List[int]]) -> int:
    return len(get_valid_moves(x, y, board))

# Get valid moves sorted by Warnsdorff's rule (fewest onward moves first)
def get_sorted_moves(x: int, y: int, board: List[List[int]]) -> List[Tuple[int, int]]:
    valid_moves = get_valid_moves(x, y, board)
    
    # Sort by number of onward moves (ascending order)
    valid_moves.sort(key=lambda move: count_onward_moves(move[0], move[1], board))
    
    return valid_moves

# Check if knight can return to starting position for closed tour
def is_closed_tour(current_pos: Tuple[int, int], start_pos: Tuple[int, int]) -> bool:
    x, y = current_pos
    start_x, start_y = start_pos
    
    for dx, dy in KNIGHT_MOVES:
        if x + dx == start_x and y + dy == start_y:
            return True
    return False


# == REQUIRED FUNCTION SIGNATURE 1 ==
def KnightsTourLasVegas(startingPosition: Tuple[int, int]) -> Tuple[bool, List[List[int]]]:
    """
    Las Vegas approach for Knight's Tour
    
    The Las Vegas algorithm uses random selection of moves.
    End conditions:
    - Tour completed successfully (all 64 squares visited and can return to start)
    - Knight steps in already-visited square (unsuccessful)
    - Knight runs out of valid moves
    
    Args:
        startingPosition: Starting position as (row, col) tuple
        
    Returns:
        Tuple of (success_flag, board_state)
    """
    board = [[0 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    
    x, y = startingPosition
    move_count = 1
    board[x][y] = move_count
    current_x, current_y = x, y
    
    total_squares = BOARD_SIZE * BOARD_SIZE
    
    # Continue until we visit all squares or get stuck
    while move_count < total_squares:
        valid_moves = get_valid_moves(current_x, current_y, board)
        
        if not valid_moves:
            # No valid moves available - unsuccessful
            break
        
        # Las Vegas: randomly select next move
        next_x, next_y = random.choice(valid_moves)
        move_count += 1
        board[next_x][next_y] = move_count
        current_x, current_y = next_x, next_y
    
    # Check if we completed the tour and can return to start (closed tour)
    success = (move_count == total_squares and 
               is_closed_tour((current_x, current_y), startingPosition))
    
    return success, board


# == REQUIRED FUNCTION SIGNATURE 2 ==
def KnightsTourBacktracking(startingPosition: Tuple[int, int]) -> Tuple[bool, List[List[int]]]:
    """
    Backtracking approach for Knight's Tour
    
    This algorithm systematically tries all possible paths and backtracks
    when it reaches a dead end. It guarantees finding a solution if one exists.
    
    Args:
        startingPosition: Starting position as (row, col) tuple
        
    Returns:
        Tuple of (success_flag, board_state)
    """
    board = [[0 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    total_squares = BOARD_SIZE * BOARD_SIZE
    
    # This is the recursive helper function
    def backtrack(x: int, y: int, move_count: int) -> bool:
        """
        Recursive backtracking function
        
        Args:
            x, y: Current position
            move_count: Number of moves made so far
            
        Returns:
            True if a closed tour is found, False otherwise
        """
        # Base case: all squares visited, check if we can return to start
        if move_count == total_squares:
            return is_closed_tour((x, y), startingPosition)
        
        # Get moves sorted by Warnsdorff's rule (try moves with fewer onward options first)
        sorted_moves = get_sorted_moves(x, y, board)
        
        for next_x, next_y in sorted_moves:
            # Make the move
            board[next_x][next_y] = move_count + 1
            
            # Recursively try to complete the tour from this new position
            if backtrack(next_x, next_y, move_count + 1):
                return True
            
            # Backtrack: undo the move if it doesn't lead to solution
            board[next_x][next_y] = 0
        
        # No valid moves from this position lead to a solution
        return False
    
    # Initialize starting position
    x, y = startingPosition
    board[x][y] = 1
    
    # Start the backtracking algorithm
    success = backtrack(x, y, 1)
    
    return success, board


def main():
    """Main program loop"""
    
    # Requirement 1.a: Create and display an empty chessboard
    empty_board = [[0 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    display_board(empty_board, title="Empty Chessboard - Knight's Movement Space")
    
    while True:
        # Requirement 1.b: Manage input from the user
        print("\n=== Knight's Tour - Closed Version ===")
        print("Choose an algorithm:")
        print("1. Las Vegas")
        print("2. Backtracking")
        print("3. Exit")
        
        algorithm = ""
        start_pos = (0, 0)
        
        choice = input("\nEnter your choice (1/2/3): ").strip()
        
        if choice == "3":
            print("Thank you for using Knight's Tour program!")
            break # Exit main loop
        elif choice in ["1", "2"]:
            algorithm = "las_vegas" if choice == "1" else "backtracking"
            
            # Get starting position
            while True:
                try:
                    x = int(input(f"Enter starting row (0-{BOARD_SIZE - 1}): "))
                    y = int(input(f"Enter starting column (0-{BOARD_SIZE - 1}): "))
                    
                    if 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE:
                        start_pos = (x, y)
                        break # Exit position loop
                    else:
                        print(f"Invalid position. Please enter values between 0-{BOARD_SIZE - 1}.")
                except ValueError:
                    print("Invalid input. Please enter integers only.")
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")
            continue # Restart main loop
            
        
        # --- Run the selected algorithm ---
        print(f"\nStarting {algorithm.replace('_', ' ').title()} algorithm from position {start_pos}")
        print("Processing... (This may take a moment for backtracking)")
        
        success = False
        final_board = []
        
        if algorithm == "las_vegas":
            success, final_board = KnightsTourLasVegas(start_pos)
        else:  # backtracking
            success, final_board = KnightsTourBacktracking(start_pos)
        
        # Requirement 1.c: Visualization of results
        print(f"\n{'='*50}")
        print(f"TOUR RESULT: {'SUCCESSFUL' if success else 'FAILED'}")
        print(f"{'='*50}")
        
        # Display the board showing all visited squares
        display_board(final_board, 
                      title=f"Final Board - {algorithm.replace('_', ' ').title()} Algorithm")
        
        if success:
            print("🎉 Congratulations! The knight completed a CLOSED tour!")
            print(f"   The knight visited all {BOARD_SIZE*BOARD_SIZE} squares and can return to the starting position.")
        else:
            print("❌ The knight could not complete a closed tour.")
            visited = sum(1 for row in final_board for cell in row if cell > 0)
            print(f"   The knight visited {visited} out of {BOARD_SIZE*BOARD_SIZE} squares before getting stuck.")
        
        # Ask if user wants to continue
        print("\n" + "-"*50)
        continue_choice = input("Would you like to try again? (y/n): ").strip().lower()
        if continue_choice != 'y':
            print("Thank you for using Knight's Tour program!")
            break # Exit main loop

 # Test function to compare success rates of both algorithms
def run_success_test(runs: int = 10000, start_pos: Tuple[int, int] = (0, 0)):
    """
    Runs a batch test to determine the success rate of
    Las Vegas vs. Backtracking algorithms.
    """
    print(f"\n{'='*60}")
    print(f"  RUNNING SUCCESS RATE TEST")
    print(f"  Total Runs per Algorithm: {runs}")
    print(f"  Start Position: {start_pos}")
    print(f"{'='*60}")

    # --- 1. Test Las Vegas ---
    print(f"\n[Testing Las Vegas Algorithm...]")
    print(f"This will run {runs} times. Please wait...")
    lv_success_count = 0
    
    for i in range(runs):
        # Print progress update every 10%
        if (i + 1) % (runs // 10) == 0:
            print(f"  ...Las Vegas run {i+1}/{runs} complete.")
            
        success, _ = KnightsTourLasVegas(start_pos)
        if success:
            lv_success_count += 1
    
    lv_rate = (lv_success_count / runs) * 100
    print(f"\n--- Las Vegas Results ---")
    print(f"  Successful Tours: {lv_success_count} / {runs}")
    print(f"  Success Rate: {lv_rate:.4f}%")


    # --- 2. Test Backtracking ---
    print(f"\n[Testing Backtracking Algorithm...]")
    # We only need a few runs to prove it's deterministic.
    # Running it 10,000 times would be very slow and unnecessary.
    bt_test_runs = 5
    print(f"This will run {bt_test_runs} times to confirm consistency...")
    bt_success_count = 0
    
    for i in range(bt_test_runs):
        print(f"  ...Backtracking run {i+1}/{bt_test_runs}...")
        success, _ = KnightsTourBacktracking(start_pos)
        if success:
            bt_success_count += 1

    bt_rate = (bt_success_count / bt_test_runs) * 100
    print(f"\n--- Backtracking Results ---")
    print(f"  Successful Tours: {bt_success_count} / {bt_test_runs}")
    print(f"  Success Rate: {bt_rate:.1f}%")
    if bt_rate == 100.0:
        print(f"  (This confirms the algorithm is deterministic and will be 100% for all {runs} runs)")
    
    print(f"\n{'='*60}\n  TEST COMPLETE\n{'='*60}")       


if __name__ == "__main__":
    # --- Run the main interactive program ---
    main() 
    
    # --- Run the 10,000-run success test instead ---
    # To run this, comment out main() above and uncomment the line below:
    
    run_success_test(runs=10000, start_pos=(0, 0))
