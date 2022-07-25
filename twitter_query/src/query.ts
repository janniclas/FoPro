import Client from "twitter-api-sdk";
import { getStartParameters } from "./configReader";

import { CsvFile, storeAllFollowers } from "./fileWriter";

export const queryFollower = async (
  rawRecords: string[],
  originalAuthorId: string,
  bearerToken: string,
  outputPath: string,
  logPath: string
) => {
  const csvFile = new CsvFile({
    path: outputPath,
    headers: ["id", "username", "name", "parentId"],
  });

  const { appendMode, ids, pagination_token } = getStartParameters(
    rawRecords,
    logPath
  );

  if (!appendMode) {
    console.log("A new file is created to store the data");
    csvFile.create([]);
  }
  console.log(ids);
  const client = new Client(bearerToken);
  for (const id of ids) {
    console.log(`start query for user with id ${id}`);
    await storeAllFollowers(csvFile, client, id, logPath, pagination_token);
  }

  console.log(`Finished processing file ${originalAuthorId}`);
};
