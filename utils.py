def chunk_df(df, n=1000):
    return [df[i:i + n] for i in range(0, df.shape[0], n)]