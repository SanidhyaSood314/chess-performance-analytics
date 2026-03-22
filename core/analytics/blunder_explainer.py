import chess


def explain_move(board, move, eval_before, eval_after):

    delta = abs(eval_after - eval_before)

    if delta < 150:
        return None

    if board.is_capture(move):
        return "This move loses material."

    if board.gives_check(move):
        return "This move allows a strong attack."

    if delta > 500:
        return "This move loses a decisive advantage."

    return "This move significantly worsens the position."