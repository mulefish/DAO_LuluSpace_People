import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import warnings

class CommonThings:
    CSV_TDD = "data/tdd_data.csv"
    ROLLUP_PII_FREE='data/rollup_pii_free.csv'
    ROLLUP_VECTORIZED='data/vectorized_rollup.csv'
    PRECISION=6 # how far to the right of the decimal

class Colors:
    BG_RED = "\x1b[41m"
    BG_CYAN = "\x1b[46m"
    BG_YELLOW = "\x1b[43m"
    BG_GREEN = "\x1b[92m"
    BOLD = "\x1b[1m"
    RESET = "\x1b[0m"

def red(msg):
    print(f"{Colors.BG_RED}{msg}{Colors.RESET}")

def yellow(msg):
    print(f"{Colors.BG_YELLOW}{msg}{Colors.RESET}")

def green(msg):
    print(f"{Colors.BG_GREEN}{msg}{Colors.RESET}")



def normalize_matrix_round_concat(df, precision):
    """
    Normalize all columns including 'sessions' and 'tlv', while preserving their original values.
    Prepend these original values to each row with the names 'ORIGINAL_SESSIONS' and 'ORIGINAL_TLV'.
    Ensure that numbers effectively rounding to 0.0000 are just represented as 0.
    """

    # Preserve original values of 'sessions' and 'tlv'
    original_sessions = df['sessions'].copy()
    original_tlv = df['tlv'].copy()

    scaler = MinMaxScaler()

    # Normalize the entire DataFrame
    normalized_df = pd.DataFrame(scaler.fit_transform(df), columns=df.columns)

    # Define a small threshold based on precision to treat values as zero
    threshold = 10 ** -precision

    # Apply rounding and replace values effectively zero with 0
    format_str = f"{{:.{precision}f}}"  # Construct format string based on precision
    normalized_df = normalized_df.applymap(lambda x: format_str.format(x).rstrip('0').rstrip('.') if abs(x) >= threshold else '0')

    # Prepend original 'sessions' and 'tlv' values to the normalized DataFrame
    normalized_df.insert(0, 'ORIGINAL_TLV', original_tlv)
    normalized_df.insert(0, 'ORIGINAL_SESSIONS', original_sessions)

    return normalized_df
