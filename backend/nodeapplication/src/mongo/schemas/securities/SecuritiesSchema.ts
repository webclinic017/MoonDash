//Modified
import { Schema } from "mongoose";

export const SecuritiesSchema = new Schema({
  securitiesList: Array,
  securityType: String,
});
