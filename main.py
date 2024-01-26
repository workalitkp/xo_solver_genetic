import random
import curses

def create_initial_population(population_size=50, chromosome_size=9):
    return [[random.choice(range(9)) for _ in range(chromosome_size)] for _ in range(population_size)]

def compute_fitness_score(chromosome, current_state):
    wins = sum(simulate_game(chromosome, current_state, player=-1) for _ in range(10))
    return wins

def simulate_game(chromosome, current_state, player):
    board = current_state.copy()
    current_player = 1

    for move in chromosome:
        if board[move] == 0:
            board[move] = current_player
            if has_won(board, current_player):
                return 1 if current_player == player else 0
            current_player *= -1

    return 0

def has_won(board, player):
    size = 3  # Size of the Tic Tac Toe board

    # Generate all possible winning combinations in a Tic Tac Toe game
    winning_combinations = []

    # Rows
    for i in range(size):
        winning_combinations.append(tuple(i * size + j for j in range(size)))

    # Columns
    for i in range(size):
        winning_combinations.append(tuple(i + j * size for j in range(size)))

    # Diagonals
    winning_combinations.append(tuple(i * size + i for i in range(size)))
    winning_combinations.append(tuple((i * size + size - 1 - i) for i in range(size)))

    for combination in winning_combinations:
        if all(board[position] == player for position in combination):
            return True

    return False

def assess_move(move, board, player):
    temp_board = board.copy()
    temp_board[move] = player

    if has_won(temp_board, player):
        return 2
    temp_board[move] = -player

    if has_won(temp_board, -player):
        return 1
    return 0

def apply_genetic_algorithm(current_state, population_size=50, generations=50, mutation_rate=0.1):
    population = create_initial_population(population_size)

    for _ in range(generations):
        fitness_scores = [compute_fitness_score(chromosome, current_state) for chromosome in population]
        best_chromosome = population[fitness_scores.index(max(fitness_scores))]
        new_population = [best_chromosome]

        for _ in range(population_size - 1):
            parent1 = random.choice(population)
            parent2 = random.choice(population)
            crossover_point = random.randint(1, len(parent1) - 1)
            child = parent1[:crossover_point] + parent2[crossover_point:]

            if random.uniform(0, 1) < mutation_rate:
                gene_to_mutate = random.randint(0, len(child) - 1)
                child[gene_to_mutate] = random.choice([i for i in range(9) if current_state[i] == 0])

            new_population.append(child)

        population = new_population

    available_moves = [move for move in range(9) if current_state[move] == 0]
    move_scores = [assess_move(move, current_state, -1) for move in available_moves]
    best_move = available_moves[move_scores.index(max(move_scores))]

    return best_move

def render_game_board(stdscr, board):
    stdscr.clear()
    for i in range(0, 9, 3):
        stdscr.addstr("\n")
        stdscr.addstr(" | ".join(map(str, board[i: i + 3])) + "\n")
        if i < 6:
            stdscr.addstr("---------\n")

def is_game_over(board):
    return all(cell != 0 for cell in board)

def get_human_player_move(stdscr, board):
    while True:
        try:
            stdscr.addstr("choose an action:")
            stdscr.refresh()
            move = int(stdscr.getkey())
            if 1 <= move <= 9 and board[move - 1] == 0:
                return move - 1
            else:
                stdscr.addstr("already played !\n")
        except ValueError:
            stdscr.addstr("wrong input !\n")

def game_loop(stdscr):
    game_board = [0] * 9
    current_player = 1

    while 1:
        if has_won(game_board, current_player):
            print("\nyou won !\n" if current_player == 1 else "\nyou lost !\n")
            _ = input()
        if is_game_over(game_board):
            print("\ndraw!")
            _ = input()

        if current_player == 1:
            render_game_board(stdscr, game_board)
            player_move = get_human_player_move(stdscr, game_board)
            game_board[player_move] = current_player
        else:
            opponent_move = apply_genetic_algorithm(current_state=game_board)
            game_board[opponent_move] = current_player


        current_player *= -1

if __name__ == "__main__":
    curses.wrapper(game_loop)