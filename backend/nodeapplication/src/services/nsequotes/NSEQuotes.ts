//Modified
import {
  INSEQuotesServiceInput,
  NSEQuotesRouteController,
} from "@server/routes/services/nsequotes/NSEQuotesRouteController";
import Axios from "axios";
import _ from "lodash";

export class NSEQuotes {
  public static async executeService(
    input: INSEQuotesServiceInput
  ): Promise<any> {
    let link = this.getLink(input.symbol);
    try {
      // FIXME: Cookie in headers, not working use formdata

      let resp = await Axios.get(link, {
        headers: {
          Cookie: NSEQuotesRouteController.cookie,
        },
      });
      console.log(resp);
      return Promise.resolve(resp);
    } catch (error) {
      console.log(error);
      throw Error;
    }
  }

  private static getLink(symbol: string) {
    return "https://www.nseindia.com/api/quote-equity?symbol=" + symbol;
  }
  private static optionChainLink(symbol: string) {
    return "https://www.nseindia.com/api/option-chain-indices?symbol=" + symbol;
  }

  public static async optionDataService(
    input: INSEQuotesServiceInput
  ): Promise<any> {
    let link = this.optionChainLink(input.symbol);
    let resp = (await Axios.get(link)).data;

    let lvl1Cond = await this.conditionOptionChainData(resp);
    // console.log(resp);
    return Promise.resolve(lvl1Cond);
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
