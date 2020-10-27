//Modified
export interface IfixedIncomeInfo {
  investmentValue: number;
  currentValue: number;

  investmentDate: Date;
  maturityDate: Date;

  period: number;

  rateOfInterest: number;
}

export interface IstocksInfo {
  stockSymbol: string;
  stockName: string;

  investmentValue: number;
  currentValue: number;

  investmentDate: Date;

  price: number;
  quantity: number;

  currentPrice: number;
}

export interface ImutualFundsInfo {
  fundSymbol: string;
  fundName: string;

  investmentValue: number;
  currentValue: number;

  investmentDate: Date;

  price: number;
  quantity: number;

  currentPrice: number;
}

export interface ITotalAssets {
  investedValue: number;
  currentValue: number;

  fixedIncomeInvestedValue: number;
  fixedIncomeCurrentValue: number;

  equityInvestedValue: number;
  equityCurrentValue: number;
}
export interface IWealthSchema {
  //Starts
  userName: string;

  assets: {
    fixedIncome: [IfixedIncomeInfo];

    stocks: [IstocksInfo];

    mutualFunds: [ImutualFundsInfo];
  };

  totalAssets: ITotalAssets;

  //Ends
}
