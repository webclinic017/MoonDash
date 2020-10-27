//Generated
import { AbstractDBRouteController } from "../AbstractDBRouteController";
import { SecuritiesMongoController } from "@mongo/controller/securities/SecuritiesMongoController";
import { ISecuritiesSchema } from "@mongo/schemas/securities/ISecuritiesSchema";

export class SecuritiesRouteController extends AbstractDBRouteController<
  ISecuritiesSchema
> {
  constructor() {
    super("/MainBase/Securities", new SecuritiesMongoController());
  }
}
