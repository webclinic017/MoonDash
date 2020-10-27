//Generated
import { model } from "mongoose";
import { MainBase } from "@mongo/databases/MainBase";
import { SecuritiesSchema } from "@mongo/schemas/securities/SecuritiesSchema";

export const SecuritiesModel = model(
  MainBase.collections.Securities,
  SecuritiesSchema,
  MainBase.collections.Securities
);
