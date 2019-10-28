# -*- coding: utf-8 -*-

"""
图像处理
"""

import re
import sys
import math
import time
from .base import AipBase
from .base import base64
from .base import json
from .base import urlencode
from .base import quote

class AipImageProcess(AipBase):

    """
    图像处理
    """

    __imageQualityEnhanceUrl = 'https://aip.baidubce.com/rest/2.0/image-process/v1/image_quality_enhance'

    __dehazeUrl = 'https://aip.baidubce.com/rest/2.0/image-process/v1/dehaze'

    __contrastEnhanceUrl = 'https://aip.baidubce.com/rest/2.0/image-process/v1/contrast_enhance'

    
    def imageQualityEnhance(self, image, options=None):
        """
            图像无损放大
        """
        options = options or {}

        data = {}
        data['image'] = base64.b64encode(image).decode()

        data.update(options)

        return self._request(self.__imageQualityEnhanceUrl, data)
    
    def dehaze(self, image, options=None):
        """
            图像去雾
        """
        options = options or {}

        data = {}
        data['image'] = base64.b64encode(image).decode()

        data.update(options)

        return self._request(self.__dehazeUrl, data)
    
    def contrastEnhance(self, image, options=None):
        """
            图像对比度增强
        """
        options = options or {}

        data = {}
        data['image'] = base64.b64encode(image).decode()

        data.update(options)

        return self._request(self.__contrastEnhanceUrl, data)

    __colourizeUrl = 'https://aip.baidubce.com/rest/2.0/image-process/v1/colourize'
    def colourize(self, image, options=None):
        """
            黑白图像上色
        """
        options = options or {}

        data = {}
        data['image'] = base64.b64encode(image).decode()

        data.update(options)

        return self._request(self.__colourizeUrl, data)

    __stretch_restoreUrl = 'https://aip.baidubce.com/rest/2.0/image-process/v1/stretch_restore'
    def stretch_restore(self, image, options=None):
        """
            图像拉伸恢复
        """
        options = options or {}

        data = {}
        data['image'] = base64.b64encode(image).decode()

        data.update(options)

        return self._request(self.__stretch_restoreUrl, data)

    __style_transUrl = 'https://aip.baidubce.com/rest/2.0/image-process/v1/style_trans'
    def style_trans(self, image, options=None):
        """
            图像风格转换
        """
        options = options or {}

        data = {}
        data['image'] = base64.b64encode(image).decode()

        data.update(options)

        return self._request(self.__contrastEnhanceUrl, data)

    __inpaintingUrl = 'https://aip.baidubce.com/rest/2.0/image-process/v1/inpainting'
    def inpainting(self, image, options=None):
        """
            图像修复
        """
        options = options or {}

        data = {}
        data['image'] = base64.b64encode(image).decode()

        data.update(options)

        return self._request(self.__inpaintingUrl, data)