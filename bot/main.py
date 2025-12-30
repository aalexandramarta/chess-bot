import chess
import numpy as np
import logging

from .opening import play_opening
from .minimax import minimax

logger = logging.getLogger(__name__)


def get_move(board, depth):
    # Opening book
    opening_move = play_opening(board)
    if opening_move:
        logger.info(f"PLAYING OPENING MOVE: {opening_move}")
        return opening_move

    best_move = None

    # Decide once
    is_white = board.turn == chess.WHITE
    best_eval = -np.inf if is_white else np.inf

    for move in board.legal_moves:
        board.push(move)
        eval = minimax(board, depth - 1, -np.inf, np.inf)
        board.pop()

        if is_white:
            if eval > best_eval:
                best_eval = eval
                best_move = move
        else:
            if eval < best_eval:
                best_eval = eval
                best_move = move

    logger.info(f"CHOSEN MOVE: {best_move} WITH EVAL: {best_eval}")
    return best_move
