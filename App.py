import os
from Game import Game
from Sudoku import Sudoku

sudoku_folder = os.path.join(os.path.dirname(__file__), "Sudokus")

class App:

    @staticmethod
    def solve_sudoku(sudoku_file, heuristic="FIFO"):
        """Solve a single sudoku with specified heuristic"""
        game = Game(Sudoku(sudoku_file))
        game.show_sudoku()
        if (game.solve(heuristic) and game.valid_solution()):
            game.show_sudoku() #seeing what the end result looks like
            print("Solved!")
            return True
        else:
            game.show_sudoku()
            print("Could not solve this sudoku :(")
            return False

    @staticmethod
    def compare_heuristics(sudoku_file): #comparing all the different heuristics on one sudoko
        
        header = "-" * 80 #this is a seperator line to make a more for structured output
        print(f"\n{header}")
        print(f"COMPARING HEURISTICS FOR: {os.path.basename(sudoku_file)}") #comparison header
        print(header)

        heuristics = ("FIFO", "MRV", "FINALIZED") #different heuristics 
        results = {} #to store results

        for h in heuristics: #looping over heuristics
            print(f"\n{header}")
            print(f"Testing with {h} heuristic:") #test header
            print(header)

            game = Game(Sudoku(sudoku_file)) #creating new Game instance for each of the heuristics
            solved = game.solve(h) and game.valid_solution() #trying to solve the solution and than validating the solution

            results[h] = { #storing the results and the statistics
                "solved": solved,
                "arc_checks": game.arc_checks,
                "constraint_checks": game.constraint_checks,
                "domain_reductions": game.domain_reductions,
            }

        print(f"\n{header}")
        print("COMPARISON SUMMARY") #comparison header
        print(header)
        print( #printing the table header 
            f"{'Heuristic':<15}"
            f"{'Solved':<10}"
            f"{'Arc Checks':<15}"
            f"{'Constraint Checks':<20}"
            f"{'Domain Reductions':<20}"
        )
        print("-" * 80) 

        for h, r in results.items(): #printing results for each heuristic
            print(
                f"{h:<15}"
                f"{'YES' if r['solved'] else 'NO':<10}"
                f"{r['arc_checks']:<15}"
                f"{r['constraint_checks']:<20}"
                f"{r['domain_reductions']:<20}"
            )

        print(header + "\n")
    
    @staticmethod
    def compare_all_sudokus(): #comparing all sudokus with all heuristics 
        header = "-" * 80
        print(f"\n{header}")
        print("COMPARING ALL SUDOKUS WITH ALL HEURISTICS") 
        print(header)
        
        heuristics = ["FIFO", "MRV", "FINALIZED"] #defining the heuristics
        
        sudoku_files = [] #list for storing all sudoko file paths
        for i in range(1, 6):
            for filename in os.listdir(sudoku_folder):
                if str(i) in filename: #select the first file containing the index number
                    sudoku_files.append(os.path.join(sudoku_folder, filename))
                    break
        
        all_results = {} #for storing all the results
        
        for sudoku_file in sudoku_files: #looping over each sudoko file
            sudoku_name = os.path.basename(sudoku_file) #ectracting file name of sudoko
            all_results[sudoku_name] = {} #initializing result dictionary
            
            for heuristic in heuristics: #looping over heuristic
                game = Game(Sudoku(sudoku_file)) #creating new game instance
                solved = game.solve(heuristic) and game.valid_solution() #solving and validating solution
                
                all_results[sudoku_name][heuristic] = { #storing results and statistics
                    'solved': solved,
                    'arc_checks': game.arc_checks,
                    'constraint_checks': game.constraint_checks,
                    'domain_reductions': game.domain_reductions
                }
        
        for sudoku_name in all_results: #printing results for each sudoko
            print(f"\n{'-'*80}")
            print(f"SUDOKU: {sudoku_name}")
            print('-'*80)
            print(f"{'Heuristic':<15} {'Solved':<10} {'Arc Checks':<15} {'Constraint Checks':<20} {'Domain Reductions':<20}")
            print("-"*80)
            
            for heuristic in heuristics: #printing results for each heuristic
                r = all_results[sudoku_name][heuristic]
                solved_str = "YES" if r['solved'] else "NO"
                print(f"{heuristic:<15} {solved_str:<10} {r['arc_checks']:<15} {r['constraint_checks']:<20} {r['domain_reductions']:<20}")
        
        print("\n",header, "\n")
    
    @staticmethod
    def start():
        header = "-" * 80
        while True:
            print(f"\n{header}")
            print("SUDOKU SOLVER WITH HEURISTICS")
            print(f"{header}")
            print("1. Solve a single Sudoku (choose heuristic)")
            print("2. Compare all heuristics on one Sudoku")
            print("3. Compare all heuristics on all Sudokus")
            print("4. Exit")
            print(f"{header}")
            
            choice = input("Enter your choice (1-4): ")
            
            if choice == "1": #solving one sudoko
                file_num = input("Enter Sudoku file (1-5): ")
                print("\nAvailable heuristics:")
                print("1. FIFO (First In First Out)")
                print("2. MRV (Minimum Remaining Values)")
                print("3. FINALIZED (Prioritize finalized neighbours)")
                heuristic_choice = input("Choose heuristic (1-3): ")
                
                heuristic_dic = {"1": "FIFO", "2": "MRV", "3": "FINALIZED"}
                heuristic = heuristic_dic.get(heuristic_choice, "FIFO")
                
                file = None #finding matching sudoko file
                for filename in os.listdir(sudoku_folder):
                    if file_num in filename:
                        file = filename
                if file is not None: #solve sudoko if file found
                    App.solve_sudoku(os.path.join(sudoku_folder, file), heuristic)
                else:
                    print("Invalid choice")
            
            elif choice == "2": #compare heuristics on one sudoko
                file_num = input("Enter Sudoku file (1-5): ") #ask for sudoko file number
                file = None
                for filename in os.listdir(sudoku_folder): #finding matching sudoko file
                    if file_num in filename:
                        file = filename
                if file is not None:
                    App.compare_heuristics(os.path.join(sudoku_folder, file))
                else:
                    print("Invalid choice")
            
            elif choice == "3": #comparing all sudokus
                App.compare_all_sudokus()
            
            elif choice == "4":
                print("Bye Bye!")
                break
            
            else:
                print("Invalid choice, please try again")


if __name__ == "__main__":
    App.start()
    


