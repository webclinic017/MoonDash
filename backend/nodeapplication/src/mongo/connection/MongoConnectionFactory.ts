import { IMongoDatabaseConnection } from "./IMongoDatabaseConnection";
import { MongoConnection } from "./MongoConnection";
import { Connection } from "mongoose";
import { DatabaseList } from "@mongo/databases/DatabaseList";
import _ from "lodash";

export class MongoConnectionFactory {
  private static connectionMap: Map<string, Connection> = new Map<
    string,
    Connection
  >();
  public static async getConnection(
    DBConnDetails: IMongoDatabaseConnection
  ): Promise<Connection> {
    let connectionName = DBConnDetails.dbName;

    if (!this.connectionMap.has(connectionName)) {
      let mongoConnection = new MongoConnection(
        DBConnDetails.dbConnectionDetails
      );

      let connection = await mongoConnection.getConnection(
        DBConnDetails.dbName
      );
      this.connectionMap.set(connectionName, connection);

      return Promise.resolve(connection);
    }

    let connection = this.connectionMap.get(connectionName);
    if (connection) return Promise.resolve(connection);
    else {
      throw Error("Mongo Connection for " + DBConnDetails + " is Undefined");
    }
  }

  public static async initializeAllConnections() {
    let databases = DatabaseList;
    let keyArr = _.keys(databases);

    await Promise.all(
      keyArr.map(async (k) => {
        let dbName = _.get(databases, k).dbName;
        console.log(`Connecting to ${dbName} ...`);
        await this.getConnection({ dbName: dbName });
      })
    );
  }
}
