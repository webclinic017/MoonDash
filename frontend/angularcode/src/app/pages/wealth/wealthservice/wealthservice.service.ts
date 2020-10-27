import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { CredentialsService } from '@app/auth';
import { IWealthSchema, IstocksInfo } from '../IWealthSchema';
import { BehaviorSubject } from 'rxjs';

const routes = {
  wealth: '/mainbase/wealth',
  saveWealth: '/mainbase/wealth/save',
  nseQuotes: '/nsequotes',
  nseOptionChain: '/nsequotes/optionchain',
  mfNAV: '/MFQuotes/NAV',
};

@Injectable({
  providedIn: 'root',
})
export class WealthserviceService {
  constructor(private httpClient: HttpClient, private credentialsService: CredentialsService) {}

  callback: any = {};
  // private messageSource = new BehaviorSubject<any>({});
  // currentMessage = this.messageSource.asObservable();

  get username(): string | null {
    const credentials = this.credentialsService.credentials;
    return credentials ? credentials.username : null;
  }
  getWealthDocument() {
    return this.httpClient.get(routes.wealth + '/?id=' + this.username).toPromise();
  }
  saveWealthDocument(doc: IWealthSchema) {
    // doc.assets.stocks.forEach(async (inf) => {
    //   await this.getStockPrice(inf);
    // });
    return this.httpClient.post(routes.saveWealth, doc).toPromise();
  }

  async getStockPrice(inf: IstocksInfo) {
    let nseData = (await this.getNSEQuotes(inf.stockSymbol)) as any;
    inf.currentPrice = nseData.priceInfo.lastPrice;
    inf.currentValue = inf.currentPrice * inf.quantity;
  }
  addCallBack(callback: any) {
    this.callback = callback;
  }

  getMFNav(symbol: string) {
    return this.httpClient.get(routes.mfNAV + '?schemeCode=' + symbol);
  }

  getNSEQuotes(symbol: string) {
    return this.httpClient.get(routes.nseQuotes + '?symbol=' + symbol).toPromise();
  }

  getNSEOptionData(symbol: string) {
    return this.httpClient.get(routes.nseOptionChain + '?symbol=' + symbol).toPromise();
  }
}
