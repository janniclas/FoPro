import * as fs from "fs";
import * as csv from "fast-csv";
import Client from "twitter-api-sdk";

import { getExpectedFollowerCount } from "./twitterQuery";
import path = require("path");
import { CsvFile } from "./fileWriter";

export const getFollowerCount = async (followers: string[], outputPath: string, bearerToken: string) => {
  const client = new Client(bearerToken);
  const p = path.parse(outputPath);
  const noDuplicatesPath = p.dir + "/" + p.name + "-noduplicates.csv";
  const csvFile = new CsvFile({
    path: noDuplicatesPath,
    headers: ["id", "count"],
  });
  csvFile.create([]);
  let sum = 0;
  for (const follower of followers) {
     const followerCount = await getExpectedFollowerCount(client, follower);
     sum += followerCount ?? 0;
      const nextRow: string[] = [follower + ", " +followerCount!];
      csvFile.append([nextRow]);
  }
  csvFile.append([["Sum, " + sum]]);
}

export const verifyFollower = async (
  filePath: string,
  expectedNumberOfParentIds: number,
  bearerToken: string
) => {
  const parentToCounter = new Map<string, number>();
  const rowSet = new Set<string>();
  let duplicateRowCounter = 0;
  fs.createReadStream(filePath)
    .pipe(csv.parse())
    .on("error", (error) => console.error(error))
    .on("data", (row: string[]) => {
      const rowString = row.reduce((previousValue, currentValue) => {
        return previousValue + currentValue;
      }, "");
      if (!rowSet.has(rowString)) {
        rowSet.add(rowString);
        const parentId = row[3];
        if (!parentToCounter.has(parentId)) {
          parentToCounter.set(parentId, 1);
        } else {
          const current = parentToCounter.get(parentId)!;
          parentToCounter.set(parentId, current + 1);
        }
      } else {
        duplicateRowCounter += 1;
      }
    })
    .on("end", async (_: number) => {
      console.log("duplicate rows " + duplicateRowCounter);
      const client = new Client(bearerToken);
      for (const key of parentToCounter.keys()) {
        const followerCount = await getExpectedFollowerCount(client, key);
        const querriedCount = parentToCounter.get(key);
        if (followerCount == querriedCount) {
          console.log("perfect match !");
        } else {
          console.log(
            `expected count for id ${key} ${followerCount} stored count: ${querriedCount}`
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
