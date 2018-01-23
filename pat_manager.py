import utils

# FIXME: Writing to files is not done asyncronously, these are blocking calls
# that slow down the application!

# TODO: This should not be writting to a text file.

PAT_FILE = 'pats.json'

def add_pats(user_id: str, amount: float):
    pats = load_pats()
    if user_id not in pats:
        pats[user_id] = amount
    else:
        pats[user_id] += amount
    save_pats(pats)


def get_pats(user_id: str) -> float:
    pats = load_pats()
    if user_id in pats:
        return pats[user_id]
    else:
        return 0


def format_pat_count(count: float) -> str:
    if float(count).is_integer():
        return str(int(count))
    else:
        return str(round(count, 1))


def load_pats() -> dict:
    return utils.load_json(PAT_FILE)


def save_pats(pats: dict):
    utils.save_json(PAT_FILE, pats)