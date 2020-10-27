import { Mongoose, connect, Connection } from "mongoose";
import * as DBConfig from "@configs/MongoDBConfig.json";

import { IMongoConnectionDetails } from "./IMongoConnectionDetails";
export class MongoConnection {
  private DBConnection: IMongoConnectionDetails;

  constructor(IConnDetails?: IMongoConnectionDetails) {
    if (IConnDetails) {
      this.DBConnection = IConnDetails;
    } else {
      let mongoCredentials = this.getMongoCredentials();
      this.DBConnection = {
        connectionURL: DBConfig.connectionURL
          .replace("<username>", mongoCredentials.user)
          .replace("<pass>", mongoCredentials.password),

        connectionOptions: DBConfig.connectionOptions,
      };
    }
  }

  private getMongoCredentials() {
    if (process.env.MONGO_USERNAME && process.env.MONGO_PASSWORD) {
      let user: string = process.env.MONGO_USERNAME;
      let password: string = process.env.MONGO_PASSWORD;

      return {
        user: user,
        password: password,
      };
    } else {
      throw new Error("Error : Mongo User Name and Password Undefined");
    }
  }

  public setDBConnection(IConnDetails: IMongoConnectionDetails) {
    this.DBConnection = IConnDetails;
  }

  public async setDBURL(dbName: string) {
    if (this.DBConnection.connectionOptions) {
      let DBURL =
        this.DBConnection.connectionURL +
        "/" +
        dbName +
        this.DBConnection.connectionOptions;

      return DBURL;
    } else {
      return this.DBConnection.connectionURL + "/" + dbName;
    }
  }

  public async getConnection(dbName: string): Promise<Connection> {
    let DBURL = await this.setDBURL(dbName);
    console.log("Connecting to " + DBURL);
    let mon = await connect(DBURL, {
      useUnifiedTopology: true,
      useNewUrlParser: true,
      useCreateIndex: true,
    });
    let conn = mon.connection;

    return Promise.resolve(conn);
  }
}
