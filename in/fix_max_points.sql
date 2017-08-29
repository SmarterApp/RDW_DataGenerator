-- There was a code error that parsed the wrong tabulator column for item max points.
-- This script fixes just those items that need adjustment, then triggers migration of the changes.
--
-- This should be run *after* all assessment packages are loaded from tabulator files.
-- If the assessment packages are loaded with a fixed version of the package processor, this isn't necessary.

use warehouse;

INSERT INTO import (status, content, contentType, digest) VALUES
  (0, 2, 'text/plain', 'fix max points');
SELECT LAST_INSERT_ID() INTO @importid;

UPDATE asmt a JOIN item i ON i.asmt_id = a.id
  SET i.max_points = 10, a.update_import_id = @importid
  WHERE i.claim_id = 3 AND i.natural_id in ('200-61867', '200-54117', '200-57206', '200-54683', '200-56561', '200-61316', '200-62027', '200-62017', '200-57242');

UPDATE import SET status = 1 WHERE id = @importid;