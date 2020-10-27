import { IMongoConnectionDetails } from "./IMongoConnectionDetails";

export interface IMongoDatabaseConnection {
  dbName: string;
  dbConnectionDetails?: IMongoConnectionDetails;
}
