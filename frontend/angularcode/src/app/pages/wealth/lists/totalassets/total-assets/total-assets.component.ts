import { Component, OnInit } from '@angular/core';
import {
  IWealthSchema,
  ITotalAssets,
  IstocksInfo,
  IfixedIncomeInfo,
  ImutualFundsInfo,
} from '@app/pages/wealth/IWealthSchema';
import { WealthserviceService } from '@app/pages/wealth/wealthservice/wealthservice.service';
import { ToastService } from '@app/@core/toast/toast.service';
import * as moment from 'moment';
import * as accounting from 'accounting';
import { Input, Output, EventEmitter } from '@angular/core';
@Component({
  selector: 'app-total-assets',
  templateUrl: './total-assets.component.html',
  styleUrls: ['./total-assets.component.scss'],
})
export class TotalAssetsComponent implements OnInit {
  // Wealth Document from Parent Component Wealth
  @Input() wealthDocument: IWealthSchema;
  Gain: {
    amount: any;
    percent: any;
  } = {
    amount: 0,
    percent: 0,
  };
  Info: ITotalAssets = {
    currentValue: 0,
    investedValue: 0,
    equityCurrentValue: 0,
    equityInvestedValue: 0,
    fixedIncomeCurrentValue: 0,
    fixedIncomeInvestedValue: 0,
  };
  constructor(private wealthservice: WealthserviceService, private toastservice: ToastService) {}
  calculateGain() {
    this.Gain.amount = this.Info.currentValue - this.Info.investedValue;
    this.Gain.amount = accounting.toFixed(this.Gain.amount, 2);

    this.Gain.percent = accounting.toFixed((this.Gain.amount * 100) / this.Info.investedValue, 2);
  }
  calculateCurrentValue(fi: IfixedIncomeInfo) {
    let p = fi.investmentValue; // Principle
    let r = fi.rateOfInterest; // ROI

    let n = 4; // Compounding Frequency 1 - Yearly, 4 - Quarterly, 12 - Monthly, 365 - Daily

    let per = moment(new Date()).diff(fi.investmentDate, 'days');

    let periodInDays = per;
    let periodInYears = periodInDays / 365;

    fi.currentValue = p * Math.pow(1 + r / (n * 100), n * periodInYears);
    fi.currentValue = Math.round(fi.currentValue * 100) / 100;
    fi.currentValue = Number(accounting.toFixed(fi.currentValue, 2));

    this.Info.fixedIncomeCurrentValue = this.Info.equityCurrentValue + fi.currentValue;
    this.Info.fixedIncomeInvestedValue = this.Info.equityInvestedValue + fi.investmentValue;

    this.Info.currentValue = this.Info.currentValue + fi.currentValue;
    this.Info.currentValue = Number(accounting.toFixed(this.Info.currentValue, 2));

    this.Info.investedValue = this.Info.investedValue + fi.investmentValue;
    this.calculateGain();
  }
  getStockPrice(inf: IstocksInfo) {
    // this.wealthservice.getNSEQuotes(inf.stockSymbol).subscribe((nseData: any) => {
    //   inf.currentPrice = Number(accounting.toFixed(nseData.priceInfo.lastPrice, 2));
    //   inf.currentValue = inf.currentPrice * inf.quantity;
    //   inf.currentValue = Number(accounting.toFixed(inf.currentValue, 2));
    //   this.Info.equityCurrentValue = this.Info.equityCurrentValue + inf.currentValue;
    //   this.Info.equityInvestedValue = this.Info.equityInvestedValue + inf.investmentValue;
    //   this.Info.currentValue = this.Info.currentValue + inf.currentValue;
    //   this.Info.currentValue = Number(accounting.toFixed(this.Info.currentValue, 2));
    //   this.Info.investedValue = this.Info.investedValue + inf.investmentValue;
    //   this.calculateGain();
    // });
  }

  getMFPrice(inf: ImutualFundsInfo) {
    this.wealthservice.getMFNav(inf.fundSymbol).subscribe((data: any) => {
      inf.currentPrice = Number(accounting.toFixed(data.NAV, 3));
      inf.currentValue = inf.currentPrice * inf.quantity;
      inf.currentValue = Number(accounting.toFixed(inf.currentValue, 2));

      this.Info.equityCurrentValue = this.Info.equityCurrentValue + inf.currentValue;
      this.Info.equityInvestedValue = this.Info.equityInvestedValue + inf.investmentValue;

      this.Info.currentValue = this.Info.currentValue + inf.currentValue;
      this.Info.currentValue = Number(accounting.toFixed(this.Info.currentValue, 2));
      this.Info.investedValue = this.Info.investedValue + inf.investmentValue;
      this.calculateGain();
    });
  }

  ngOnInit() {
    this.wealthDocument.assets.stocks.forEach((inf) => {
      this.getStockPrice(inf);
    });
    this.wealthDocument.assets.fixedIncome.forEach((inf) => {
      this.calculateCurrentValue(inf);
    });
    this.wealthDocument.assets.mutualFunds.forEach((inf) => {
      this.getMFPrice(inf);
    });
  }
}
