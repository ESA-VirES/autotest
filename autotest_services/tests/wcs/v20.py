#-------------------------------------------------------------------------------
#
# Project: EOxServer <http://eoxserver.org>
# Authors: Fabian Schindler <fabian.schindler@eox.at>
#
#-------------------------------------------------------------------------------
# Copyright (C) 2013 EOX IT Services GmbH
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies of this Software or works derived from this Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#-------------------------------------------------------------------------------

from urllib import quote

from autotest_services import testbase
import base as wcsbase


#===============================================================================
# WCS 2.0 Get Capabilities
#===============================================================================

class WCS20GetCapabilitiesValidTestCase(testbase.XMLTestCase, testbase.SchematronTestMixIn):
    """This test shall retrieve a valid WCS 2.0 EO-AP (EO-WCS) GetCapabilities response"""
    
    schematron_locations = ["http://schemas.opengis.net/wcs/crs/", 
                            "http://schemas.opengis.net/wcs/crs/1.0/wcsCrs.sch"]
    
    def getRequest(self):
        params = "service=WCS&version=2.0.1&request=GetCapabilities"
        return (params, "kvp")

class WCS20GetCapabilitiesEmptyTestCase(testbase.XMLTestCase):
    """This test shall retrieve a valid but empty WCS 2.0 EO-AP (EO-WCS) GetCapabilities response (see #41)"""
    fixtures = testbase.BASE_FIXTURES
    
    def getRequest(self):
        params = "service=WCS&version=2.0.1&request=GetCapabilities"
        return (params, "kvp")

class WCSVersionNegotiationOldStyleTestCase(testbase.XMLTestCase):
    """This test shall check old style version negotiation. A valid WCS 2.0 EO-AP (EO-WCS) GetCapabilities response shall be returned"""
    def getRequest(self):
        params = "service=wcs&version=3.0.0&request=GetCapabilities"
        return (params, "kvp")

class WCSVersionNegotiationNewStyleTestCase(testbase.XMLTestCase):
    """This test shall check new style version negotiation. A valid WCS 2.0 EO-AP (EO-WCS) GetCapabilities response shall be returned"""
    def getRequest(self):
        params = "service=wcs&acceptversions=2.0.1,1.1.0&request=GetCapabilities"
        return (params, "kvp")

class WCSVersionNegotiationFaultTestCase(testbase.ExceptionTestCase):
    """This test shall check new style version negotiation. A valid ows:ExceptionReport shall be returned"""
    def getRequest(self):
        params = "service=wcs&acceptversions=3.0.0&request=GetCapabilities"
        return (params, "kvp")

    def getExpectedExceptionCode(self):
        return "VersionNegotiationFailed"

#===============================================================================
# WCS 2.0 DescribeCoverage
#===============================================================================
    
class WCS20DescribeCoverageDatasetTestCase(testbase.XMLTestCase):
    """This test shall retrieve a valid WCS 2.0 EO-AP (EO-WCS) DescribeCoverage response for a wcseo:RectifiedDataset."""
    def getRequest(self):
        params = "service=WCS&version=2.0.0&request=DescribeCoverage&CoverageId=MER_FRS_1PNPDE20060822_092058_000001972050_00308_23408_0077_uint16_reduced_compressed"
        return (params, "kvp")

class WCS20DescribeCoverageMosaicTestCase(testbase.XMLTestCase):
    """This test shall retrieve a valid WCS 2.0 EO-AP (EO-WCS) DescribeCoverage response for a wcseo:RectifiedStitchedMosaic."""
    def getRequest(self):
        params = "service=WCS&version=2.0.0&request=DescribeCoverage&CoverageId=mosaic_MER_FRS_1P_RGB_reduced"
        return (params, "kvp")

class WCS20DescribeCoverageDatasetSeriesFaultTestCase(testbase.ExceptionTestCase):
    """This test shall try to retrieve a CoverageDescription for a non-coverage. It shall yield a valid ows:ExceptionReport"""
    def getRequest(self):
        params = "service=WCS&version=2.0.0&request=DescribeCoverage&CoverageId=MER_FRS_1P_reduced"
        return (params, "kvp")
    
    def getExpectedHTTPStatus(self):
        return 404
    
    def getExpectedExceptionCode(self):
        return "NoSuchCoverage"
        
class WCS20DescribeCoverageFaultTestCase(testbase.ExceptionTestCase):
    """This test shall try to retrieve a CoverageDescription for a coverage that does not exist. It shall yield a valid ows:ExceptionReport"""
    def getRequest(self):
        params = "service=WCS&version=2.0.0&request=DescribeCoverage&CoverageId=some_coverage"
        return (params, "kvp")
    
    def getExpectedHTTPStatus(self):
        return 404
    
    def getExpectedExceptionCode(self):
        return "NoSuchCoverage"

class WCS20DescribeCoverageMissingParameterFaultTestCase(testbase.ExceptionTestCase):
    """This test shall yield a valid ows:ExceptionReport for a missing parameter"""
    def getRequest(self):
        params = "service=WCS&version=2.0.0&request=DescribeCoverage"
        return (params, "kvp")
    
    def getExpectedExceptionCode(self):
        return "MissingParameterValue"

#===============================================================================
# WCS 2.0 DescribeEOCoverageSet 
#===============================================================================

class WCS20DescribeEOCoverageSetDatasetTestCase(testbase.XMLTestCase):
    """This test shall retrieve a valid WCS 2.0 EO-AP (EO-WCS) DescribeEOCoverageSet response for a wcseo:RectifiedDataset"""
    def getRequest(self):
        params = "service=WCS&version=2.0.0&request=DescribeEOCoverageSet&eoId=MER_FRS_1PNPDE20060822_092058_000001972050_00308_23408_0077_uint16_reduced_compressed"
        return (params, "kvp")

class WCS20DescribeEOCoverageSetMosaicTestCase(testbase.XMLTestCase):
    """This test shall retrieve a valid WCS 2.0 EO-AP (EO-WCS) DescribeEOCoverageSet response for a wcseo:RectifiedStitchedMosaic"""
    def getRequest(self):
        params = "service=WCS&version=2.0.0&request=DescribeEOCoverageSet&eoId=mosaic_MER_FRS_1P_RGB_reduced"
        return (params, "kvp")

class WCS20DescribeEOCoverageSetDatasetSeriesTestCase(testbase.XMLTestCase):
    """This test shall retrieve a valid WCS 2.0 EO-AP (EO-WCS) DescribeEOCoverageSet response for a wcseo:RectifiedDatasetSeries."""
    def getRequest(self):
        params = "service=WCS&version=2.0.0&request=DescribeEOCoverageSet&eoId=MER_FRS_1P_reduced"
        return (params, "kvp")

class WCS20DescribeEOCoverageSetFaultTestCase(testbase.ExceptionTestCase):
    """This test shall try to retrieve a CoverageDescription set for an wcseo-Object that does not exist. It shall yield a valid ows:ExceptionReport."""
    def getRequest(self):
        params = "service=WCS&version=2.0.0&request=DescribeEOCoverageSet&eoId=some_eo_object"
        return (params, "kvp")
    
    def getExpectedHTTPStatus(self):
        return 404
    
    def getExpectedExceptionCode(self):
        return "NoSuchCoverage"

class WCS20DescribeEOCoverageSetMissingParameterFaultTestCase(testbase.ExceptionTestCase):
    def getRequest(self):
        params = "service=WCS&version=2.0.0&request=DescribeEOCoverageSet"
        return (params, "kvp")
    
    def getExpectedExceptionCode(self):
        return "MissingParameterValue"

class WCS20DescribeEOCoverageSetTwoSpatialSubsetsTestCase(testbase.WCS20DescribeEOCoverageSetSubsettingTestCase):
    def getRequest(self):
        params = "service=wcs&version=2.0.0&request=DescribeEOCoverageSet&EOID=MER_FRS_1P_reduced&subset=lat,http://www.opengis.net/def/crs/EPSG/0/4326(32,47)&subset=long,http://www.opengis.net/def/crs/EPSG/0/4326(11,33)"
        return (params, "kvp")

    def getExpectedCoverageIds(self):
        return [
            "MER_FRS_1PNPDE20060816_090929_000001972050_00222_23322_0058_uint16_reduced_compressed",
            "MER_FRS_1PNPDE20060822_092058_000001972050_00308_23408_0077_uint16_reduced_compressed",
            "MER_FRS_1PNPDE20060830_100949_000001972050_00423_23523_0079_uint16_reduced_compressed",
            "mosaic_MER_FRS_1PNPDE20060816_090929_000001972050_00222_23322_0058_RGB_reduced",
            "mosaic_MER_FRS_1P_RGB_reduced"
        ]

class WCS20DescribeEOCoverageSetTwoSpatialSubsetsOverlapsTestCase(testbase.WCS20DescribeEOCoverageSetSubsettingTestCase):
    def getRequest(self):
        params = "service=wcs&version=2.0.0&request=DescribeEOCoverageSet&EOID=MER_FRS_1P_reduced&subset=lat,http://www.opengis.net/def/crs/EPSG/0/4326(32,47)&subset=long,http://www.opengis.net/def/crs/EPSG/0/4326(11,33)&containment=overlaps"
        return (params, "kvp")

    def getExpectedCoverageIds(self):
        return [
            "MER_FRS_1PNPDE20060816_090929_000001972050_00222_23322_0058_uint16_reduced_compressed",
            "MER_FRS_1PNPDE20060822_092058_000001972050_00308_23408_0077_uint16_reduced_compressed",
            "MER_FRS_1PNPDE20060830_100949_000001972050_00423_23523_0079_uint16_reduced_compressed",
            "mosaic_MER_FRS_1PNPDE20060816_090929_000001972050_00222_23322_0058_RGB_reduced",
            "mosaic_MER_FRS_1P_RGB_reduced"
        ]

class WCS20DescribeEOCoverageSetTwoSpatialSubsetsContainsTestCase(testbase.WCS20DescribeEOCoverageSetSubsettingTestCase):
    def getRequest(self):
        params = "service=wcs&version=2.0.0&request=DescribeEOCoverageSet&EOID=MER_FRS_1P_reduced&subset=lat,http://www.opengis.net/def/crs/EPSG/0/4326(32,47)&subset=long,http://www.opengis.net/def/crs/EPSG/0/4326(11,33)&containment=contains"
        return (params, "kvp")
    
    def getExpectedCoverageIds(self):
        return [
            "MER_FRS_1PNPDE20060816_090929_000001972050_00222_23322_0058_uint16_reduced_compressed",
            "mosaic_MER_FRS_1PNPDE20060816_090929_000001972050_00222_23322_0058_RGB_reduced"
        ]

class WCS20DescribeEOCoverageSetTemporalSubsetTestCase(testbase.WCS20DescribeEOCoverageSetSubsettingTestCase):
    def getRequest(self):
        params = "service=wcs&version=2.0.0&request=DescribeEOCoverageSet&EOID=MER_FRS_1P_reduced&subset=phenomenonTime(\"2006-08-01\",\"2006-08-22T09:22:00Z\")"
        return (params, "kvp")
    
    def getExpectedCoverageIds(self):
        return [
            "MER_FRS_1PNPDE20060816_090929_000001972050_00222_23322_0058_uint16_reduced_compressed",
            "MER_FRS_1PNPDE20060822_092058_000001972050_00308_23408_0077_uint16_reduced_compressed",
            "mosaic_MER_FRS_1PNPDE20060816_090929_000001972050_00222_23322_0058_RGB_reduced",
            "mosaic_MER_FRS_1P_RGB_reduced"
        ]

class WCS20DescribeEOCoverageSetTemporalSubsetOverlapsTestCase(testbase.WCS20DescribeEOCoverageSetSubsettingTestCase):
    def getRequest(self):
        params = "service=wcs&version=2.0.0&request=DescribeEOCoverageSet&EOID=MER_FRS_1P_reduced&subset=phenomenonTime(\"2006-08-01\",\"2006-08-22T09:22:00Z\")&containment=overlaps"
        return (params, "kvp")
    
    def getExpectedCoverageIds(self):
        return [
            "MER_FRS_1PNPDE20060816_090929_000001972050_00222_23322_0058_uint16_reduced_compressed",
            "MER_FRS_1PNPDE20060822_092058_000001972050_00308_23408_0077_uint16_reduced_compressed",
            "mosaic_MER_FRS_1PNPDE20060816_090929_000001972050_00222_23322_0058_RGB_reduced",
            "mosaic_MER_FRS_1P_RGB_reduced"
        ]

class WCS20DescribeEOCoverageSetTemporalSubsetContainsTestCase(testbase.WCS20DescribeEOCoverageSetSubsettingTestCase):
    def getRequest(self):
        params = "service=wcs&version=2.0.0&request=DescribeEOCoverageSet&EOID=MER_FRS_1P_reduced&subset=phenomenonTime(\"2006-08-01\",\"2006-08-22T09:22:00Z\")&containment=contains"
        return (params, "kvp")
    
    def getExpectedCoverageIds(self):
        return [
            "MER_FRS_1PNPDE20060816_090929_000001972050_00222_23322_0058_uint16_reduced_compressed",
            "mosaic_MER_FRS_1PNPDE20060816_090929_000001972050_00222_23322_0058_RGB_reduced"
        ]

class WCS20DescribeEOCoverageSetSpatioTemporalSubsetTestCase(testbase.WCS20DescribeEOCoverageSetSubsettingTestCase):
    def getRequest(self):
        params = "service=wcs&version=2.0.0&request=DescribeEOCoverageSet&EOID=MER_FRS_1P_reduced&subset=phenomenonTime(\"2006-08-01\",\"2006-08-22T09:22:00Z\")&subset=lat,http://www.opengis.net/def/crs/EPSG/0/4326(32,47)&subset=long,http://www.opengis.net/def/crs/EPSG/0/4326(11,33)"
        return (params, "kvp")
        
    def getExpectedCoverageIds(self):
        return [
            "MER_FRS_1PNPDE20060816_090929_000001972050_00222_23322_0058_uint16_reduced_compressed",
            "MER_FRS_1PNPDE20060822_092058_000001972050_00308_23408_0077_uint16_reduced_compressed",
            "mosaic_MER_FRS_1PNPDE20060816_090929_000001972050_00222_23322_0058_RGB_reduced",
            "mosaic_MER_FRS_1P_RGB_reduced"
        ]

class WCS20DescribeEOCoverageSetSpatioTemporalSubsetOverlapsTestCase(testbase.WCS20DescribeEOCoverageSetSubsettingTestCase):
    def getRequest(self):
        params = "service=wcs&version=2.0.0&request=DescribeEOCoverageSet&EOID=MER_FRS_1P_reduced&subset=phenomenonTime(\"2006-08-01\",\"2006-08-22T09:22:00Z\")&subset=lat,http://www.opengis.net/def/crs/EPSG/0/4326(32,47)&subset=long,http://www.opengis.net/def/crs/EPSG/0/4326(11,33)&containment=overlaps"
        return (params, "kvp")
        
    def getExpectedCoverageIds(self):
        return [
            "MER_FRS_1PNPDE20060816_090929_000001972050_00222_23322_0058_uint16_reduced_compressed",
            "MER_FRS_1PNPDE20060822_092058_000001972050_00308_23408_0077_uint16_reduced_compressed",
            "mosaic_MER_FRS_1PNPDE20060816_090929_000001972050_00222_23322_0058_RGB_reduced",
            "mosaic_MER_FRS_1P_RGB_reduced"
        ]

class WCS20DescribeEOCoverageSetSpatioTemporalSubsetContainsTestCase(testbase.WCS20DescribeEOCoverageSetSubsettingTestCase):
    def getRequest(self):
        params = "service=wcs&version=2.0.0&request=DescribeEOCoverageSet&EOID=MER_FRS_1P_reduced&subset=phenomenonTime(\"2006-08-01\",\"2006-08-22T09:22:00Z\")&subset=lat,http://www.opengis.net/def/crs/EPSG/0/4326(32,47)&subset=long,http://www.opengis.net/def/crs/EPSG/0/4326(11,33)&containment=contains"
        return (params, "kvp")
        
    def getExpectedCoverageIds(self):
        return [
            "MER_FRS_1PNPDE20060816_090929_000001972050_00222_23322_0058_uint16_reduced_compressed",
            "mosaic_MER_FRS_1PNPDE20060816_090929_000001972050_00222_23322_0058_RGB_reduced"
        ]

class WCS20DescribeEOCoverageSetIncorrectTemporalSubsetFaultTestCase(testbase.ExceptionTestCase):
    def getRequest(self):
        params = "service=wcs&version=2.0.0&request=DescribeEOCoverageSet&EOID=MER_FRS_1P_reduced&subset=phenomenonTime(2006-08-01,2006-08-22)"
        return (params, "kvp")
    
    def getExpectedHTTPStatus(self):
        return 404
    
    def getExpectedExceptionCode(self):
        return "InvalidSubsetting"
    
class WCS20DescribeEOCoverageSetInvalidTemporalSubsetFaultTestCase(testbase.ExceptionTestCase):
    def getRequest(self):
        params = "service=wcs&version=2.0.0&request=DescribeEOCoverageSet&EOID=MER_FRS_1P_reduced&subset=phenomenonTime(\"2006-08-01\",\"2006-31-31\")"
        return (params, "kvp")
    
    def getExpectedHTTPStatus(self):
        return 404
    
    def getExpectedExceptionCode(self):
        return "InvalidSubsetting"

class WCS20DescribeEOCoverageSetIncorrectSpatialSubsetFaultTestCase(testbase.ExceptionTestCase):
    def getRequest(self):
        params = "service=wcs&version=2.0.0&request=DescribeEOCoverageSet&EOID=MER_FRS_1P_reduced&subset=lat,http://www.opengis.net/def/crs/EPSG/0/4326(some_lat,some_other_lat)"
        return (params, "kvp")
    
    def getExpectedHTTPStatus(self):
        return 404
    
    def getExpectedExceptionCode(self):
        return "InvalidSubsetting"

class WCS20DescribeEOCoverageSetInvalidSpatialSubsetFaultTestCase(testbase.ExceptionTestCase):
    def getRequest(self):
        params = "service=wcs&version=2.0.0&request=DescribeEOCoverageSet&EOID=MER_FRS_1P_reduced&subset=lat,http://www.opengis.net/def/crs/EPSG/0/4326(47,32)"
        return (params, "kvp")
    
    def getExpectedHTTPStatus(self):
        return 404
    
    def getExpectedExceptionCode(self):
        return "InvalidSubsetting"

# EOxServer allows and understands certain additional axis labels like "lat", or "long".
class WCS20DescribeEOCoverageSetInvalidAxisLabelFaultTestCase(testbase.ExceptionTestCase):
    def getRequest(self):
        params = "service=wcs&version=2.0.0&request=DescribeEOCoverageSet&EOID=MER_FRS_1P_reduced&subset=x_axis,http://www.opengis.net/def/crs/EPSG/0/4326(32,47)"
        return (params, "kvp")
    
    def getExpectedHTTPStatus(self):
        return 404
    
    def getExpectedExceptionCode(self):
        return "InvalidAxisLabel"

#===============================================================================
# WCS 2.0: Paging testcases
#===============================================================================

class WCS20DescribeEOCoverageSetDatasetPagingCountTestCase(testbase.WCS20DescribeEOCoverageSetPagingTestCase):
    def getExpectedCoverageCount(self):
        return 2
    
    def getRequest(self):
        params = "service=WCS&version=2.0.0&request=DescribeEOCoverageSet&eoId=MER_FRS_1P_reduced&count=2"
        return (params, "kvp")

#===============================================================================
# WCS 2.0: Section test cases
#===============================================================================

class WCS20DescribeEOCoverageSetSectionsAllTestCase(testbase.WCS20DescribeEOCoverageSetSectionsTestCase):
    def getExpectedSections(self):
        return [
            "{http://www.opengis.net/wcs/2.0}CoverageDescriptions",
            "{http://www.opengis.net/wcseo/1.0}DatasetSeriesDescriptions"
        ]
        
    def getRequest(self):
        params = "service=WCS&version=2.0.0&request=DescribeEOCoverageSet&eoId=MER_FRS_1P_reduced&sections=All"
        return (params, "kvp")

class WCS20DescribeEOCoverageSetSectionsAll2TestCase(testbase.WCS20DescribeEOCoverageSetSectionsTestCase):
    def getExpectedSections(self):
        return [
            "{http://www.opengis.net/wcs/2.0}CoverageDescriptions",
            "{http://www.opengis.net/wcseo/1.0}DatasetSeriesDescriptions"
        ]
        
    def getRequest(self):
        params = "service=WCS&version=2.0.0&request=DescribeEOCoverageSet&eoId=MER_FRS_1P_reduced&sections=CoverageDescriptions,DatasetSeriesDescriptions"
        return (params, "kvp")
    
class WCS20DescribeEOCoverageSetSectionsAll3TestCase(testbase.WCS20DescribeEOCoverageSetSectionsTestCase):
    def getExpectedSections(self):
        return [
            "{http://www.opengis.net/wcs/2.0}CoverageDescriptions",
            "{http://www.opengis.net/wcseo/1.0}DatasetSeriesDescriptions"
        ]
        
    def getRequest(self):
        params = "service=WCS&version=2.0.0&request=DescribeEOCoverageSet&eoId=MER_FRS_1P_reduced&sections=All,DatasetSeriesDescriptions"
        return (params, "kvp")

class WCS20DescribeEOCoverageSetSectionsAll4TestCase(testbase.WCS20DescribeEOCoverageSetSectionsTestCase):
    def getExpectedSections(self):
        return [
            "{http://www.opengis.net/wcs/2.0}CoverageDescriptions",
            "{http://www.opengis.net/wcseo/1.0}DatasetSeriesDescriptions"
        ]
        
    def getRequest(self):
        params = "service=WCS&version=2.0.0&request=DescribeEOCoverageSet&eoId=MER_FRS_1P_reduced&sections=CoverageDescriptions,All"
        return (params, "kvp")

class WCS20DescribeEOCoverageSetSectionsCoverageDescriptionsTestCase(testbase.WCS20DescribeEOCoverageSetSectionsTestCase):
    def getExpectedSections(self):
        return [
            "{http://www.opengis.net/wcs/2.0}CoverageDescriptions"
        ]
        
    def getRequest(self):
        params = "service=WCS&version=2.0.0&request=DescribeEOCoverageSet&eoId=MER_FRS_1P_reduced&sections=CoverageDescriptions"
        return (params, "kvp")

class WCS20DescribeEOCoverageSetSectionsDatasetSeriesDescriptionsTestCase(testbase.WCS20DescribeEOCoverageSetSectionsTestCase):
    def getExpectedSections(self):
        return [
            "{http://www.opengis.net/wcseo/1.0}DatasetSeriesDescriptions"
        ]
        
    def getRequest(self):
        params = "service=WCS&version=2.0.0&request=DescribeEOCoverageSet&eoId=MER_FRS_1P_reduced&sections=DatasetSeriesDescriptions"
        return (params, "kvp")

class WCS20DescribeEOCoverageSetSectionsFaultTestCase(testbase.ExceptionTestCase):
    def getRequest(self):
        params = "service=wcs&version=2.0.0&request=DescribeEOCoverageSet&EOID=MER_FRS_1P_reduced&sections=WrongSection"
        return (params, "kvp")
    
    def getExpectedHTTPStatus(self):
        return 400
    
    def getExpectedExceptionCode(self):
        return "InvalidParameterValue"


class WCS20DescribeEOCoverageSetDatasetUniqueTestCase(testbase.WCS20DescribeEOCoverageSetSubsettingTestCase): 
    def getRequest(self):
        params = "service=wcs&version=2.0.0&request=DescribeEOCoverageSet&EOID=MER_FRS_1PNPDE20060816_090929_000001972050_00222_23322_0058_uint16_reduced_compressed,MER_FRS_1PNPDE20060816_090929_000001972050_00222_23322_0058_uint16_reduced_compressed"
        return (params, "kvp")
    
    def getExpectedCoverageIds(self):
        return [
            "MER_FRS_1PNPDE20060816_090929_000001972050_00222_23322_0058_uint16_reduced_compressed"
        ]

class WCS20DescribeEOCoverageSetDatasetOutOfSubsetTestCase(testbase.WCS20DescribeEOCoverageSetSubsettingTestCase):
    def getRequest(self):
        params = "service=wcs&version=2.0.0&request=DescribeEOCoverageSet&EOID=MER_FRS_1PNPDE20060816_090929_000001972050_00222_23322_0058_uint16_reduced_compressed&ubset=lat,http://www.opengis.net/def/crs/EPSG/0/4326(0,1)&subset=long,http://www.opengis.net/def/crs/EPSG/0/4326(0,1)"
        return (params, "kvp")
    
    def getExpectedCoverageIds(self):
        return []
    
class WCS20DescribeEOCoverageSetDatasetSeriesStitchedMosaicTestCase(testbase.WCS20DescribeEOCoverageSetSubsettingTestCase):
    def getRequest(self):
        params = "service=wcs&version=2.0.0&request=DescribeEOCoverageSet&EOID=MER_FRS_1P_reduced,mosaic_MER_FRS_1P_RGB_reduced"
        return (params, "kvp")
    
    def getExpectedCoverageIds(self):
        return [
            "MER_FRS_1PNPDE20060816_090929_000001972050_00222_23322_0058_uint16_reduced_compressed",
            "MER_FRS_1PNPDE20060822_092058_000001972050_00308_23408_0077_uint16_reduced_compressed",
            "MER_FRS_1PNPDE20060830_100949_000001972050_00423_23523_0079_uint16_reduced_compressed",
            "mosaic_MER_FRS_1PNPDE20060816_090929_000001972050_00222_23322_0058_RGB_reduced",
            "mosaic_MER_FRS_1PNPDE20060822_092058_000001972050_00308_23408_0077_RGB_reduced",
            "mosaic_MER_FRS_1PNPDE20060830_100949_000001972050_00423_23523_0079_RGB_reduced",
            "mosaic_MER_FRS_1P_RGB_reduced"
        ]

#===============================================================================
# WCS 2.0: Exceptions
#===============================================================================

# after WCS 2.0.1 implementation does not lead to an error anymore 
#class WCS20GetCoverageFormatMissingFaultTestCase(testbase.ExceptionTestCase):
#    def getRequest(self):
#        params = "service=wcs&version=2.0.0&request=GetCoverage&CoverageId=mosaic_MER_FRS_1P_RGB_reduced"
#        return (params, "kvp")
#    
#    def getExpectedExceptionCode(self):
#        return "MissingParameterValue"

class WCS20GetCoverageNoSuchCoverageFaultTestCase(testbase.ExceptionTestCase):
    def getRequest(self):
        params = "service=wcs&version=2.0.0&request=GetCoverage&CoverageId=INVALID"
        return (params, "kvp")

    def getExpectedHTTPStatus(self):
        return 404
    
    def getExpectedExceptionCode(self):
        return "NoSuchCoverage"

class WCS20GetCoverageFormatUnsupportedFaultTestCase(testbase.ExceptionTestCase):
    def getRequest(self):
        params = "service=wcs&version=2.0.0&request=GetCoverage&CoverageId=MER_FRS_1PNPDE20060822_092058_000001972050_00308_23408_0077_uint16_reduced_compressed&format=image/jpeg"
        return (params, "kvp")
    
    def getExpectedExceptionCode(self):
        return "InvalidParameterValue"

class WCS20GetCoverageFormatUnknownFaultTestCase(testbase.ExceptionTestCase):
    def getRequest(self):
        params = "service=wcs&version=2.0.0&request=GetCoverage&CoverageId=MER_FRS_1PNPDE20060822_092058_000001972050_00308_23408_0077_uint16_reduced_compressed&format=unknown"
        return (params, "kvp")
    
    def getExpectedExceptionCode(self):
        return "InvalidParameterValue"

#===============================================================================
# WCS 2.0: Simple requests
#===============================================================================

class WCS20GetCoverageMosaicTestCase(testbase.RectifiedGridCoverageTestCase):
    def getRequest(self):
        params = "service=wcs&version=2.0.0&request=GetCoverage&CoverageId=mosaic_MER_FRS_1P_RGB_reduced&format=image/tiff"
        return (params, "kvp")

class WCS20GetCoverageDatasetTestCase(testbase.RectifiedGridCoverageTestCase):
    def getRequest(self):
        params = "service=wcs&version=2.0.0&request=GetCoverage&CoverageId=MER_FRS_1PNPDE20060822_092058_000001972050_00308_23408_0077_uint16_reduced_compressed&format=image/tiff"
        return (params, "kvp")

#==============================================================================
# WCS 2.0: Formats
#==============================================================================

# WCS 2.0.1 introduced the native format, i.e., default format in case of missing format specification
class WCS20GetCoverageNativeTestCase(testbase.RectifiedGridCoverageTestCase):
    def getRequest(self):
        params = "service=wcs&version=2.0.1&request=GetCoverage&CoverageId=mosaic_MER_FRS_1P_RGB_reduced"
        return (params, "kvp")

    def getFileExtension(self, part=None):
        return "tif"

class WCS20GetCoverageJPEG2000TestCase(testbase.RectifiedGridCoverageTestCase):
    def getRequest(self):
        params = "service=wcs&version=2.0.0&request=GetCoverage&CoverageId=mosaic_MER_FRS_1P_RGB_reduced&format=image/jp2"
        return (params, "kvp")
    
    def getFileExtension(self, part=None):
        return "jp2"

class WCS20GetCoverageNetCDFTestCase(testbase.RectifiedGridCoverageTestCase):
    def getRequest(self):
        params = "service=wcs&version=2.0.0&request=GetCoverage&CoverageId=mosaic_MER_FRS_1P_RGB_reduced&format=application/x-netcdf"
        return (params, "kvp")
    
    def getFileExtension(self, part=None):
        return "nc"

class WCS20GetCoverageHDFTestCase(testbase.RectifiedGridCoverageTestCase):
    def getRequest(self):
        params = "service=wcs&version=2.0.0&request=GetCoverage&CoverageId=mosaic_MER_FRS_1P_RGB_reduced&format=application/x-hdf"
        return (params, "kvp")
    
    def getFileExtension(self, part=None):
        return "hdf"

class WCS20GetCoverageCompressionLZWTestCase(testbase.RectifiedGridCoverageTestCase):
    def getRequest(self):
        params = "service=wcs&version=2.0.0&request=GetCoverage&CoverageId=mosaic_MER_FRS_1P_RGB_reduced&format=%s" % quote("image/tiff;compress=LZW")
        return (params, "kvp")

class WCS20GetCoverageCompressionJPEGTestCase(testbase.RectifiedGridCoverageTestCase):
    def getRequest(self):
        params = "service=wcs&version=2.0.0&request=GetCoverage&CoverageId=mosaic_MER_FRS_1P_RGB_reduced&format=%s" % quote("image/tiff;compress=JPEG;jpeg_quality=50")
        return (params, "kvp")

class WCS20GetCoverageTiledTestCase(testbase.RectifiedGridCoverageTestCase):
    def getRequest(self):
        params = "service=wcs&version=2.0.0&request=GetCoverage&CoverageId=mosaic_MER_FRS_1P_RGB_reduced&format=%s" % quote("image/tiff;tiled=YES")
        return (params, "kvp")

# TODO: Enable test once subdatasets are supported (see #123):
#class WCS20GetCoverageNetCDFInputTestCase(testbase.RectifiedGridCoverageTestCase):
#    def getRequest(self):
#        params = "service=wcs&version=2.0.0&request=GetCoverage&CoverageId=MER_FRS_1PNPDE20060816_090929_000001972050_00222_23322_0058_uint16_reduced_compressed_netCDF&format=image/tiff"
#        return (params, "kvp")

class WCS20GetCoverageJPEG2000InputTestCase(testbase.RectifiedGridCoverageTestCase):
    def getRequest(self):
        params = "service=wcs&version=2.0.0&request=GetCoverage&CoverageId=mosaic_MER_FRS_1PNPDE20060816_090929_000001972050_00222_23322_0058_RGB_reduced_JPEG2000&format=image/tiff"
        return (params, "kvp")
    
#===============================================================================
# WCS 2.0: Multipart requests
#===============================================================================

class WCS20GetCoverageMultipartMosaicTestCase(testbase.WCS20GetCoverageRectifiedGridCoverageMultipartTestCase):
    def getRequest(self):
        params = "service=wcs&version=2.0.1&request=GetCoverage&CoverageId=mosaic_MER_FRS_1P_RGB_reduced&format=image/tiff&mediatype=multipart/related"
        return (params, "kvp")

class WCS20GetCoverageMultipartDatasetTestCase(testbase.WCS20GetCoverageRectifiedGridCoverageMultipartTestCase):
    def getRequest(self):
        params = "service=wcs&version=2.0.1&request=GetCoverage&CoverageId=MER_FRS_1PNPDE20060822_092058_000001972050_00308_23408_0077_uint16_reduced_compressed&format=image/tiff&mediatype=multipart/related"
        return (params, "kvp")

# TODO: wrong multipart parameters only result in non-multipart images. Uncomment, when implemented
#class WCS20GetCoverageWrongMultipartParameterFaultTestCase(testbase.ExceptionTestCase):
#    def getRequest(self):
#        params = "service=wcs&version=2.0.1&request=GetCoverage&CoverageId=mosaic_MER_FRS_1P_RGB_reduced&format=image/tiff&mediatype=multipart/something"
#        return (params, "kvp")
#
#    def getExpectedExceptionCode(self):
#        return "InvalidParameterValue"

#===============================================================================
# WCS 2.0: Subset requests
#===============================================================================

class WCS20GetCoverageSubsetDatasetTestCase(testbase.RectifiedGridCoverageTestCase):
    def getRequest(self):
        params = "service=wcs&version=2.0.1&request=GetCoverage&CoverageId=MER_FRS_1PNPDE20060822_092058_000001972050_00308_23408_0077_uint16_reduced_compressed&format=image/tiff&subset=x(100,200)&subset=y(200,300)"
        return (params, "kvp")

class WCS20GetCoverageMultipartSubsetMosaicTestCase(testbase.WCS20GetCoverageRectifiedGridCoverageMultipartTestCase):
    def getRequest(self):
        params = "service=wcs&version=2.0.1&request=GetCoverage&CoverageId=mosaic_MER_FRS_1P_RGB_reduced&format=image/tiff&mediatype=multipart/related&subset=x(100,1000)&subset=y(0,99)"
        return (params, "kvp")

class WCS20GetCoverageMultipartSubsetDatasetTestCase(testbase.WCS20GetCoverageRectifiedGridCoverageMultipartTestCase):
    def getRequest(self):
        params = "service=wcs&version=2.0.1&request=GetCoverage&CoverageId=MER_FRS_1PNPDE20060822_092058_000001972050_00308_23408_0077_uint16_reduced_compressed&format=image/tiff&mediatype=multipart/related&subset=x(100,200)&subset=y(200,300)"
        return (params, "kvp")

class WCS20GetCoverageSubsetEPSG4326DatasetTestCase(testbase.RectifiedGridCoverageTestCase):
    def getRequest(self):
        params = "service=wcs&version=2.0.1&request=GetCoverage&CoverageId=MER_FRS_1PNPDE20060822_092058_000001972050_00308_23408_0077_uint16_reduced_compressed&format=image/tiff&subset=lat,http://www.opengis.net/def/crs/EPSG/0/4326(38,40)&subset=long,http://www.opengis.net/def/crs/EPSG/0/4326(20,22)"
        return (params, "kvp")
    
class WCS20GetCoverageSubsetEPSG4326MosaicTestCase(testbase.RectifiedGridCoverageTestCase):
    def getRequest(self):
        params = "service=wcs&version=2.0.1&request=GetCoverage&CoverageId=mosaic_MER_FRS_1P_RGB_reduced&format=image/tiff&subset=lat,http://www.opengis.net/def/crs/EPSG/0/4326(38,40)&subset=long,http://www.opengis.net/def/crs/EPSG/0/4326(0,30)"
        return (params, "kvp")

class WCS20GetCoverageSubsetInvalidEPSGFaultTestCase(testbase.ExceptionTestCase):
    def getRequest(self):
        params = "service=wcs&version=2.0.1&request=GetCoverage&CoverageId=mosaic_MER_FRS_1P_RGB_reduced&format=image/tiff&subset=x,http://www.opengis.net/def/crs/EPSG/0/99999(38,40)&subset=y,http://www.opengis.net/def/crs/EPSG/0/99999(20,22)"
        return (params, "kvp")
    
    def getExpectedExceptionCode(self):
        return "InvalidParameterValue"

#===============================================================================
# WCS 2.0: OutputCRS
#===============================================================================

class WCS20GetCoverageOutputCRSDatasetTestCase(testbase.WCS20GetCoverageRectifiedGridCoverageMultipartTestCase):
    def getRequest(self):
        params = "service=wcs&version=2.0.1&request=GetCoverage&CoverageId=MER_FRS_1PNPDE20060822_092058_000001972050_00308_23408_0077_uint16_reduced_compressed&format=image/tiff&mediatype=multipart/related&outputcrs=http://www.opengis.net/def/crs/EPSG/0/3035"
        return (params, "kvp")

class WCS20GetCoverageOutputCRSotherUoMDatasetTestCase(testbase.WCS20GetCoverageRectifiedGridCoverageMultipartTestCase):
    def getRequest(self):
        params = "service=wcs&version=2.0.1&request=GetCoverage&CoverageId=MER_FRS_1PNPDE20060822_092058_000001972050_00308_23408_0077_uint16_reduced_compressed&format=image/tiff&mediatype=multipart/related&outputcrs=http://www.opengis.net/def/crs/EPSG/0/3857"
        return (params, "kvp")

#===============================================================================
# WCS 2.0: Size
#===============================================================================

class WCS20GetCoverageSizeDatasetTestCase(testbase.RectifiedGridCoverageTestCase):
    def getRequest(self):
        params = "service=wcs&version=2.0.0&request=GetCoverage&CoverageId=MER_FRS_1PNPDE20060822_092058_000001972050_00308_23408_0077_uint16_reduced_compressed&format=image/tiff&size=x(200)&size=y(200)"
        return (params, "kvp")

class WCS20GetCoverageSizeMosaicTestCase(testbase.RectifiedGridCoverageTestCase):
    def getRequest(self):
        params = "service=wcs&version=2.0.0&request=GetCoverage&CoverageId=mosaic_MER_FRS_1P_RGB_reduced&format=image/tiff&size=x(200)&size=y(400)"
        return (params, "kvp")

class WCS20GetCoverageSubsetSizeDatasetTestCase(testbase.RectifiedGridCoverageTestCase):
    def getRequest(self):
        params = "service=wcs&version=2.0.0&request=GetCoverage&CoverageId=MER_FRS_1PNPDE20060822_092058_000001972050_00308_23408_0077_uint16_reduced_compressed&format=image/tiff&subset=x(100,200)&subset=y(200,300)&size=x(20)&size=y(20)"
        return (params, "kvp")

class WCS20GetCoverageSubsetEPSG4326SizeDatasetTestCase(testbase.WCS20GetCoverageRectifiedGridCoverageMultipartTestCase):
    def getRequest(self):
        params = "service=wcs&version=2.0.1&request=GetCoverage&CoverageId=MER_FRS_1PNPDE20060822_092058_000001972050_00308_23408_0077_uint16_reduced_compressed&format=image/tiff&mediatype=multipart/related&subset=lat,http://www.opengis.net/def/crs/EPSG/0/4326(38,40)&subset=long,http://www.opengis.net/def/crs/EPSG/0/4326(20,22)&size=lat(20)&size=long(20)"
        return (params, "kvp")
    
class WCS20GetCoverageSubsetEPSG4326SizeExceedsExtentDatasetTestCase(testbase.WCS20GetCoverageRectifiedGridCoverageMultipartTestCase):
    def getRequest(self):
        params = "service=wcs&version=2.0.1&request=GetCoverage&CoverageId=MER_FRS_1PNPDE20060822_092058_000001972050_00308_23408_0077_uint16_reduced_compressed&format=image/tiff&subset=lat,http://www.opengis.net/def/crs/EPSG/0/4326(10,50)&subset=long,http://www.opengis.net/def/crs/EPSG/0/4326(0,50)&size=lat(100)&size=long(100)&mediatype=multipart/related"
        return (params, "kvp")

class WCS20GetCoverageInvalidSizeFaultTestCase(testbase.ExceptionTestCase):
    def getRequest(self):
        params = "service=wcs&version=2.0.0&request=GetCoverage&CoverageId=mosaic_MER_FRS_1P_RGB_reduced&format=image/tiff&size=x(1.11)"
        return (params, "kvp")
    
    def getExpectedExceptionCode(self):
        return "InvalidParameterValue"

#===============================================================================
# WCS 2.0: Resolution
#===============================================================================

class WCS20GetCoverageResolutionDatasetTestCase(testbase.RectifiedGridCoverageTestCase):
    def getRequest(self):
        params = "service=wcs&version=2.0.0&request=GetCoverage&CoverageId=MER_FRS_1PNPDE20060822_092058_000001972050_00308_23408_0077_uint16_reduced_compressed&format=image/tiff&resolution=x(0.1)&resolution=y(0.1)"
        return (params, "kvp")
    
class WCS20GetCoverageResolutionMosaicTestCase(testbase.RectifiedGridCoverageTestCase):
    def getRequest(self):
        params = "service=wcs&version=2.0.0&request=GetCoverage&CoverageId=mosaic_MER_FRS_1P_RGB_reduced&format=image/tiff&resolution=x(0.1)&resolution=y(0.1)"
        return (params, "kvp")

class WCS20GetCoverageSubsetResolutionDatasetTestCase(testbase.RectifiedGridCoverageTestCase):
    def getRequest(self):
        params = "service=wcs&version=2.0.0&request=GetCoverage&CoverageId=MER_FRS_1PNPDE20060822_092058_000001972050_00308_23408_0077_uint16_reduced_compressed&format=image/tiff&subset=x(100,200)&subset=y(200,300)&resolution=x(0.1)&resolution=y(0.1)"
        return (params, "kvp")

class WCS20GetCoverageSubsetEPSG4326ResolutionLatLonDatasetTestCase(testbase.RectifiedGridCoverageTestCase):
    def getRequest(self):
        params = "service=wcs&version=2.0.0&request=GetCoverage&CoverageId=MER_FRS_1PNPDE20060822_092058_000001972050_00308_23408_0077_uint16_reduced_compressed&format=image/tiff&subset=lat,http://www.opengis.net/def/crs/EPSG/0/4326(38,40)&subset=long,http://www.opengis.net/def/crs/EPSG/0/4326(20,22)&resolution=lat(0.01)&resolution=long(0.01)"
        return (params, "kvp")

class WCS20GetCoverageSubsetEPSG4326ResolutionInvalidAxisDatasetFaultTestCase(testbase.ExceptionTestCase):
    def getRequest(self):
        params = "service=wcs&version=2.0.0&request=GetCoverage&CoverageId=MER_FRS_1PNPDE20060822_092058_000001972050_00308_23408_0077_uint16_reduced_compressed&format=image/tiff&subset=lat,http://www.opengis.net/def/crs/EPSG/0/4326(38,40)&subset=long,http://www.opengis.net/def/crs/EPSG/0/4326(20,22)&resolution=x(0.01)&resolution=y(0.01)"
        return (params, "kvp")
    
    def getExpectedExceptionCode(self):
        return "InvalidParameterValue"

#===============================================================================
# WCS 2.0: Rangesubset
#===============================================================================

class WCS20GetCoverageRangeSubsetIndicesDatasetTestCase(testbase.RectifiedGridCoverageTestCase):
    def getRequest(self):
        params = "service=wcs&version=2.0.0&request=GetCoverage&CoverageId=MER_FRS_1PNPDE20060822_092058_000001972050_00308_23408_0077_uint16_reduced_compressed&format=image/tiff&rangesubset=1,2,3"
        return (params, "kvp")

class WCS20GetCoverageRangeSubsetNamesDatasetTestCase(testbase.RectifiedGridCoverageTestCase):
    def getRequest(self):
        params = "service=wcs&version=2.0.0&request=GetCoverage&CoverageId=MER_FRS_1PNPDE20060822_092058_000001972050_00308_23408_0077_uint16_reduced_compressed&format=image/tiff&rangesubset=MERIS_radiance_04_uint16,MERIS_radiance_05_uint16,MERIS_radiance_06_uint16"
        return (params, "kvp")

class WCS20GetCoverageRangeSubsetNamesPNGDatasetTestCase(testbase.RectifiedGridCoverageTestCase):
    def getRequest(self):
        params = "service=wcs&version=2.0.0&request=GetCoverage&CoverageId=MER_FRS_1PNPDE20060822_092058_000001972050_00308_23408_0077_uint16_reduced_compressed&format=image/png&rangesubset=1"
        return (params, "kvp")

    def getFileExtension(self, part=None):
        return "png"

class WCS20GetCoverageMultipartRangeSubsetNamesDatasetTestCase(testbase.WCS20GetCoverageRectifiedGridCoverageMultipartTestCase):
    def getRequest(self):
        params = "service=wcs&version=2.0.1&request=GetCoverage&CoverageId=MER_FRS_1PNPDE20060822_092058_000001972050_00308_23408_0077_uint16_reduced_compressed&format=image/tiff&mediatype=multipart/related&rangesubset=MERIS_radiance_04_uint16,MERIS_radiance_05_uint16,MERIS_radiance_06_uint16"
        return (params, "kvp")

class WCS20GetCoverageSubsetSizeResolutionOutputCRSRangeSubsetIndicesDatasetTestCase(testbase.WCS20GetCoverageRectifiedGridCoverageMultipartTestCase):
    def getRequest(self):
        params = "service=wcs&version=2.0.1&request=GetCoverage&CoverageId=MER_FRS_1PNPDE20060822_092058_000001972050_00308_23408_0077_uint16_reduced_compressed&format=image/tiff&subset=x(100,200)&subset=y(200,300)&size=y(100)&resolution=x(0.1)&outputcrs=http://www.opengis.net/def/crs/EPSG/0/3035&rangesubset=1,2,3&mediatype=multipart/related"
        return (params, "kvp")
    
#===============================================================================
# WCS 2.0: Polygon Mask 
#===============================================================================

# TODO: Enable these tests once the feature is implemented in MapServer

#class WCS20GetCoveragePolygonMaskTestCase(testbase.RectifiedGridCoverageTestCase):
#    def getRequest(self):
#        params = "service=wcs&version=2.0.0&request=GetCoverage&CoverageId=MER_FRS_1PNPDE20060822_092058_000001972050_00308_23408_0077_uint16_reduced_compressed&format=image/tiff&mask=polygon(14.124422306243844,42.806626286621963,21.208516509273601,43.730638573973678,21.208516509273601,43.730638573973678,21.892970055460054,37.8443380767702,15.04843459359555,36.646544370943914,12.379065763468395,39.555471942236323,14.124422306243844,42.806626286621963)"
#        return (params, "kvp") 


#class WCS20GetCoveragePolygonMaskProjectedTestCase(testbase.RectifiedGridCoverageTestCase):
#    def getRequest(self): # TODO: swap axes
#        params = "service=wcs&version=2.0.0&request=GetCoverage&CoverageId=MER_FRS_1PNPDE20060822_092058_000001972050_00308_23408_0077_uint16_reduced_compressed&format=image/tiff&mask=polygon,http://www.opengis.net/def/crs/EPSG/0/4326(42.806626286621963,14.124422306243844,43.730638573973678,21.208516509273601,43.730638573973678,21.208516509273601,37.8443380767702,21.892970055460054,36.646544370943914,15.04843459359555,39.555471942236323,12.379065763468395,42.806626286621963,14.124422306243844)" 
#        return (params, "kvp")

#class WCS20PostGetCoveragePolygonMaskTestCase(testbase.RectifiedGridCoverageTestCase):
#    def getRequest(self):
#        params = """<wcs:GetCoverage service="WCS" version="2.0.0"
#           xmlns:wcs="http://www.opengis.net/wcs/2.0"
#           xmlns:wcsmask="http://www.opengis.net/wcs/mask/1.0">
#          <wcs:CoverageId>MER_FRS_1PNPDE20060822_092058_000001972050_00308_23408_0077_uint16_reduced_compressed</wcs:CoverageId>
#          <wcs:format>image/tiff</wcs:format>
#          <wcs:Extension>
#            <wcsmask:polygonMask>14.124422306243844 42.806626286621963 21.208516509273601 43.730638573973678 21.208516509273601 43.730638573973678 21.892970055460054 37.8443380767702 15.04843459359555 36.646544370943914 12.379065763468395 39.555471942236323 14.124422306243844 42.806626286621963</wcsmask:polygonMask>
#          </wcs:Extension>
#        </wcs:GetCoverage>"""
#        return (params, "xml")

#===============================================================================
# WCS 2.0 Rasdaman test cases
#===============================================================================

class WCS20GetCoverageRasdamanMultipartDatasetTestCase(testbase.RasdamanTestCaseMixIn, testbase.WCS20GetCoverageRectifiedGridCoverageMultipartTestCase):
    def getRequest(self):
        params = "service=wcs&version=2.0.1&request=GetCoverage&CoverageId=mosaic_MER_FRS_1PNPDE20060830_100949_000001972050_00423_23523_0079_RGB_reduced_rasdaman&format=image/tiff&mediatype=multipart/related"
        return (params, "kvp")   

class WCS20GetCoverageRasdamanMultipartDatasetSubsetTestCase(testbase.RasdamanTestCaseMixIn, testbase.WCS20GetCoverageRectifiedGridCoverageMultipartTestCase):
    def getRequest(self):
        params = "service=wcs&version=2.0.1&request=GetCoverage&CoverageId=mosaic_MER_FRS_1PNPDE20060830_100949_000001972050_00423_23523_0079_RGB_reduced_rasdaman&format=image/tiff&mediatype=multipart/related&subset=x(100,200)&subset=y(200,300)"
        return (params, "kvp")

class WCS20GetCoverageRasdamanMultipartDatasetSizeTestCase(testbase.RasdamanTestCaseMixIn, testbase.WCS20GetCoverageRectifiedGridCoverageMultipartTestCase):
    def getRequest(self):
        params = "service=wcs&version=2.0.1&request=GetCoverage&CoverageId=mosaic_MER_FRS_1PNPDE20060830_100949_000001972050_00423_23523_0079_RGB_reduced_rasdaman&format=image/tiff&mediatype=multipart/related&size=x(100)&size=y(100)"
        return (params, "kvp")

class WCS20GetCoverageRasdamanMultipartDatasetResolutionTestCase(testbase.RasdamanTestCaseMixIn, testbase.WCS20GetCoverageRectifiedGridCoverageMultipartTestCase):
    def getRequest(self):
        params = "service=wcs&version=2.0.1&request=GetCoverage&CoverageId=mosaic_MER_FRS_1PNPDE20060830_100949_000001972050_00423_23523_0079_RGB_reduced_rasdaman&format=image/tiff&mediatype=multipart/related&resolution=x(0.1)&resolution=y(0.1)"
        return (params, "kvp")

class WCS20GetCoverageRasdamanMultipartDatasetOutputCRSTestCase(testbase.RasdamanTestCaseMixIn, testbase.WCS20GetCoverageRectifiedGridCoverageMultipartTestCase):
    def getRequest(self):
        params = "service=wcs&version=2.0.1&request=GetCoverage&CoverageId=mosaic_MER_FRS_1PNPDE20060830_100949_000001972050_00423_23523_0079_RGB_reduced_rasdaman&format=image/tiff&mediatype=multipart/related&outputcrs=http://www.opengis.net/def/crs/EPSG/0/3035"
        return (params, "kvp")

class WCS20GetCoverageRasdamanMultipartDatasetSubsetSizeTestCase(testbase.RasdamanTestCaseMixIn, testbase.WCS20GetCoverageRectifiedGridCoverageMultipartTestCase):
    def getRequest(self):
        params = "service=wcs&version=2.0.1&request=GetCoverage&CoverageId=mosaic_MER_FRS_1PNPDE20060830_100949_000001972050_00423_23523_0079_RGB_reduced_rasdaman&format=image/tiff&mediatype=multipart/related&subset=x(100,200)&subset=y(200,300)&size=x(20)&size=y(20)"
        return (params, "kvp")

class WCS20GetCoverageRasdamanMultipartDatasetSubsetResolutionTestCase(testbase.RasdamanTestCaseMixIn, testbase.WCS20GetCoverageRectifiedGridCoverageMultipartTestCase):
    def getRequest(self):
        params = "service=wcs&version=2.0.1&request=GetCoverage&CoverageId=mosaic_MER_FRS_1PNPDE20060830_100949_000001972050_00423_23523_0079_RGB_reduced_rasdaman&format=image/tiff&mediatype=multipart/related&subset=x(100,200)&subset=y(200,300)&resolution=x(0.1)&resolution=y(0.1)"
        return (params, "kvp")

class WCS20GetCoverageRasdamanMultipartDatasetRangeSubsetTestCase(testbase.RasdamanTestCaseMixIn, testbase.WCS20GetCoverageRectifiedGridCoverageMultipartTestCase):
    def getRequest(self):
        params = "service=wcs&version=2.0.1&request=GetCoverage&CoverageId=mosaic_MER_FRS_1PNPDE20060830_100949_000001972050_00423_23523_0079_RGB_reduced_rasdaman&format=image/tiff&mediatype=multipart/related&rangesubset=1"
        return (params, "kvp")

class WCS20GetCoverageRasdamanSubsetSizeResolutionOutputCRSRangeSubsetIndicesDatasetTestCase(testbase.RasdamanTestCaseMixIn, testbase.WCS20GetCoverageRectifiedGridCoverageMultipartTestCase):
    def getRequest(self):
        params = "service=wcs&version=2.0.1&request=GetCoverage&CoverageId=mosaic_MER_FRS_1PNPDE20060830_100949_000001972050_00423_23523_0079_RGB_reduced_rasdaman&format=image/tiff&subset=x(100,200)&subset=y(200,300)&size=y(100)&resolution=x(0.1)&outputcrs=http://www.opengis.net/def/crs/EPSG/0/3035&rangesubset=1,2,3&mediatype=multipart/related"
        return (params, "kvp")


#===============================================================================
# WCS 2.0: GetCov with EPSG:3035 input images 
#===============================================================================

class WCS20DescribeCoverageReprojectedDatasetTestCase(testbase.XMLTestCase):
    fixtures = testbase.OWSTestCase.fixtures + ["testing_reprojected_coverages.json"]
    def getRequest(self):
        params = "service=WCS&version=2.0.0&request=DescribeCoverage&CoverageId=MER_FRS_1PNPDE20060816_090929_000001972050_00222_23322_0058_uint16_reduced_compressed_reprojected"
        return (params, "kvp")

class WCS20GetCoverageReprojectedDatasetTestCase(testbase.RectifiedGridCoverageTestCase):
    fixtures = testbase.OWSTestCase.fixtures + ["testing_reprojected_coverages.json"]
    def getRequest(self):
        params = "service=wcs&version=2.0.0&request=GetCoverage&CoverageId=MER_FRS_1PNPDE20060816_090929_000001972050_00222_23322_0058_uint16_reduced_compressed_reprojected&format=image/tiff"
        return (params, "kvp")

class WCS20GetCoverageReprojectedSubsetDatasetTestCase(testbase.RectifiedGridCoverageTestCase):
    fixtures = testbase.OWSTestCase.fixtures + ["testing_reprojected_coverages.json"]
    def getRequest(self):
        params = "service=wcs&version=2.0.0&request=GetCoverage&CoverageId=MER_FRS_1PNPDE20060816_090929_000001972050_00222_23322_0058_uint16_reduced_compressed_reprojected&format=image/tiff&subset=x(100,200)&subset=y(200,300)"
        return (params, "kvp")
    
class WCS20GetCoverageReprojectedSubsetEPSG4326DatasetTestCase(testbase.WCS20GetCoverageRectifiedGridCoverageMultipartTestCase):
    fixtures = testbase.OWSTestCase.fixtures + ["testing_reprojected_coverages.json"]
    def getRequest(self):
        params = "service=wcs&version=2.0.1&request=GetCoverage&CoverageId=MER_FRS_1PNPDE20060816_090929_000001972050_00222_23322_0058_uint16_reduced_compressed_reprojected&format=image/tiff&mediatype=multipart/related&subset=lat,http://www.opengis.net/def/crs/EPSG/0/4326(38,40)&subset=long,http://www.opengis.net/def/crs/EPSG/0/4326(20,22)"
        return (params, "kvp")

class WCS20GetCoverageReprojectedMultipartDatasetTestCase(testbase.WCS20GetCoverageRectifiedGridCoverageMultipartTestCase):
    fixtures = testbase.OWSTestCase.fixtures + ["testing_reprojected_coverages.json"]
    def getRequest(self):
        params = "service=wcs&version=2.0.1&request=GetCoverage&CoverageId=MER_FRS_1PNPDE20060816_090929_000001972050_00222_23322_0058_uint16_reduced_compressed_reprojected&format=image/tiff&mediatype=multipart/related"
        return (params, "kvp")

class WCS20GetCoverageReprojectedEPSG3857DatasetTestCase(testbase.WCS20GetCoverageRectifiedGridCoverageMultipartTestCase):
    fixtures = testbase.OWSTestCase.fixtures + ["testing_reprojected_coverages.json"]
    def getRequest(self):
        params = "service=wcs&version=2.0.1&request=GetCoverage&CoverageId=MER_FRS_1PNPDE20060816_090929_000001972050_00222_23322_0058_uint16_reduced_compressed_reprojected&format=image/tiff&mediatype=multipart/related&outputcrs=http://www.opengis.net/def/crs/EPSG/0/3857"
        return (params, "kvp")

#===============================================================================
# WCS 2.0 Referenceable Grid Coverages
#===============================================================================

class WCS20DescribeCoverageReferenceableDatasetTestCase(testbase.XMLTestCase):
    """This test shall retrieve a valid WCS 2.0 EO-AP (EO-WCS) DescribeCoverage response for a wcseo:ReferenceableDataset."""
    def getRequest(self):
        params = "service=WCS&version=2.0.0&request=DescribeCoverage&CoverageId=ASA_WSM_1PNDPA20050331_075939_000000552036_00035_16121_0775"
        return (params, "kvp")

class WCS20GetCoverageReferenceableDatasetTestCase(testbase.WCS20GetCoverageReferenceableGridCoverageMultipartTestCase):
    def getRequest(self):
        params = "service=wcs&version=2.0.1&request=GetCoverage&CoverageId=ASA_WSM_1PNDPA20050331_075939_000000552036_00035_16121_0775&format=image/tiff&mediatype=multipart/related"
        return (params, "kvp")

class WCS20GetCoverageReferenceableDatasetImageCRSSubsetTestCase(testbase.WCS20GetCoverageReferenceableGridCoverageMultipartTestCase):
    def getRequest(self):
        params = "service=wcs&version=2.0.1&request=GetCoverage&CoverageId=ASA_WSM_1PNDPA20050331_075939_000000552036_00035_16121_0775&format=image/tiff&mediatype=multipart/related&subset=x(0,99)&subset=y(0,99)"
        return (params, "kvp")

class WCS20GetCoverageReferenceableDatasetGeogCRSSubsetTestCase(testbase.WCS20GetCoverageReferenceableGridCoverageMultipartTestCase):
    def getRequest(self):
        params = "service=wcs&version=2.0.0&request=GetCoverage&CoverageId=ASA_WSM_1PNDPA20050331_075939_000000552036_00035_16121_0775&format=image/tiff&mediatype=multipart/mixed&subset=x,http://www.opengis.net/def/crs/EPSG/0/4326(18.0,20.0)&subset=y,http://www.opengis.net/def/crs/EPSG/0/4326(-34.5,-33.5)"
        return (params, "kvp")

class WCS20GetCoverageReferenceableDatasetGeogCRSSubsetExceedsExtentTestCase(testbase.WCS20GetCoverageReferenceableGridCoverageMultipartTestCase):
    def getRequest(self):
        params = "service=wcs&version=2.0.0&request=GetCoverage&CoverageId=ASA_WSM_1PNDPA20050331_075939_000000552036_00035_16121_0775&format=image/tiff&mediatype=multipart/mixed&subset=x,http://www.opengis.net/def/crs/EPSG/0/4326(18,23)&subset=y,http://www.opengis.net/def/crs/EPSG/0/4326(-35,-33)"
        return (params, "kvp")

class WCS20GetCoverageReferenceableDatasetGeogCRSSubsetOutsideExtentTestCase(testbase.ExceptionTestCase):
    def getRequest(self):
        params = "service=wcs&version=2.0.0&request=GetCoverage&CoverageId=ASA_WSM_1PNDPA20050331_075939_000000552036_00035_16121_0775&format=image/tiff&mediatype=multipart/mixed&subset=x,http://www.opengis.net/def/crs/EPSG/0/4326(14.5,16.5)&subset=y,http://www.opengis.net/def/crs/EPSG/0/4326(-34.5,-33.5)"
        return (params, "kvp")

    def getExpectedHTTPStatus(self):
        return 400
    
    def getExpectedExceptionCode(self):
        return "InvalidParameterValue"

#===============================================================================
# WCS 2.0.1 Corrigendum test cases
#===============================================================================


class WCS20CorrigendumGetCapabilitiesEmptyTestCase(testbase.XMLTestCase):
    """This test shall retrieve a valid but empty WCS 2.0.1 EO-AP (EO-WCS) GetCapabilities response (see #162)"""
    fixtures = testbase.BASE_FIXTURES
    
    def getRequest(self):
        params = "service=WCS&version=2.0.1&request=GetCapabilities"
        return (params, "kvp")


class WCS20CorrigendumDescribeCoverageDatasetTestCase(testbase.XMLTestCase):
    """This test shall retrieve a valid WCS 2.0.1 EO-AP (EO-WCS) DescribeCoverage response for a wcseo:RectifiedDataset (see #162)."""
    def getRequest(self):
        params = "service=WCS&version=2.0.1&request=DescribeCoverage&CoverageId=MER_FRS_1PNPDE20060822_092058_000001972050_00308_23408_0077_uint16_reduced_compressed"
        return (params, "kvp")


class WCS20CorrigendumDescribeEOCoverageSetMosaicTestCase(testbase.XMLTestCase):
    """This test shall retrieve a valid WCS 2.0.1 EO-AP (EO-WCS) DescribeEOCoverageSet response for a wcseo:RectifiedStitchedMosaic (see #162)"""
    def getRequest(self):
        params = "service=WCS&version=2.0.1&request=DescribeEOCoverageSet&eoId=mosaic_MER_FRS_1P_RGB_reduced"
        return (params, "kvp")


class WCS20CorrigendumGetCoverageDatasetTestCase(testbase.RectifiedGridCoverageTestCase):
    def getRequest(self):
        params = "service=wcs&version=2.0.1&request=GetCoverage&CoverageId=MER_FRS_1PNPDE20060822_092058_000001972050_00308_23408_0077_uint16_reduced_compressed"
        return (params, "kvp")


#===============================================================================
# WCS 2.0 - POST
#===============================================================================

class WCS20PostGetCapabilitiesValidTestCase(testbase.XMLTestCase):
    """This test shall retrieve a valid WCS 2.0 EO-AP (EO-WCS) GetCapabilities response
       via POST.
    """
    def getRequest(self):
        params = """<ns:GetCapabilities updateSequence="u2001" service="WCS"
          xmlns:ns="http://www.opengis.net/wcs/2.0"
          xmlns:ns1="http://www.opengis.net/ows/2.0">
            <ns1:AcceptVersions><ns1:Version>2.0.0</ns1:Version></ns1:AcceptVersions>
          </ns:GetCapabilities>
        """        
        return (params, "xml")

class WCS20PostDescribeCoverageDatasetTestCase(testbase.XMLTestCase):
    """This test shall retrieve a valid WCS 2.0 EO-AP (EO-WCS) DescribeCoverage response 
       for a wcseo:RectifiedDataset via POST.
    """
    def getRequest(self):
        params = """<ns:DescribeCoverage 
           xmlns:ns="http://www.opengis.net/wcs/2.0" service="WCS" version="2.0.0">
         <ns:CoverageId>MER_FRS_1PNPDE20060816_090929_000001972050_00222_23322_0058_uint16_reduced_compressed</ns:CoverageId>
        </ns:DescribeCoverage>"""
        return (params, "xml")

class WCS20PostDescribeEOCoverageSetDatasetSeriesTestCase(testbase.XMLTestCase):
    """This test shall retrieve a valid WCS 2.0 EO-AP (EO-WCS) DescribeEOCoverageSet response
    for a wcseo:RectifiedDatasetSeries via POST.
    """
    def getRequest(self):
        params = """<wcseo:DescribeEOCoverageSet service="WCS" version="2.0.0" count="100"
           xmlns:wcseo="http://www.opengis.net/wcseo/1.0"
           xmlns:wcs="http://www.opengis.net/wcs/2.0">     
          <wcseo:eoId>MER_FRS_1P_reduced</wcseo:eoId>
          <wcseo:containment>OVERLAPS</wcseo:containment>
          <wcseo:Sections>
            <wcseo:Section>All</wcseo:Section>
          </wcseo:Sections>
          <wcs:DimensionTrim>
            <wcs:Dimension>Long</wcs:Dimension>
            <wcs:TrimLow>16</wcs:TrimLow>
            <wcs:TrimHigh>18</wcs:TrimHigh>
          </wcs:DimensionTrim>
          <wcs:DimensionTrim>
            <wcs:Dimension>Lat</wcs:Dimension>
            <wcs:TrimLow>46</wcs:TrimLow>
            <wcs:TrimHigh>48</wcs:TrimHigh>
          </wcs:DimensionTrim>
        </wcseo:DescribeEOCoverageSet>"""
        return (params, "xml")

class WCS20PostGetCoverageMultipartDatasetTestCase(testbase.WCS20GetCoverageRectifiedGridCoverageMultipartTestCase):
    def getRequest(self):
        params = """<wcs:GetCoverage service="WCS" version="2.0.1"
           xmlns:wcs="http://www.opengis.net/wcs/2.0">
          <wcs:CoverageId>mosaic_MER_FRS_1PNPDE20060816_090929_000001972050_00222_23322_0058_RGB_reduced</wcs:CoverageId>
          <wcs:format>image/tiff</wcs:format>
          <wcs:mediaType>multipart/related</wcs:mediaType>
        </wcs:GetCoverage>"""
        return (params, "xml")

class WCS20PostGetCoverageSubsetMultipartDatasetTestCase(testbase.WCS20GetCoverageRectifiedGridCoverageMultipartTestCase):
    def getRequest(self):
        params = """<wcs:GetCoverage service="WCS" version="2.0.1"
           xmlns:wcs="http://www.opengis.net/wcs/2.0">
          <wcs:CoverageId>mosaic_MER_FRS_1PNPDE20060816_090929_000001972050_00222_23322_0058_RGB_reduced</wcs:CoverageId>
          <wcs:DimensionTrim>
            <wcs:Dimension>x</wcs:Dimension>
            <wcs:TrimLow>0</wcs:TrimLow>
            <wcs:TrimHigh>99</wcs:TrimHigh>
          </wcs:DimensionTrim>
          <wcs:DimensionTrim>
            <wcs:Dimension>y</wcs:Dimension>
            <wcs:TrimLow>0</wcs:TrimLow>
            <wcs:TrimHigh>99</wcs:TrimHigh>
          </wcs:DimensionTrim>
          <wcs:format>image/tiff</wcs:format>
          <wcs:mediaType>multipart/related</wcs:mediaType>
        </wcs:GetCoverage>"""
        return (params, "xml")

# TODO: Enable once CRS handling with POST requests is implemented in MapServer
# TODO: Adjust to final namespace maybe "http://www.opengis.net/wcs_service-extension_crs/1.0"
#class WCS20PostGetCoverageSubsetEPSG4326MultipartDatasetTestCase(testbase.WCS20GetCoverageRectifiedGridCoverageMultipartTestCase):
#    def getRequest(self):
#        params = """<wcs:GetCoverage service="WCS" version="2.0.1"
#           xmlns:wcs="http://www.opengis.net/wcs/2.0" 
#           xmlns:wcscrs="http://www.opengis.net/wcs/extensions/crs/1.0">
#          <wcs:Extension>
#            <wcscrs:GetCoverageCrs>
#              <wcscrs:subsettingCrs>http://www.opengis.net/def/crs/EPSG/0/4326</wcscrs:subsettingCrs>
#            </wcscrs:GetCoverageCrs>
#          </wcs:Extension>
#          <wcs:CoverageId>mosaic_MER_FRS_1PNPDE20060816_090929_000001972050_00222_23322_0058_RGB_reduced</wcs:CoverageId>
#          <wcs:DimensionTrim>
#            <wcs:Dimension>Long</wcs:Dimension>
#            <wcs:TrimLow>20</wcs:TrimLow>
#            <wcs:TrimHigh>22</wcs:TrimHigh>
#          </wcs:DimensionTrim>
#          <wcs:DimensionTrim>
#            <wcs:Dimension>Lat</wcs:Dimension>
#            <wcs:TrimLow>36</wcs:TrimLow>
#            <wcs:TrimHigh>38</wcs:TrimHigh>
#          </wcs:DimensionTrim>
#          <wcs:format>image/tiff</wcs:format>
#          <wcs:mediaType>multipart/related</wcs:mediaType>
#        </wcs:GetCoverage>"""
#        return (params, "xml")

class WCS20PostGetCoverageReferenceableMultipartDatasetTestCase(testbase.WCS20GetCoverageReferenceableGridCoverageMultipartTestCase):
    def getRequest(self):
        params = """<wcs:GetCoverage service="WCS" version="2.0.1"
           xmlns:wcs="http://www.opengis.net/wcs/2.0">
          <wcs:CoverageId>ASA_WSM_1PNDPA20050331_075939_000000552036_00035_16121_0775</wcs:CoverageId>
          <wcs:DimensionTrim>
            <wcs:Dimension>x</wcs:Dimension>
            <wcs:TrimLow>0</wcs:TrimLow>
            <wcs:TrimHigh>100</wcs:TrimHigh>
          </wcs:DimensionTrim>
          <wcs:DimensionTrim>
            <wcs:Dimension>y</wcs:Dimension>
            <wcs:TrimLow>0</wcs:TrimLow>
            <wcs:TrimHigh>100</wcs:TrimHigh>
          </wcs:DimensionTrim>
          <wcs:format>image/tiff</wcs:format>
          <wcs:mediaType>multipart/related</wcs:mediaType>
        </wcs:GetCoverage>"""
        return (params, "xml")