import "dotenv/config";
import { getPaths, readConfig } from "./configReader";

import { readUserIDs } from "./fileReader";
import { queryFollower } from "./query";
import { calculateStatistics, saveUniqueFollower } from "./statistic";
import { verifyFollower } from "./verify";

const main = async () => {
  const { bearerToken, filePath, mode } = readConfig();

  const { rawRecords, originalAuthorId } = await readUserIDs(filePath);
  const { outputPath, logPath } = getPaths(filePath, originalAuthorId);

  switch (mode) {
    case "query":
      console.log("Running in query mode");
      queryFollower(
        rawRecords,
        originalAuthorId,
        bearerToken,
        outputPath,
        logPath
      );
      break;
    case "verify":
      console.log("Running in verify mode");
      verifyFollower(outputPath, rawRecords.length, bearerToken);
      break;
    case "statistic":
      calculateStatistics(filePath).then((statistic) =>
        saveUniqueFollower(filePath, statistic)
      );
      break;
    default:
      console.log("Unkown mode. Possible modes: query, verify, statistic.");
  }
};

main();
