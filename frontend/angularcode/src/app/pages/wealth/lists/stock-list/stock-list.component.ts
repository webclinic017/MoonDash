import { Component, EventEmitter, OnInit, Output } from '@angular/core';
import { IstocksInfo, IWealthSchema } from '../../IWealthSchema';
import { WealthserviceService } from '../../wealthservice/wealthservice.service';
import { ToastService } from '@app/@core/toast/toast.service';
import * as _ from 'lodash';
import * as accounting from 'accounting';
import { Input } from '@angular/core';

@Component({
  selector: 'app-stock-list',
  templateUrl: './stock-list.component.html',
  styleUrls: ['./stock-list.component.scss'],
})
export class StockListComponent implements OnInit {
  // Wealth Document from Parent Component Wealth
  @Input() wealthDocument: IWealthSchema;

  // Emit the change back to the parent component
  @Output() wealthChange = new EventEmitter<IWealthSchema>();

  Info: Array<IstocksInfo>;
  constructor(private toastservice: ToastService, private wealthservice: WealthserviceService) {}

  deleteStock(i: number) {
    this.toastservice.showWealthAdditionToast();
    console.log(i);
    this.Info.splice(i, 1);

    console.log(this.wealthDocument);
    this.wealthChange.emit(this.wealthDocument);
  }

  ngOnInit() {
    this.Info = this.wealthDocument.assets.stocks;

    this.Info.forEach(async (val) => {
      await this.getCurrentPrice(val);
    });
  }

  async getCurrentPrice(inf: IstocksInfo) {
    try {
      await this.wealthservice
        .getNSEQuotes(inf.stockSymbol)
        .then((nseData) => {
          console.log(nseData);
        })
        .catch((er) => {
          console.error(er);
        });
    } catch (error) {}
    // inf.currentPrice = Number(accounting.toFixed(nseData.priceInfo.lastPrice, 2));
    // inf.currentValue = inf.currentPrice * inf.quantity;
    // inf.currentValue = Number(accounting.toFixed(inf.currentValue, 2));
  }
}
