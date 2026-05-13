#Ben Bornebusch s1134580
#Beyzanur Kivir s1147793

class Game:

    def __init__(self, sudoku):
        self.sudoku = sudoku

        self.arc_checks = 0 #how many arcs processed
        self.domain_reductions = 0 #how many values removed from domains
        self.constraint_checks = 0 #how many individual constraint checks
        self.heuristic = "FIFO"  # default heuristic

    def show_sudoku(self):
        print(self.sudoku)
    
    def solve(self, heuristic="FIFO") -> bool:
        
        self.heuristic = heuristic
        
        #resetting metrics at the start
        self.arc_checks = 0
        self.domain_reductions = 0
        self.constraint_checks = 0

        queue = [] #initializing empty list to later on save all the arcs
        board = self.sudoku.get_board() #getting the 9x9 board from the sudoku object 

        # adding all the arcs to the queue
        for row in range(9): #loop through all rows
            for col in range(9): #loop through all columns
                field = board[row][col] #getting current field
                neighbours = field.get_neighbours() #getting all the neighbours of the field
                for neighbour in neighbours: #for each of the neighbours we are going to create an arc and add to the queue
                    arc = (field, neighbour) #arc is saved as tuple
                    queue.append(arc) #adding arc to queue
        
        start_size_of_queue = len(queue) #this is for the metric to keep track of the initial size of the queue

        #processing the queue with selected heuristic
        while len(queue) > 0: #while there are still arcs not processed
            #Select next arc based on heuristic
            if self.heuristic == "FIFO":
                field, neighbour = queue.pop(0)  #FIFO: first in, first out
            elif self.heuristic == "MRV":
                #Minimum Remaining Values: prioritize arcs with smallest domain fields
                min_index = 0
                min_domain_size = 10
                for i in range(len(queue)):
                    f, n = queue[i]
                    if not f.is_finalized():
                        domain_size = f.get_domain_size()
                        if domain_size < min_domain_size:
                            min_domain_size = domain_size
                            min_index = i
                field, neighbour = queue.pop(min_index)
            elif self.heuristic == "FINALIZED":
                #Prioritize arcs where neighbour is finalized
                finalized_index = -1
                for i in range(len(queue)):
                    f, n = queue[i]
                    if n.is_finalized():
                        finalized_index = i
                        break
                if finalized_index != -1:
                    field, neighbour = queue.pop(finalized_index)
                else:
                    field, neighbour = queue.pop(0)  #fallback to FIFO
            else:
                field, neighbour = queue.pop(0)  #default FIFO
            
            self.arc_checks += 1 #counting how many arcs been processed
            revised = False #tracking if domain of field was modified
            
            if not field.is_finalized(): #only revising if field not already finalized
                if neighbour.is_finalized(): #either the neighbour already has a definite value...
                    value_neighbour = neighbour.get_value()
                    if value_neighbour in field.get_domain(): #if the neighbours value is in field's domain remove it
                        field.remove_from_domain(value_neighbour)
                        self.domain_reductions += 1 #counting the domain reductions
                        revised = True #marking that we changed that domain
                else: #... or the neighbour is not finalized 
                    domain_copy_of_field = field.get_domain().copy() #making copy of fields domain
                    for value_field in domain_copy_of_field:
                        compatible = False
                        for neighbour_value in neighbour.get_domain(): #checking if any value in the domain of the neighbour is different from the value_field
                            self.constraint_checks += 1 #counting the constraint checks
                            if value_field != neighbour_value:
                                compatible = True#found a compatible value
                                break #dont check any further
                        if not compatible: #if no compatible value exists (neighbour has the same value) the value gets removed from the field's domain
                            field.remove_from_domain(value_field)
                            self.domain_reductions += 1 #counting the domain reductions
                            revised = True #marking that we changed the domain
            
            if revised:
                if field.get_domain_size() == 0:#checking if domain is empty
                    return False #no solution exists
                
                other_neighbours = field.get_other_neighbours(neighbour)#getting all the neighbours of field except the one that was just processed
                for other_neighbour in other_neighbours: #adding arcs from each of the other neighbours back to the field
                    queue.append((other_neighbour, field))  #since field domain changed they would need to be rechecked


        print(f"\n------------------Complexity Analysis (Heuristic: {self.heuristic})------------------")
        print(f"Initial queue size: {start_size_of_queue}")
        print(f"Total arc checks: {self.arc_checks}")
        print(f"Total constraint checks: {self.constraint_checks}")
        print(f"Domain reductions: {self.domain_reductions}")
        print("---------------------------------------------------------------------------------------\n")

        return True #true means that the AC-3 completed without finding any contradictions
    
    def valid_solution(self) -> bool:
        
        board = self.sudoku.get_board() #getting the board
        
        for row in range(9):
            for col in range(9):
                if not board[row][col].is_finalized(): #verifying if all of the fields are finalized
                    return False #found an empty field --> not complete
        
        
        for row in range(9): #checking if rows dont have a duplicate
            values_row = [] #storing all values of that row
            for col in range(9): #collecting all values in this row
                values_row.append(board[row][col].get_value())
            seen_values_row = [] #checking for duplicates using another list
            for value in values_row:
                if value in seen_values_row:
                    return False #found a duplicate which means it is invalid
                seen_values_row.append(value) #adding value to seen list
        

        for col in range(9): #checking if all columns dont have a duplicate
            values_col = [] #storing all values in that column
            for row in range(9): #collecting all values in that column
                values_col.append(board[row][col].get_value())
            seen_values_col = [] #checking duplicates with another list
            for value in values_col:
                if value in seen_values_col:
                    return False #found duplicate which means its invalid 
                seen_values_col.append(value) #adding value to seen list
        
    
        for box_row in range(0, 9, 3): #looping through all the three by three boxes
            for box_col in range(0, 9, 3):
                values_box = [] #storing all the values in this list
                for row in range(box_row, box_row + 3): #collecting all values in the three by three
                    for col in range(box_col, box_col + 3): 
                        values_box.append(board[row][col].get_value())
                seen_values_box = [] #checking for duplicates using another list
                for value in values_box:
                    if value in seen_values_box:
                        return False #if there is a duplicate the sudoku is invalid
                    seen_values_box.append(value) #adding value to seen list
        
        return True #all check passed the sudoku must be valid