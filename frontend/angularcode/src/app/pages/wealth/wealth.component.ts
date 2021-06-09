import { Component, OnInit } from '@angular/core';
import { ToastService } from '@app/@core/toast/toast.service';
import { CredentialsService } from '@app/auth/credentials.service';
import { NbWindowService, NbDialogService } from '@nebular/theme';
import * as accounting from 'accounting';
import { AssetFormComponent } from './forms/asset-form/asset-form.component';
import { IstocksInfo, IWealthSchema } from './IWealthSchema';
import { WealthserviceService } from './wealthservice/wealthservice.service';

@Component({
  selector: 'app-wealth',
  templateUrl: './wealth.component.html',
  styleUrls: ['./wealth.component.css'],
})
export class WealthComponent implements OnInit {
  //The Master Document
  wealthDocument: IWealthSchema;

  constructor(
    private dialogService: NbDialogService,
    private wealthservice: WealthserviceService,
    private credentialsService: CredentialsService,
    private toastservice: ToastService
  ) {
    this.wealthservice
      .getWealthDocument()
      .then((wealthInfoDocs: Array<IWealthSchema>) => {
        if (wealthInfoDocs && wealthInfoDocs.length != 0) {
          this.wealthDocument = wealthInfoDocs[0];
        } else {
          this.initializeBlankWealthDoc();
        }
      })
      .catch((er) => {
        toastservice.showErrorWhileRetrieving();
      });
  }

  //Opens The form
  openAssetWindowForm() {
    let dialog = this.dialogService.open(AssetFormComponent, {
      context: {
        wealthDocument: this.wealthDocument,
      } as any,
    });

    dialog.onClose.subscribe((x: any) => {
      this.wealthDocument = dialog.componentRef.instance.wealthDocument;
    });
  }

  async onWealthChange(event: IWealthSchema) {
    this.wealthDocument = event;

    //-- Save The Document
    try {
      let saved = await this.wealthservice.saveWealthDocument(this.wealthDocument);
      this.toastservice.showSuccessWhileDeleting();
    } catch (er) {
      console.log(er);
      this.toastservice.showErrorWhileDeleting();
    }
  }

  async getStockPrice(inf: IstocksInfo) {
    let nseData = (await this.wealthservice.getNSEQuotes(inf.stockSymbol)) as any;
    inf.currentPrice = Number(accounting.toFixed(nseData.priceInfo.lastPrice, 2));
    inf.currentValue = inf.currentPrice * inf.quantity;
    inf.currentValue = Number(accounting.toFixed(inf.currentValue, 2));
  }

  initializeBlankWealthDoc() {
    this.wealthDocument = {
      userName: this.username,
      assets: {
        fixedIncome: <any>[],
        stocks: <any>[],
        mutualFunds: <any>[],
      },
      totalAssets: {
        currentValue: 0,
        investedValue: 0,
        equityCurrentValue: 0,
        equityInvestedValue: 0,
        fixedIncomeCurrentValue: 0,
        fixedIncomeInvestedValue: 0,
      },
    };
  }

  get username(): string | null {
    const credentials = this.credentialsService.credentials;
    return credentials ? credentials.username : null;
  }

  ngOnInit() {
    // this.toastservice.showWealthAdditionToast();
  }
}
