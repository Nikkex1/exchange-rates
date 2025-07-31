import pandas as pd

class Fx():

    def __init__(self, base: str, quote: str):
        """Daily euro reference rates by the European Central Bank."""
        
        self.__base = base
        self.__quote = quote

        self.__data = _web_scraper()

    def ref_spot(self):
        """Returns the spot exchange rate."""

        df = self.__calculate().head(1).values[0][0]

        return df
    
    def ref_rates(self):
        """Returns the historical exchange rates."""

        df = self.__calculate()
        col = df.columns[0]
        df.rename(columns={col:f"{self.__base}/{self.__quote}"},inplace=True)

        return df
    
    def __str__(self):
        return f"{self.__base}/{self.__quote} ({self.__labels(self.__base)}, {self.__labels(self.__quote)})"

    def __calculate(self):
        """Calculates the exchange rate in terms of the base and quote currencies."""

        df = self.__data

        # Comparing currency against itself
        if self.__base == self.__quote:
            return (df["USD"] / df["USD"]).to_frame()
        
        # Exchange rate for EUR/x
        elif self.__base == "EUR":
            return df[self.__quote].to_frame()
        
        # Exchange rate for x/EUR
        elif self.__quote == "EUR":
            return (1 / df[self.__base]).round(4).to_frame()
        
        # Exchange rate for x/y (no EUR)
        else:
            return (df[self.__quote] / df[self.__base]).round(4).to_frame()
        
    def __labels(self, label: str):
        """Returns currency name."""

        currency = {"EUR":"Euro",
                    "USD":"US dollar",
                    "JPY":"Japanese yen",
                    "BGN":"Bulgarian lev",
                    "CZK":"Czech koruna",
                    "DKK":"Danish krone",
                    "GBP":"Pound sterling",
                    "HUF":"Hungarian forint",
                    "PLN":"Polish zloty",
                    "RON":"Romanian leu",
                    "SEK":"Swedish krona",
                    "CHF":"Swiss franc",
                    "ISK":"Icelandic krona",
                    "NOK":"Norwegian krone",
                    "TRY":"Turkish lira",
                    "AUD":"Australian dollar",
                    "BRL":"Brazilian real",
                    "CAD":"Canadian dollar",
                    "CNY":"Chinese yuan renminbi",
                    "HKD":"Hong Kong dollar",
                    "IDR":"Indonesian rupiah",
                    "ILS":"Israeli shekel",
                    "INR":"Indian rupee",
                    "KRW":"South Korean won",
                    "MXN":"Mexican peso",
                    "MYR":"Malaysian ringgit",
                    "NZD":"New Zealand dollar",
                    "PHP":"Philippine peso",
                    "SGD":"Singapore dollar",
                    "THB":"Thai baht",
                    "ZAR":"South African rand"}
        
        return currency[label]

def _web_scraper():
    """Reference exchange rates from the ECB."""

    url = "https://www.ecb.europa.eu/stats/eurofxref/eurofxref-hist.zip?c750b601a4ceffb9c260f8007a037a27"
    
    df = pd.read_csv(url,compression="zip")
    index = pd.to_datetime(df["Date"])
    df.set_index(index,inplace=True)
    df.drop(columns=["Date","Unnamed: 42"],inplace=True)

    return df

if __name__ == "__main__":
    eur_usd = Fx(base="EUR",quote="USD")
    eur_jpy = Fx(base="EUR",quote="JPY")

    df = eur_usd.ref_rates()
    series = df.query('"2024-01-01" < index')

    import matplotlib.pyplot as plt

    fig, ax = plt.subplots()

    plt.plot(series)

    plt.show()