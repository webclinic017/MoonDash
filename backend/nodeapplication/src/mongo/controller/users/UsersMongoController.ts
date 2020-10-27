//Generated
import { AbstractMongoController } from "../AbstractMongoController";
import { UsersSchema } from "@mongo/schemas/users/UsersSchema";
import { UsersModel } from "@mongo/models/users/UsersModel";
import { IUsersSchema } from "@mongo/schemas/users/IUsersSchema";

export class UsersMongoController extends AbstractMongoController<
  IUsersSchema
> {
  constructor() {
    super(UsersSchema, UsersModel);
  }
}
