import * as APIKeys from "@configs/APIKeys.json";

async function stockValue(tickerName: string) {
  const key = APIKeys.AlphaVantage;
  const alpha = require("alphavantage")({ key: key });

  let data = await alpha.data.intraday(`msft`);

  return Promise.resolve(data);
}
