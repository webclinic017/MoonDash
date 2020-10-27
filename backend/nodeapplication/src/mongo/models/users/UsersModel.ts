//Generated
import { model } from "mongoose";
import { MainBase } from "@mongo/databases/MainBase";
import { UsersSchema } from "@mongo/schemas/users/UsersSchema";

export const UsersModel = model(
  MainBase.collections.Users,
  UsersSchema,
  MainBase.collections.Users
);
