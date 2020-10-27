import { Component, OnInit } from '@angular/core';
import { WealthserviceService } from '../../wealthservice/wealthservice.service';
import { IWealthSchema, IstocksInfo, IfixedIncomeInfo } from '../../IWealthSchema';
import { ToastService } from '@app/@core/toast/toast.service';
import * as moment from 'moment';
import * as _ from 'lodash';
import { Input, Output, EventEmitter } from '@angular/core';
@Component({
  selector: 'app-fixedincome-list',
  templateUrl: './fixedincome-list.component.html',
  styleUrls: ['./fixedincome-list.component.css'],
})
export class FixedincomeListComponent implements OnInit {
  Info: Array<IfixedIncomeInfo>;
  WealthInfo: IWealthSchema;

  // Wealth Document from Parent Component Wealth
  @Input() wealthDocument: IWealthSchema;

  // Emit the change back to the parent component
  @Output() wealthChange = new EventEmitter<IWealthSchema>();
  constructor() {}

  ngOnInit() {
    this.Info = this.wealthDocument.assets.fixedIncome;

    // TODO: Update the Current Value on Addition from Asset Form
    this.Info.forEach((val) => {
      this.calculateCurrentValue(val);
    });
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
  }

  deleteStock(i: number) {
    console.log(i);
    this.Info.splice(i, 1);
    this.wealthChange.emit(this.wealthDocument);
  }
}
