//Modified
import {
  INSEQuotesServiceInput,
  NSEQuotesRouteController,
} from "@server/routes/services/nsequotes/NSEQuotesRouteController";
import { Logger } from "@utils/logger/Logger";
import Axios from "axios";
import _ from "lodash";

export class NSEQuotes {
  public static async executeService(
    input: INSEQuotesServiceInput
  ): Promise<any> {
    let link = this.getLink(input.symbol);
    try {
      //let cookie = NSEQuotesRouteController.cookie;
      NSEQuotesRouteController.getNewCookie();

      let resp = await Axios.get(link, {
        headers: {
          Cookie: NSEQuotesRouteController.cookie,
        },
      }).catch((er) => {
        console.log(er);
      });

      if (resp) {
        console.log(resp.data);
        return Promise.resolve(resp.data);
      } else {
        let logger = Logger.getLogger();
        logger.error("Response Null");
        throw Error;
      }
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
    console.log(NSEQuotesRouteController.cookie);
    let resp = (
      await Axios.get(link, {
        headers: {
          Cookie: NSEQuotesRouteController.cookie,
        },
      })
    ).data;

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

/*
    const FormData = require('form-data');
    let bodyFormData = new FormData();
    let headers = bodyFormData.getHeaders()
    let cookie = NSEQuotesRouteController.cookie
    headers ["Cookie"] = cookie
*/
