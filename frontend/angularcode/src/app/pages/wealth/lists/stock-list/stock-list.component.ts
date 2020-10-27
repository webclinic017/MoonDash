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
  constructor(private toastservice: ToastService) {}

  deleteStock(i: number) {
    this.toastservice.showWealthAdditionToast();
    console.log(i);
    this.Info.splice(i, 1);

    console.log(this.wealthDocument);
    this.wealthChange.emit(this.wealthDocument);
  }

  ngOnInit() {
    this.Info = this.wealthDocument.assets.stocks;
  }
}
