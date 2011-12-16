# -*- coding: utf-8 -*-

import unittest2 as unittest

from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles

from plone.browserlayer.utils import registered_layers

from collective.newsflash.config import PROJECTNAME
from collective.newsflash.testing import INTEGRATION_TESTING

JS = '++resource++collective.newsflash.javascript/newsflash.js'


class InstallTest(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

    def test_installed(self):
        qi = getattr(self.portal, 'portal_quickinstaller')
        self.assertTrue(qi.isProductInstalled(PROJECTNAME))

    def test_browserlayer_installed(self):
        layers = [l.getName() for l in registered_layers()]
        self.assertTrue('INewsFlashLayer' in layers,
                        'browser layer not installed')

    def test_javascript_installed(self):
        js = getattr(self.portal, 'portal_javascripts')
        self.assertTrue(JS in js.getResourceIds(),
                        'javascript not installed')


class UninstallTest(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.qi = getattr(self.portal, 'portal_quickinstaller')
        self.qi.uninstallProducts(products=[PROJECTNAME])

    def test_uninstalled(self):
        self.assertTrue(not self.qi.isProductInstalled(PROJECTNAME))

    def test_browserlayer_uninstalled(self):
        layers = [l.getName() for l in registered_layers()]
        self.assertTrue('INewsFlashLayer' not in layers,
                        'browser layer not removed')

    def test_javascript_installed(self):
        js = getattr(self.portal, 'portal_javascripts')
        self.assertTrue(JS not in js.getResourceIds(),
                        'javascript not removed')


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
