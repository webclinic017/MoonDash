//Generated
import { model } from "mongoose";
import { MainBase } from "@mongo/databases/MainBase";
import { WealthSchema } from "@mongo/schemas/wealth/WealthSchema";

export const WealthModel = model(
  MainBase.collections.Wealth,
  WealthSchema,
  MainBase.collections.Wealth
);
