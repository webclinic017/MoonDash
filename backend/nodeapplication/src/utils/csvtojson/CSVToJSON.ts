import { readFileSync } from "fs-extra";
import csv from "csvtojson";
export async function CSVToJSON(fileLocation: string): Promise<any> {
  let fileData = await csv().fromFile(fileLocation);
  return Promise.resolve(fileData);
}
