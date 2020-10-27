//Generated
import { AbstractDBRouteController } from "../AbstractDBRouteController";
import { WealthMongoController } from "@mongo/controller/wealth/WealthMongoController";
import { IWealthSchema } from "@mongo/schemas/wealth/IWealthSchema";
import { Finance } from "financejs";
import moment from "moment";

export class WealthRouteController extends AbstractDBRouteController<
  IWealthSchema
> {
  constructor() {
    super("/MainBase/Wealth", new WealthMongoController());
  }

  public async formatDoc(doc: IWealthSchema) {
    // Calculate Current Value of FD

    let finance = new Finance();
    await Promise.all(
      doc.assets.fixedIncome.map(async (fi) => {
        // let periodInYears = fi.period
        let p = fi.investmentValue; // Principle
        let r = fi.rateOfInterest; // ROI

        let n = 4; // Compounding Frequency 1 - Yearly, 4 - Quarterly, 12 - Monthly, 365 - Daily

        let per = moment(new Date()).diff(fi.investmentDate, "days");

        let periodInDays = per;
        let periodInYears = periodInDays / 365;

        fi.currentValue = p * Math.pow(1 + r / (n * 100), n * periodInYears);
        fi.currentValue = Math.round(fi.currentValue * 100) / 100;
      })
    );

    console.log(doc);
    return Promise.resolve(doc);
  }
}
