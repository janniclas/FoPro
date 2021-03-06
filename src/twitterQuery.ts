import { Client } from "twitter-api-sdk";
import * as fs from "fs";

export interface Position {
  id: string;
  pagination_token: string | undefined;
}

export const getExpectedFollowerCount = async (
  client: Client,
  id: string | undefined
): Promise<number | undefined> => {
  if (id) {
    try {
      return (
        await client.users.findUserById(id, {
          "user.fields": ["public_metrics"],
        })
      ).data?.public_metrics?.followers_count;
    } catch (error) {
      await savePositionAndWait(id, error);
      return getExpectedFollowerCount(client, id);
    }
  } else {
    return -1;
  }
};

export const queryFollowers = async (
  client: Client,
  id: string,
  logPath: string,
  pagination_token: string | undefined
): Promise<any> => {
  try {
    const followerResponse = await client.users.usersIdFollowers(id, {
      max_results: 1000,
      pagination_token: pagination_token,
    });
    console.log(followerResponse);
    if (
      followerResponse.meta &&
      followerResponse.meta.result_count &&
      followerResponse.meta.result_count > 0
    ) {
      if (!followerResponse.errors && followerResponse.data) {
        return {
          followers: followerResponse.data,
          nextToken: followerResponse.meta?.next_token,
        };
      } else {
        await savePositionAndWait(
          id,
          followerResponse.errors,
          logPath,
          pagination_token
        );

        return await queryFollowers(client, id, logPath, pagination_token);
      }
    } else {
      return { followers: undefined, nextToken: undefined };
    }
  } catch (error) {
    await savePositionAndWait(id, error, logPath, pagination_token);
    return queryFollowers(client, id, logPath, pagination_token);
  }
};

const savePositionAndWait = async (
  id: string,
  error: any,
  logPath?: string,
  pagination_token?: string | undefined
) => {
  // prepare gracefull shutdown
  // save last processed id and page token
  const currentPosition: Position = {
    id: id,
    pagination_token: pagination_token,
  };
  if (logPath) {
    fs.writeFileSync(logPath, JSON.stringify(currentPosition));
  }
  console.error(error);
  const date = new Date();
  const time = date.getHours() + ":" + date.getMinutes();
  console.error(
    `${time} To many requests going to sleep and retry for 17 minutes`
  );

  await sleepFor17Min();
};

const sleepFor17Min = async () => {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve("");
    }, 930000);
  });
};
