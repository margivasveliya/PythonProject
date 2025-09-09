import os

def export_csv(df, filename: str) -> bytes:
    
    os.makedirs("reports", exist_ok=True)
    df.to_csv(os.path.join("reports", filename), index=True)
    return df.to_csv(index=True).encode("utf-8")
