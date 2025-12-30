from .material import get_material
import chess
from . import positions


# -------------------------------
# Helpers
# -------------------------------

def is_endgame(board):
    """Simple endgame detection: no queens on board."""
    queens = (
        len(board.pieces(chess.QUEEN, chess.WHITE)) +
        len(board.pieces(chess.QUEEN, chess.BLACK))
    )
    return queens == 0


def king_safety(board):
    """Very lightweight king safety heuristic."""
    score = 0

    wk = board.king(chess.WHITE)
    bk = board.king(chess.BLACK)

    # Castling bonus
    if wk in (chess.G1, chess.C1):
        score += 40
    if bk in (chess.G8, chess.C8):
        score -= 40

    # Central king penalty in middlegame
    if board.fullmove_number > 10:
        if wk in (chess.E1, chess.D1, chess.E2, chess.D2):
            score -= 50
        if bk in (chess.E8, chess.D8, chess.E7, chess.D7):
            score += 50

    # Pawn shield (simple)
    for sq in (chess.F2, chess.G2, chess.H2):
        if not board.piece_at(sq):
            score -= 10

    for sq in (chess.F7, chess.G7, chess.H7):
        if not board.piece_at(sq):
            score += 10

    return score



# -------------------------------
# Evaluation
# -------------------------------

def get_evaluation(board):
    # --- Game end conditions ---
    if board.is_checkmate():
        # If it's our turn and we're checkmated → bad
        return -9999 if board.turn else 9999

    if board.is_stalemate() or board.is_insufficient_material():
        return 0

    # --- Material ---
    total_material = get_material(board)

    # --- Piece-square tables ---
    pawnsq = sum(positions.pawn[i] for i in board.pieces(chess.PAWN, chess.WHITE))
    pawnsq += sum(
        -positions.pawn[chess.square_mirror(i)]
        for i in board.pieces(chess.PAWN, chess.BLACK)
    )

    knightsq = sum(positions.knight[i] for i in board.pieces(chess.KNIGHT, chess.WHITE))
    knightsq += sum(
        -positions.knight[chess.square_mirror(i)]
        for i in board.pieces(chess.KNIGHT, chess.BLACK)
    )

    bishopsq = sum(positions.bishop[i] for i in board.pieces(chess.BISHOP, chess.WHITE))
    bishopsq += sum(
        -positions.bishop[chess.square_mirror(i)]
        for i in board.pieces(chess.BISHOP, chess.BLACK)
    )

    rooksq = sum(positions.rook[i] for i in board.pieces(chess.ROOK, chess.WHITE))
    rooksq += sum(
        -positions.rook[chess.square_mirror(i)]
        for i in board.pieces(chess.ROOK, chess.BLACK)
    )

    queensq = sum(positions.queen[i] for i in board.pieces(chess.QUEEN, chess.WHITE))
    queensq += sum(
        -positions.queen[chess.square_mirror(i)]
        for i in board.pieces(chess.QUEEN, chess.BLACK)
    )

    # --- King activity ---
    if is_endgame(board) and hasattr(positions, "king_endgame"):
        kingsq = sum(
            positions.king_endgame[i]
            for i in board.pieces(chess.KING, chess.WHITE)
        )
        kingsq += sum(
            -positions.king_endgame[chess.square_mirror(i)]
            for i in board.pieces(chess.KING, chess.BLACK)
        )
    else:
        kingsq = sum(
            positions.king[i]
            for i in board.pieces(chess.KING, chess.WHITE)
        )
        kingsq += sum(
            -positions.king[chess.square_mirror(i)]
            for i in board.pieces(chess.KING, chess.BLACK)
        )

    # --- Mobility ---
    mobility = len(list(board.legal_moves))
    mobility = mobility if board.turn == chess.WHITE else -mobility

    # --- King safety ---
    safety = king_safety(board)

    # --- Final score ---
    eval_score = (
        total_material
        + pawnsq
        + knightsq
        + bishopsq
        + rooksq
        + queensq
        + kingsq
        + safety
        + mobility * 5
    )

    return eval_score
