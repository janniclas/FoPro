import "dotenv/config";
import * as fs from "fs";
import * as csv from "fast-csv";
import Client from "twitter-api-sdk";
import { getPaths, getStartParameters, readConfig } from "./configReader";

import { readUserIDs } from "./fileReader";
import { CsvFile, storeAllFollowers } from "./fileWriter";
import { getExpectedFollowerCount } from "./twitterQuery";

const main = async () => {
  const { bearerToken, filePath, mode } = readConfig();

  const { rawRecords, originalAuthorId } = await readUserIDs(filePath);
  const { outputPath, logPath } = getPaths(filePath, originalAuthorId);
  if (mode == "query") {
    console.log("Running in query mode");
    queryFollower(
      rawRecords,
      originalAuthorId,
      bearerToken,
      outputPath,
      logPath
    );
  }
  if (mode == "verify") {
    console.log("Running in verify mode");
    verifyFollower(outputPath, rawRecords.length, bearerToken);
  }
};

const queryFollower = async (
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

const verifyFollower = async (
  filePath: string,
  expectedNumberOfParentIds: number,
  bearerToken: string
) => {
  const parentToCounter = new Map<string, number>();
  fs.createReadStream(filePath)
    .pipe(csv.parse())
    .on("error", (error) => console.error(error))
    .on("data", (row) => {
      const parentId = row[3];
      if (!parentToCounter.has(parentId)) {
        parentToCounter.set(parentId, 1);
      } else {
        const current = parentToCounter.get(parentId)!;
        parentToCounter.set(parentId, current + 1);
      }
    })
    .on("end", async (_: number) => {
      const client = new Client(bearerToken);
      for (const key of parentToCounter.keys()) {
        const followerCount = await getExpectedFollowerCount(client, key);
        const querriedCount = parentToCounter.get(key);
        if (followerCount == querriedCount) {
          console.log("perfect match !");
        } else {
          console.log(
            "expected count " +
              followerCount +
              " stored count: " +
              querriedCount
          );
          if (followerCount && querriedCount) {
            const diff = followerCount - querriedCount;
            console.log("difference " + diff);
          }
        }
      }
      console.log(
        `Parent keys read from csv ${expectedNumberOfParentIds}. Parent keys in result ${parentToCounter.size}`
      );
    });
};

main();
