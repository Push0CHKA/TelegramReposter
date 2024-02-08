from config.config import FUTURES_DONOR_ID, FUTURES_ID, SPOT_ID


def get_target_chat_id(donor_chat_id: int):
    if int(f"-100{donor_chat_id}") == FUTURES_DONOR_ID:
        return FUTURES_ID
    else:
        return SPOT_ID
