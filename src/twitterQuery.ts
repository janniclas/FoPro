import { Client } from "twitter-api-sdk";
import * as fs from "fs";

export interface Position {
  id: string;
  pagination_token: string | undefined;
}

export const queryFollowers = async (
  client: Client,
  id: string,
  logPath: string,
  pagination_token: string | undefined
) => {
  try {
    const followerResponse = await client.users.usersIdFollowers(id, {
      max_results: 1000,
      pagination_token: pagination_token,
    });
    if (!followerResponse.errors && followerResponse.data) {
      return followerResponse.data;
    } else {
      // prepare gracefull shutdown
      // save last processed id and page token
      const currentPosition: Position = {
        id: id,
        pagination_token: pagination_token,
      };
      fs.writeFileSync(logPath, JSON.stringify(currentPosition));
      followerResponse.errors!.forEach((err) => {
        console.error(err);
      });
      console.error(
        "Shutdown because of errors, saved current position into logfile"
      );
      throw followerResponse.errors;
    }
  } catch (error) {
    // prepare gracefull shutdown
    // save last processed id and page token
    const currentPosition: Position = {
      id: id,
      pagination_token: pagination_token,
    };
    fs.writeFileSync(logPath, JSON.stringify(currentPosition));

    console.error(
      "Shutdown because of errors, saved current position into logfile"
    );
    console.error(error);
    throw error;
  }
};
