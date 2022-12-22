from datetime import date, timedelta


def chunk_df(df, n=1000):
    return [df[i:i + n] for i in range(0, df.shape[0], n)]


def yesterday():
    return (date.today() - timedelta(days=1)).strftime("%m-%d-%Y")


def date_today():
    return date.today().strftime("%m-%d-%Y")
