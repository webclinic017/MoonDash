import { Express } from "express";
import { HelloWorldRouteController } from "@server/routes/helloworld/HelloWorldRouteController";
import { AbstractRouteController } from "@server/routes/AbstractRouteController";
import { UsersRouteController } from "@server/routes/databaseaccess/users/UsersRouteController";
import { SecuritiesRouteController } from "@server/routes/databaseaccess/securities/SecuritiesRouteController";
import { WealthRouteController } from "@server/routes/databaseaccess/wealth/WealthRouteController";
import { NSEQuotesRouteController } from "@server/routes/services/nsequotes/NSEQuotesRouteController";
import { MFQuotesRouteController } from "@server/routes/services/mfquotes/MFQuotesRouteController";
export class InitializeRoutes {
  public static async Initialize(app: Express, link: string) {
    let routes = await this.getRoutes(link);

    routes.forEach((rc) => {
      app.use("/", rc.router);
    });
  }

  public static async getRoutes(
    link: string
  ): Promise<Array<AbstractRouteController>> {
    let routes: Array<AbstractRouteController> = [];

    routes.push(new HelloWorldRouteController());
    routes.push(new UsersRouteController());
    routes.push(new SecuritiesRouteController());
    routes.push(new WealthRouteController());
    routes.push(new NSEQuotesRouteController());
    routes.push(new MFQuotesRouteController());
    return Promise.resolve(routes);
  }
}
