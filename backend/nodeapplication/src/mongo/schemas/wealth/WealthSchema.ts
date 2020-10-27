//Modified
import { Schema } from "mongoose";

export const WealthSchema = new Schema({
  //Starts
  _id: { type: String },
  userName: { type: String, required: true, unique: true },

  assets: {
    fixedIncome: [
      {
        investmentValue: Number,
        currentValue: Number,

        investmentDate: Date,
        maturityDate: Date,

        period: Number,

        rateOfInterest: Number,
      },
    ],

    stocks: [
      {
        stockSymbol: String,
        stockName: String,

        investmentValue: Number,
        currentValue: Number,

        investmentDate: Date,

        price: Number,
        quantity: Number,

        currentPrice: Number,
      },
    ],

    mutualFunds: [
      {
        fundSymbol: String,
        fundName: String,

        investmentValue: Number,
        currentValue: Number,

        investmentDate: Date,

        price: Number,
        quantity: Number,

        currentPrice: Number,
      },
    ],
  },

  totalAssets: {
    investedValue: Number,
    currentValue: Number,

    fixedIncomeInvestedValue: Number,
    fixedIncomeCurrentValue: Number,

    equityInvestedValue: Number,
    equityCurrentValue: Number,
  },

  //Ends
});
