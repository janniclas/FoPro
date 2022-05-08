import { FormatterOptionsArgs, Row, writeToStream } from "@fast-csv/format";
import * as fs from "fs";
import Client from "twitter-api-sdk";
import { queryFollowers } from "./twitterQuery";

type CsvFileOpts = {
  headers: string[];
  path: string;
};

export class CsvFile {
  static write(
    stream: NodeJS.WritableStream,
    rows: Row[],
    options: FormatterOptionsArgs<Row, Row>
  ): Promise<void> {
    return new Promise((res, rej) => {
      writeToStream(stream, rows, options)
        .on("error", (err: Error) => rej(err))
        .on("finish", () => res());
    });
  }

  private readonly headers: string[];

  private readonly path: string;

  private readonly writeOpts: FormatterOptionsArgs<Row, Row>;

  constructor(opts: CsvFileOpts) {
    this.headers = opts.headers;
    this.path = opts.path;
    this.writeOpts = { headers: this.headers, includeEndRowDelimiter: true };
  }

  create(rows: Row[]): Promise<void> {
    fs.writeFileSync(this.path, "");
    return CsvFile.write(fs.createWriteStream(this.path), rows, {
      ...this.writeOpts,
    });
  }

  append(rows: Row[]): Promise<void> {
    return CsvFile.write(
      fs.createWriteStream(this.path, { flags: "a" }),
      rows,
      {
        ...this.writeOpts,
        // dont write the headers when appending
        writeHeaders: false,
      } as FormatterOptionsArgs<Row, Row>
    );
  }

  read(): Promise<Buffer> {
    return new Promise((res, rej) => {
      fs.readFile(this.path, (err, contents) => {
        if (err) {
          return rej(err);
        }
        return res(contents);
      });
    });
  }
}

export const storeAllFollowers = async (
  csvFile: CsvFile,
  client: Client,
  id: string,
  logPath: string,
  pagination_token: string | undefined
) => {
  let hasNext = true;
  while (hasNext) {
    const { followers, nextToken } = await queryFollowers(
      client,
      id,
      logPath,
      pagination_token
    );
    console.log(
      `query result for user with id ${id} and token ${pagination_token}`
    );
    if (followers) {
      const essentialData = followers.map((follower: any) => {
        return {
          id: follower.id,
          username: follower.username,
          name: follower.name,
          parentId: id,
        };
      });
      console.log(`start writing results to file for user ${id}`);
      await csvFile.append(essentialData);
      console.log(`finished writing results to file for user ${id}`);
    }
    if (nextToken) {
      pagination_token = nextToken;
    } else {
      hasNext = false;
    }
  }
};
