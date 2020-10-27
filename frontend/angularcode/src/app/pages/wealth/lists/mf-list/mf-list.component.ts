import { Component, OnInit } from '@angular/core';
import { IWealthSchema, IstocksInfo, ImutualFundsInfo } from '../../IWealthSchema';
import { WealthserviceService } from '../../wealthservice/wealthservice.service';
import { ToastService } from '@app/@core/toast/toast.service';
import * as _ from 'lodash';
import * as accounting from 'accounting';
import { Input, Output, EventEmitter } from '@angular/core';

@Component({
  selector: 'app-mf-list',
  templateUrl: './mf-list.component.html',
  styleUrls: ['./mf-list.component.scss'],
})
export class MfListComponent implements OnInit {
  WealthInfo: IWealthSchema;
  Info: Array<ImutualFundsInfo>;
  // Wealth Document from Parent Component Wealth
  @Input() wealthDocument: IWealthSchema;

  // Emit the change back to the parent component
  @Output() wealthChange = new EventEmitter<IWealthSchema>();
  constructor(private wealthservice: WealthserviceService) {}

  getCurrentPrice(inf: ImutualFundsInfo) {
    this.wealthservice.getMFNav(inf.fundSymbol).subscribe((data: any) => {
      inf.currentPrice = Number(accounting.toFixed(data.NAV, 3));
      inf.currentValue = inf.currentPrice * inf.quantity;
      inf.currentValue = Number(accounting.toFixed(inf.currentValue, 2));
    });
  }

  deleteStock(i: number) {
    console.log(i);
    this.Info.splice(i, 1);

    this.wealthChange.emit(this.wealthDocument);
  }

  updateList(doc: IWealthSchema) {
    let newDoc = _.cloneDeep(doc);
    this.WealthInfo = newDoc;
    this.Info = this.WealthInfo.assets.mutualFunds;
    this.Info.forEach((inf) => {
      this.getCurrentPrice(inf);
    });
  }
  ngOnInit() {
    this.Info = this.wealthDocument.assets.mutualFunds;

    // TODO: Also Update the Current Price of funds added from Asset Form
    this.Info.forEach((val) => {
      this.getCurrentPrice(val);
    });
  }
}
