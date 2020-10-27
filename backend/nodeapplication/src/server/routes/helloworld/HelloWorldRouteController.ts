import { Response, Request } from "express";
import { HelloWorld } from "@services/helloworld/HelloWorld";
import { StatusConstants } from "@constants/StatusConstants";
import { AbstractServiceRouteController } from "../services/AbstractServiceRouteController";

export class HelloWorldRouteController extends AbstractServiceRouteController {
  constructor() {
    super("/helloworld");
  }

  public async runService(req: Request, resp: Response): Promise<any> {
    let response = await HelloWorld.wishHello();
    resp.status(StatusConstants.code200).send(response);
  }
}
