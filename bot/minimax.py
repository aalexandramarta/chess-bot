from .eval import get_evaluation
import numpy as np
import chess


def minimax(board, depth, alpha, beta):
    # Terminal node
    if board.is_game_over():
        return get_evaluation(board)

    # Leaf → quiescence search
    if depth == 0:
        return quiescence(board, alpha, beta)

    # White = maximize
    if board.turn == chess.WHITE:
        max_eval = -np.inf
        for move in ordered_moves(board):
            board.push(move)
            eval = minimax(board, depth - 1, alpha, beta)
            board.pop()

            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)

            if beta <= alpha:
                break  # beta cutoff

        return max_eval

    # Black = minimize
    else:
        min_eval = np.inf
        for move in ordered_moves(board):
            board.push(move)
            eval = minimax(board, depth - 1, alpha, beta)
            board.pop()

            min_eval = min(min_eval, eval)
            beta = min(beta, eval)

            if beta <= alpha:
                break  # alpha cutoff

        return min_eval


def quiescence(board, alpha, beta):
    stand_pat = get_evaluation(board)

    if board.turn == chess.WHITE:
        if stand_pat >= beta:
            return beta
        alpha = max(alpha, stand_pat)
    else:
        if stand_pat <= alpha:
            return alpha
        beta = min(beta, stand_pat)

    for move in board.legal_moves:
        if not board.is_capture(move):
            continue

        board.push(move)
        score = quiescence(board, alpha, beta)
        board.pop()

        if board.turn == chess.WHITE:
            alpha = max(alpha, score)
            if alpha >= beta:
                break
        else:
            beta = min(beta, score)
            if beta <= alpha:
                break

    return alpha if board.turn == chess.WHITE else beta


def ordered_moves(board):
    # Captures first (simple but effective)
    return sorted(
        board.legal_moves,
        key=lambda m: board.is_capture(m),
        reverse=True
    )
