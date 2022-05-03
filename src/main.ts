import "dotenv/config";
import * as fs from "fs";
import Client from "twitter-api-sdk";

import { getRawRecords } from "./fileReader";
import { CsvFile } from "./fileWriter";
import { Position, queryFollowers } from "./twitterQuery";

export const main = async () => {
  const bearerToken = process.env.BEARER_TOKEN;
  if (bearerToken) {
    const filePath = "/Users/struewer/git/FoPro/data/deuxcvsix.csv";
    const rawRecords = await getRawRecords(filePath);
    const originalAuthorId = rawRecords[0];
    const outputPath =
      "/Users/struewer/git/FoPro/data/followers/" + originalAuthorId + ".csv";
    const appendMode = fs.existsSync(outputPath);
    const logPath =
      "/Users/struewer/git/FoPro/data/followers/" + originalAuthorId + ".log";
    let pagination_token: string | undefined = undefined;
    const csvFile = new CsvFile({
      path: outputPath,
      headers: ["id", "username", "name", "parentId"],
    });

    if (!appendMode) {
      csvFile.create([]);
    } else {
      // get start parameter
      const logContent = fs.readFileSync(logPath, "utf8");
      const currentPosition: Position = JSON.parse(logContent);
      const startElement = rawRecords.indexOf(currentPosition.id);
      rawRecords.splice(startElement);
      pagination_token = currentPosition.pagination_token;
    }
    const client = new Client(bearerToken);
    rawRecords.forEach(async (value) => {
      const followers = await queryFollowers(
        client,
        value,
        logPath,
        pagination_token
      );
      const essentialData = followers.map((follower) => {
        return {
          id: follower.id,
          username: follower.username,
          name: follower.name,
          parentId: value,
        };
      });

      csvFile.append(essentialData);
    });
  } else {
    console.error("No bearer token found");
  }
};

main();
