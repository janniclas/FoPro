import "dotenv/config";
import { getPaths, readConfig } from "./configReader";

import { readUserIDs } from "./fileReader";
import {
  getNodeAndEdgePaths,
  prepareTransitivity,
  saveTransitivity,
} from "./networkTransitivity";
import { queryFollower } from "./query";
import { removeDuplicateRows } from "./remove";
import { calculateStatistics, saveUniqueFollower } from "./statistic";
import { getFollowerCount, verifyFollower } from "./verify";

const main = async () => {
  const { bearerToken, filePaths, mode } = readConfig();

  for (const filePath of filePaths) {
    console.log(`----starting query for file path ${filePath}-----`)
    const { rawRecords, originalAuthorId } = await readUserIDs(filePath);
    const noDuplicates = [...new Set(rawRecords)];
    const { outputPath, logPath } = getPaths(filePath, originalAuthorId);

    switch (mode) {
      case "query":
        console.log("Running in query mode");
        await queryFollower(
          noDuplicates,
          originalAuthorId,
          bearerToken,
          outputPath,
          logPath
        );
        break;
      case "verify":
        console.log("Running in verify mode");
        await verifyFollower(outputPath, noDuplicates.length, bearerToken);
        break;
      case "follower-count": 
          await getFollowerCount(noDuplicates, outputPath, bearerToken);
          break;
      case "statistic":
        calculateStatistics(filePath).then((statistic) =>
          saveUniqueFollower(filePath, statistic)
        );
        break;
      case "remove-duplicates":
        await removeDuplicateRows(outputPath);
        break;
      case "network-transitivity":
        prepareTransitivity(filePath).then((data) => {
          const { nodePath, edgePath } = getNodeAndEdgePaths(filePath);
          saveTransitivity(nodePath, edgePath, data);
        });
        break;
      default:
        console.log("Unkown mode. Possible modes: query, verify, statistic.");
    }
  }
};

main();
