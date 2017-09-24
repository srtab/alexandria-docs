from unittest.mock import MagicMock, patch, PropertyMock

from accounts.models import AccessLevel
from django.test import SimpleTestCase
from groups.models import Group
from projects.models import (
    ImportedArchive, ImportedFile, Project, ProjectCollaborator)


class ProjectModelTest(SimpleTestCase):

    def setUp(self):
        self.project = Project(title="title", slug="slug")

    def test_str(self):
        self.assertEqual(str(self.project), self.project.title)

    @patch.object(Group, 'is_private', new_callable=PropertyMock,
                  return_value=True)
    def test_is_private_with_group_private(self, mis_private):
        self.project.group = Group()
        self.project.visibility_level = Project.Level.PRIVATE
        self.assertTrue(self.project.is_private)
        self.project.visibility_level = Project.Level.PUBLIC
        self.assertTrue(self.project.is_private)

    @patch.object(Group, 'is_private', new_callable=PropertyMock,
                  return_value=False)
    def test_is_private_with_group_public(self, mis_private):
        self.project.group = Group()
        self.project.visibility_level = Project.Level.PRIVATE
        self.assertTrue(self.project.is_private)
        self.project.visibility_level = Project.Level.PUBLIC
        self.assertFalse(self.project.is_private)

    @patch.object(Group, 'is_public', new_callable=PropertyMock,
                  return_value=True)
    def test_is_public_with_group_public(self, mis_public):
        self.project.group = Group()
        self.project.visibility_level = Project.Level.PRIVATE
        self.assertTrue(self.project.is_public)
        self.project.visibility_level = Project.Level.PUBLIC
        self.assertTrue(self.project.is_public)

    @patch.object(Group, 'is_public', new_callable=PropertyMock,
                  return_value=False)
    def test_is_public_with_group_private(self, mis_public):
        self.project.group = Group()
        self.project.visibility_level = Project.Level.PRIVATE
        self.assertFalse(self.project.is_public)
        self.project.visibility_level = Project.Level.PUBLIC
        self.assertTrue(self.project.is_public)

    def test_get_absolute_url(self):
        with self.settings(PROJECTS_SERVE_URL="/docs/"):
            self.assertEqual(self.project.get_absolute_url(),
                             "/docs/slug/index.html")

    def test_serve_root_path(self):
        with self.settings(PROJECTS_SERVE_ROOT="/test/"):
            self.assertEqual(self.project.serve_root_path, "/test/slug")

    @patch.object(Project, 'imported_archives')
    def test_last_imported_archive_date(self, mimported_archives):
        mimported_archives.latest().created = 'created'
        result = self.project.last_imported_archive_date
        mimported_archives.latest.assert_called_with('created')
        self.assertEqual(result, 'created')

    @patch.object(Project, 'imported_archives')
    def test_last_imported_archive_date_empty(self, mimported_archives):
        mimported_archives.latest.side_effect = ImportedArchive.DoesNotExist
        result = self.project.last_imported_archive_date
        self.assertIsNone(result)

    @patch.object(Project, 'imported_files')
    def test_imported_files_count(self, mimported_files):
        self.project.imported_files_count
        mimported_files.count.assert_called_with()

    @patch('projects.models.token_generator.make_token', return_value="token")
    def test_api_token(self, mmake_token):
        self.assertEqual(self.project.api_token, 'token')
        mmake_token.assert_called_with(self.project)

    @patch.object(ProjectCollaborator, 'objects')
    def test_post_save_with_created_true(self, mobjects):
        Project.post_save(Project, Project(pk=1, author_id=1), True)
        mobjects.create.assert_called_with(
            project_id=1, user_id=1, access_level=AccessLevel.OWNER)

    @patch.object(ProjectCollaborator, 'objects')
    def test_post_save_with_created_false(self, mobjects):
        Project.post_save(Project, None, False)
        mobjects.create.assert_not_called()


class ImportedArchiveModelTest(SimpleTestCase):

    def setUp(self):
        self.project = Project(title="title", slug="slug")
        self.archive = ImportedArchive(project=self.project)
        self.archive.archive = MagicMock()

    def test_str(self):
        self.assertEqual(str(self.archive), self.project.title)

    @patch.object(ImportedFile.objects, 'walk')
    @patch('projects.models.tarfile')
    def test_fileify(self, tarfile, walk):
        self.archive.fileify()
        tarfile.open.assert_called_with(self.archive.archive.path, 'r:gz')
        tarfile.open().__enter__().extractall.assert_called_with(
            self.project.serve_root_path)
        walk.assert_called_with(self.project.pk, self.project.serve_root_path)

    def test_post_save(self):
        self.archive.fileify = MagicMock()
        ImportedArchive.post_save(ImportedArchive, self.archive, True)
        self.assertTrue(self.archive.fileify.called)

    def test_post_save_not_created(self):
        self.archive.fileify = MagicMock()
        ImportedArchive.post_save(ImportedArchive, self.archive, False)
        self.archive.fileify.assert_not_called()


class ImportedFileModelTest(SimpleTestCase):

    def setUp(self):
        self.imported_file = ImportedFile(path="/unit/test.html")

    def test_str(self):
        self.assertEqual(str(self.imported_file), "/unit/test.html")

    def test_get_absolute_url(self):
        with self.settings(
                PROJECTS_SERVE_ROOT="/unit/", PROJECTS_SERVE_URL="/docs/"):
            self.assertEqual(self.imported_file.get_absolute_url(),
                             "/docs/test.html")
