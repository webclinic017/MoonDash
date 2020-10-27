//Modified
export interface IWealthSchema {
  //Starts
  userName: string;

  assets: {
    fixedIncome: [
      {
        investmentValue: number;
        currentValue: number;

        investmentDate: Date;
        maturityDate: Date;

        period: number;

        rateOfInterest: number;
      }
    ];

    stocks: [
      {
        stockSymbol: String;
        stockName: String;

        investmentValue: number;
        currentValue: number;

        investmentDate: Date;

        price: number;
        quantity: number;

        currentPrice: number;
      }
    ];

    mutualFunds: [
      {
        fundSymbol: String;
        fundName: String;

        investmentValue: number;
        currentValue: number;

        investmentDate: Date;

        price: number;
        quantity: number;

        currentPrice: number;
      }
    ];
  };

  totalAssets: {
    investedValue: number;
    currentValue: number;

    fixedIncomeInvestedValue: number;
    fixedIncomeCurrentValue: number;

    equityInvestedValue: number;
    equityCurrentValue: number;
  };

  //Ends
}
