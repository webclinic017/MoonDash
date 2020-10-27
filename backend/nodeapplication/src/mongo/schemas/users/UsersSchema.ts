//Modified
import { Schema } from "mongoose";

export const UsersSchema = new Schema({
  userName: String,
  password: String,
});
