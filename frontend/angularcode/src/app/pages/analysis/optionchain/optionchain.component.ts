import { Component, OnInit } from '@angular/core';
import { OptionDataService } from '../services/optiondataservice';
import * as _ from 'lodash';

@Component({
  selector: 'app-optionchain',
  templateUrl: './optionchain.component.html',
  styleUrls: ['./optionchain.component.scss'],
})
export class OptionchainComponent implements OnInit {
  Info: any;
  constructor(private service: OptionDataService) {
    this.getOptionData();
  }

  ngOnInit() {}

  async getOptionData() {
    this.Info = await this.service.getNSEIndexOptionQuotes('NIFTY');
    // this.Info = await OptionchainComponent.conditionOptionChainData(this.Info)
    this.Info.forEach((item: any) => {
      let callPriceChange = item.CE.change;
      let callOIChange = item.CE.changeinOpenInterest;

      let putPriceChange = item.PE.change;
      let putOIChange = item.PE.change;

      if (callPriceChange < 0 && callOIChange < 0) {
        item.CE.signal = 'Long Liquidation';
        item.CE.trend = 'Bearish';
      }
      if (callPriceChange < 0 && callOIChange > 0) {
        item.CE.signal = 'Short Buildup';
        item.CE.trend = 'Bearish';
      }
      if (callPriceChange > 0 && callOIChange > 0) {
        item.CE.signal = 'Long Buildup';
        item.CE.trend = 'Bullish';
      }
      if (callPriceChange > 0 && callOIChange < 0) {
        item.CE.signal = 'Short Covering';
        item.CE.trend = 'Bullish';
      }

      //-- Put

      if (putPriceChange < 0 && putOIChange < 0) {
        item.PE.signal = 'Long Liquidation';
        item.PE.trend = 'Bearish';
      }
      if (putPriceChange < 0 && putOIChange > 0) {
        item.PE.signal = 'Short Buildup';
        item.PE.trend = 'Bearish';
      }
      if (putPriceChange > 0 && putOIChange > 0) {
        item.PE.signal = 'Long Buildup';
        item.PE.trend = 'Bullish';
      }
      if (putPriceChange > 0 && putOIChange < 0) {
        item.PE.signal = 'Short Covering';
        item.PE.trend = 'Bullish';
      }

      // PCR
      if (item.PE.openInterest > item.CE.openInterest) {
        item.level = 'Support';
      }
      if (item.PE.openInterest < item.CE.openInterest) {
        item.level = 'Resistance';
      }
    });
    console.log(this.Info);
  }

  public static async conditionOptionChainData(data: any) {
    let expiryDates = data.records.expiryDates;

    let selectedDate = expiryDates[0];

    let allData = data.records.data;
    allData = _.filter(allData, (val) => {
      return val.expiryDate == selectedDate;
    });

    return allData;
  }
}

// Spot Price
// Eliminate OI Smaller Then
// Color Code
// Use symbols
// Other Indices and stocks
// Other Expiries
