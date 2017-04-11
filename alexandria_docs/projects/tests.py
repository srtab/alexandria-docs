from __future__ import unicode_literals

from StringIO import StringIO
from mock import patch, Mock

from django.core.exceptions import ValidationError
from django.test import SimpleTestCase

from projects.validators import MimeTypeValidator
from projects.models import Organization, Project, ProjectArchive
from projects.utils import projects_upload_to, extract_to, extract_files


class OrganizationModelTest(SimpleTestCase):

    def test_str(self):
        organization = Organization(name="name")
        self.assertEqual(str(organization), organization.name)


class ProjectModelTest(SimpleTestCase):

    def test_str(self):
        project = Project(title="title")
        self.assertEqual(str(project), project.title)

    def test_get_absolute_url(self):
        project = Project(slug="slug")
        with self.settings(PROJECTS_SERVE_URL="/docs/"):
            self.assertEqual(project.get_absolute_url(), "/docs/slug/")


class ProjectArchiveModelTest(SimpleTestCase):

    def setUp(self):
        self.project = Project(title="title", slug="slug")
        self.archive = ProjectArchive(project=self.project)

    def test_str(self):
        self.assertEqual(str(self.archive), self.project.title)

    @patch("projects.models.extract_files")
    def test_post_save(self, extract_files):
        ProjectArchive.post_save(ProjectArchive, self.archive)
        extract_files.assert_called_with(
            self.project.slug, self.archive.archive)


class UtilsTest(SimpleTestCase):

    def test_projects_upload_to(self):
        project = Project(slug="title")
        archive = ProjectArchive(project=project)
        result = projects_upload_to(archive, "test.zip")
        self.assertRegexpMatches(result, r"^projects/\d+/\d+/title/test\.zip$")

    def test_extract_to(self):
        with self.settings(PROJECTS_SERVE_ROOT="/test/"):
            result = extract_to("unit")
        self.assertEqual(result, "/test/unit")

    @patch('projects.utils.tarfile')
    @patch('projects.utils.extract_to', return_value='/extractto')
    def test_extract_files(self, extract_to, tarfile):
        archive = Mock(path='/path/')
        extract_files('unit', archive)
        tarfile.open.assert_called_with('/path/', 'r:gz')
        tarfile.open().__enter__().extractall.assert_called_with('/extractto')


class MimeTypeValidatorTest(SimpleTestCase):
    """ """

    def setUp(self):
        self.archive = StringIO("test unit")

    @patch('projects.validators.magic')
    def test_empty_allowed_mimetype(self, magic):
        """ """
        validator = MimeTypeValidator()
        validator(self.archive)
        magic.from_buffer.assert_called_with("test unit", mime=True)

    @patch('projects.validators.magic')
    def test_with_valid_mymetype(self, magic):
        magic.from_buffer.return_value = "mimetype"
        validator = MimeTypeValidator(allowed_mimetypes=["mimetype"])
        returned = validator(self.archive)
        self.assertIsNone(returned)

    @patch('projects.validators.magic')
    def test_with_invalid_mymetype(self, magic):
        magic.from_buffer.return_value = "invalid_mimetype"
        validator = MimeTypeValidator(allowed_mimetypes=["mimetype"])
        expected_msg = (
            "MIME type 'invalid_mimetype' is not valid. "
            "Allowed types are: mimetype."
        )
        with self.assertRaisesRegex(ValidationError, expected_msg):
            validator(self.archive)

    @patch('projects.validators.magic')
    def test_with_invalid_mymetype_and_custom_message(self, magic):
        magic.from_buffer.return_value = "invalid_mimetype"
        validator = MimeTypeValidator(
            allowed_mimetypes=["mimetype"], message="Invalid mimetype")
        with self.assertRaisesRegex(ValidationError, "Invalid mimetype"):
            validator(self.archive)
