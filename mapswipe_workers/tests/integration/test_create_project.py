import unittest

import set_up
import tear_down
from click.testing import CliRunner

from mapswipe_workers import auth, mapswipe_workers
from mapswipe_workers.utils.create_directories import create_directories


class TestCreateProject(unittest.TestCase):
    def setUp(self):
        self.project_id = set_up.create_test_project_draft(
            "tile_map_service_grid", "build_area"
        )
        create_directories()

    def tearDown(self):
        tear_down.delete_test_data(self.project_id)

    def test_create_project(self):
        runner = CliRunner()
        runner.invoke(mapswipe_workers.run_create_projects)

        pg_db = auth.postgresDB()
        query = "SELECT project_id FROM projects WHERE project_id = '{0}'".format(
            self.project_id
        )
        result = pg_db.retr_query(query)[0][0]
        self.assertEqual(result, self.project_id)

        fb_db = auth.firebaseDB()
        ref = fb_db.reference("/v2/projects/{0}".format(self.project_id))
        result = ref.get()
        self.assertIsNotNone(result)


if __name__ == "__main__":
    unittest.main()
