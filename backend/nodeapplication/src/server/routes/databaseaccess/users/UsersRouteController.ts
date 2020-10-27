//Generated
import { AbstractDBRouteController } from "../AbstractDBRouteController";
import { UsersMongoController } from "@mongo/controller/users/UsersMongoController";
import { IUsersSchema } from "@mongo/schemas/users/IUsersSchema";

export class UsersRouteController extends AbstractDBRouteController<
  IUsersSchema
> {
  constructor() {
    super("/MainBase/Users", new UsersMongoController());
  }
}
