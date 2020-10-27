//Generated
import { AbstractMongoController } from "../AbstractMongoController";
import { SecuritiesSchema } from "@mongo/schemas/securities/SecuritiesSchema";
import { SecuritiesModel } from "@mongo/models/securities/SecuritiesModel";
import { ISecuritiesSchema } from "@mongo/schemas/securities/ISecuritiesSchema";

export class SecuritiesMongoController extends AbstractMongoController<
  ISecuritiesSchema
> {
  constructor() {
    super(SecuritiesSchema, SecuritiesModel);
  }
}
