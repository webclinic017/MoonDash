//Modified
import Axios from "axios";

export class MFQuotes {
  public static async executeService(input: {
    schemeCode: string;
  }): Promise<any> {
    let link = this.getLink(input.schemeCode);
    let resp = (await Axios.get(link)).data;
    // console.log(resp);
    return Promise.resolve(resp);
  }

  public static async getNAV(input: { schemeCode: string }) {
    let resp = await MFQuotes.executeService(input);
    return { NAV: resp.data[0].nav };
  }

  public static async executeSearchService(input: { q: string }): Promise<any> {
    let link = this.getSearchLink(input.q);
    let resp = (await Axios.get(link)).data;
    // console.log(resp);
    return Promise.resolve(resp);
  }

  private static getLink(symbol: string) {
    return "https://api.mfapi.in/mf/" + symbol;
  }
  private static getSearchLink(symbol: string) {
    return "https://api.mfapi.in/mf/search?q=" + symbol;
  }
}
