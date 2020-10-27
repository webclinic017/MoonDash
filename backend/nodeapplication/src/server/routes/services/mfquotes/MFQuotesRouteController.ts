//Modified
import { Response, Request } from "express";
import { MFQuotes } from "@services/mfquotes/MFQuotes";
import { StatusConstants } from "@constants/StatusConstants";
import { AbstractServiceRouteController } from "../AbstractServiceRouteController";

export class MFQuotesRouteController extends AbstractServiceRouteController {
  constructor() {
    super("/MFQuotes");

    console.log(this.serverLink + "/MFQuotes/Search");
    console.log(this.serverLink + "/MFQuotes/NAV");
    this.router
      .get("/MFQuotes/Search", this.runSearchService.bind(this))
      .bind(this);
    this.router.get("/MFQuotes/NAV", this.NAVService.bind(this)).bind(this);
  }

  public async runService(req: Request, resp: Response): Promise<any> {
    let input: { schemeCode: string } = req.query;
    let response = await MFQuotes.executeService(input);
    resp.status(StatusConstants.code200).send(response);
  }
  public async NAVService(req: Request, resp: Response): Promise<any> {
    let input: { schemeCode: string } = req.query;
    let response = await MFQuotes.getNAV(input);
    resp.status(StatusConstants.code200).send(response);
  }

  public async runSearchService(req: Request, resp: Response): Promise<any> {
    let input: { q: string } = req.query;
    let response = await MFQuotes.executeSearchService(input);
    resp.status(StatusConstants.code200).send(response);
  }
}
