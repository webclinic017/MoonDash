//Generated
import { AbstractMongoController } from "../AbstractMongoController";
import { WealthSchema } from "@mongo/schemas/wealth/WealthSchema";
import { WealthModel } from "@mongo/models/wealth/WealthModel";
import { IWealthSchema } from "@mongo/schemas/wealth/IWealthSchema";

export class WealthMongoController extends AbstractMongoController<
  IWealthSchema
> {
  constructor() {
    super(WealthSchema, WealthModel);
    this.idProperty = "userName";
  }
}
