import "dotenv/config";
import Client from "twitter-api-sdk";
import { getPaths, getStartParameters, readConfig } from "./configReader";

import { readUserIDs } from "./fileReader";
import { CsvFile, storeAllFollowers } from "./fileWriter";

export const main = async () => {
  const { filePath, bearerToken } = readConfig();
  const { rawRecords, originalAuthorId } = await readUserIDs(filePath);
  const { outputPath, logPath } = getPaths(originalAuthorId);

  const csvFile = new CsvFile({
    path: outputPath,
    headers: ["id", "username", "name", "parentId"],
  });

  const { appendMode, ids, pagination_token } = getStartParameters(
    rawRecords,
    outputPath,
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
    storeAllFollowers(csvFile, client, id, logPath, pagination_token);
  }

  console.log(`Finished processing file ${filePath}`);
};

main();
