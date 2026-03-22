import math


def calculate_separate_accuracy(analysis_data):

    white_loss = 0
    black_loss = 0
    white_moves = 0
    black_moves = 0

    # ---------------------------------
    # Helper: Stable CP loss
    # ---------------------------------

    def compute_cp_loss(best_eval, eval_after):

        # Handle mate scores
        if abs(best_eval) >= 9000 or abs(eval_after) >= 9000:
            return 1000  # cap mate impact

        loss = abs(best_eval - eval_after)

        # Cap extreme values
        return min(loss, 1000)

    # ---------------------------------
    # Compute losses
    # ---------------------------------

    for move in analysis_data:

        cp_loss = compute_cp_loss(
            move.best_eval,
            move.eval_after
        )

        if move.is_white_move:
            white_loss += cp_loss
            white_moves += 1
        else:
            black_loss += cp_loss
            black_moves += 1

    # ---------------------------------
    # Accuracy conversion
    # ---------------------------------

    def convert_to_accuracy(avg_loss):
        return 100 * math.exp(-avg_loss / 300)

    white_avg = white_loss / white_moves if white_moves else 0
    black_avg = black_loss / black_moves if black_moves else 0

    white_accuracy = round(convert_to_accuracy(white_avg), 2)
    black_accuracy = round(convert_to_accuracy(black_avg), 2)

    return white_accuracy, black_accuracy