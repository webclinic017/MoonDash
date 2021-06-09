import { Component, OnInit, Input, ViewEncapsulation, ViewChild, Output } from '@angular/core';
import { IWealthSchema, IfixedIncomeInfo, IstocksInfo, ImutualFundsInfo } from '../../IWealthSchema';
import { CredentialsService } from '@app/auth/credentials.service';
import { WealthserviceService } from '../../wealthservice/wealthservice.service';
import { NbIconLibraries } from '@nebular/theme';
import { faCoffee } from '@fortawesome/free-solid-svg-icons';
import { Moment } from 'moment';
import * as moment from 'moment';
import { NgForm } from '@angular/forms';
import { ToastService } from '@app/@core/toast/toast.service';
import { FixedincomeListComponent } from '../../lists/fixedincome-list/fixedincome-list.component';
import { StockListComponent } from '../../lists/stock-list/stock-list.component';
import { StockListService } from '@app/pages/analysis/services/stocklist.service';
import { Observable, of } from 'rxjs';
import { finalize, map } from 'rxjs/operators';
import * as accounting from 'accounting';
import { EventEmitter } from '@angular/core';
import * as _ from 'lodash';

@Component({
  selector: 'app-asset-form',
  templateUrl: './asset-form.component.html',
  styleUrls: ['./asset-form.component.css'],
})
export class AssetFormComponent implements OnInit {
  evaIcons: string[] = [];
  faCoffee = faCoffee;
  stocks: Array<string>;
  funds: Array<{ schemeCode: string; schemeName: string }>;
  @Input() selectedStock: string;
  @Input() selectedFund: string;

  //Comes From Parent Wealth Component
  @Input() wealthDocument: IWealthSchema;

  filteredOptions$: Observable<string[]>;
  filteredFundOptions$: Observable<Array<{ schemeCode: string; schemeName: string }>>;
  isLoading = false;

  isFundLoading = false;
  @ViewChild('autoInput') input: any;
  constructor(
    private credentialsService: CredentialsService,
    private wealthservice: WealthserviceService,
    private iconsLibrary: NbIconLibraries,
    private toastservice: ToastService,
    private stockListService: StockListService
  ) {
    this.evaIcons = Array.from(iconsLibrary.getPack('eva').icons.keys());
    this.iconsLibrary.registerFontPack('@fortawesome/free-solid-svg-icons', { iconClassPrefix: 'fa' });
  }

  @Input() selectedForm: string = 'Select Form';
  forms: string[] = ['Fixed Income', 'Stocks', 'Mutual Funds'];

  isFixedIncomeVisible = false;
  isStocksVisible = false;
  isMutualFundsVisible = false;

  fixedIncomeInfo: IfixedIncomeInfo = <any>{
    // investmentValue: 100,
    // investmentDate: new Date(),
    // maturityDate: new Date(),
    // period: 1,
    // rateOfInterest: 1,
    // currentValue: 1
  };

  stocksInfo: IstocksInfo = <any>{};
  mutualFundsInfo: ImutualFundsInfo = <any>{};

  ngOnInit() {
    this.getPeriod();
    this.isLoading = true;
    this.stockListService
      .getStockList()
      .pipe(
        finalize(() => {
          this.isLoading = false;
        })
      )
      .subscribe((stocks: any) => {
        this.stocks = stocks;
      });
    this.filteredOptions$ = of(this.stocks);
  }
  getStock(stock: string) {
    this.selectedStock = stock;
  }
  getFund(fund: string) {
    this.selectedFund = fund;

    let selectedF = this.funds.filter((x) => {
      return x.schemeName === fund;
    });
    this.mutualFundsInfo.fundSymbol = selectedF[0].schemeCode;
  }

  onChange() {
    this.filteredOptions$ = this.getFilteredOptions(this.input.nativeElement.value);
  }
  onFundSymbolChange() {
    this.filteredFundOptions$ = this.getFilteredFundOptions(this.input.nativeElement.value);
    console.log(this.filteredOptions$);
  }

  getFilteredOptions(value: string): Observable<string[]> {
    return of(value).pipe(map((filterString: string) => this.filter(filterString)));
  }
  getFilteredFundOptions(value: string): Observable<Array<{ schemeCode: string; schemeName: string }>> {
    return of(value).pipe(map((filterString: string) => this.filterFund(filterString)));
  }

  private filter(value: string): string[] {
    const filterValue = value.toLowerCase();
    return this.stocks.filter((optionValue) => optionValue.toLowerCase().includes(filterValue));
  }
  private filterFund(value: string): Array<{ schemeCode: string; schemeName: string }> {
    const filterValue = value.toLowerCase();
    this.isFundLoading = true;
    this.stockListService
      .getFundList(filterValue)
      .pipe(
        finalize(() => {
          this.isFundLoading = false;
        })
      )
      .subscribe((funds: any) => {
        this.funds = funds;
        // .map((fund: any) => fund.schemeName);
      });
    return this.funds;
  }
  ngAfterContentChecked() {
    this.getPeriod();
    this.getInvestmentValue();
  }
  changeForm(form: any) {
    if (form == 'Fixed Income') {
      this.isFixedIncomeVisible = true;
      this.isStocksVisible = false;
      this.isMutualFundsVisible = false;
    }

    if (form == 'Stocks') {
      this.isFixedIncomeVisible = false;
      this.isStocksVisible = true;
      this.isMutualFundsVisible = false;
    }

    if (form == 'Mutual Funds') {
      this.isFixedIncomeVisible = false;
      this.isStocksVisible = false;
      this.isMutualFundsVisible = true;
    }
  }

  getPeriod() {
    if (this.fixedIncomeInfo.maturityDate && this.fixedIncomeInfo.investmentDate) {
      let per = moment(this.fixedIncomeInfo.maturityDate).diff(this.fixedIncomeInfo.investmentDate, 'days');
      this.fixedIncomeInfo.period = per;
      return true;
    } else return false;
  }

  getInvestmentValue() {
    if (this.stocksInfo.price && this.stocksInfo.quantity) {
      this.stocksInfo.investmentValue = this.stocksInfo.price * this.stocksInfo.quantity;
      return true;
    } else return false;
  }
  getMFInvestmentValue() {
    if (this.mutualFundsInfo.price && this.mutualFundsInfo.quantity) {
      this.mutualFundsInfo.investmentValue = this.mutualFundsInfo.price * this.mutualFundsInfo.quantity;
      this.mutualFundsInfo.investmentValue = Number(accounting.toFixed(this.mutualFundsInfo.investmentValue, 2));
      return true;
    } else return false;
  }

  resetForm(f: NgForm) {
    f.resetForm();
  }
  async saveForm(f: NgForm) {
    console.log(this.wealthDocument);
    if (this.wealthDocument) {
      if (this.isFixedIncomeVisible) {
        //The push method is a mutating method, ngOnChanges will not be run
        //Therefore we use concat which is non-mutating
        this.wealthDocument.assets.fixedIncome.concat([_.cloneDeep(this.fixedIncomeInfo)]);
      }
      if (this.isStocksVisible) {
        this.wealthDocument.assets.stocks.concat([_.cloneDeep(this.stocksInfo)]);
      }
      if (this.isMutualFundsVisible) {
        this.wealthDocument.assets.mutualFunds.concat([_.cloneDeep(this.mutualFundsInfo)]);
      }

      //-- Save The Document
      try {
        let saved = await this.wealthservice.saveWealthDocument(this.wealthDocument);
        this.toastservice.showWealthAdditionToast();
        f.resetForm();
      } catch (er) {
        console.log(er);
        this.toastservice.showErrorWhileSaving();
      }
    } else {
      this.toastservice.showErrorWhileSaving();
    }
  }

  get username(): string | null {
    const credentials = this.credentialsService.credentials;
    return credentials ? credentials.username : null;
  }
}
